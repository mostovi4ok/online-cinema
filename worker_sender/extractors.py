from collections import defaultdict
from collections.abc import AsyncIterator, Callable, Coroutine
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Self

import backoff
from aiokafka import AIOKafkaConsumer, ConsumerRecord, TopicPartition
from aiokafka.errors import KafkaConnectionError, KafkaError
from avro.datafile import DataFileReader
from avro.io import DatumReader
from pydantic import ValidationError

from configs.settings import settings
from models import EmailTask, Task
from sender_emails import send_email
from sender_producer import sender_producer


logger = settings.logger


@dataclass(frozen=True)
class DataContract:
    model: type[Task]
    func: Callable[..., Coroutine[Any, Any, Any]]
    dlq: str


@dataclass(frozen=True)
class Contracts:
    api_kafka_email: DataContract = DataContract(model=EmailTask, func=send_email, dlq="api_kafka_email_dlq")  # noqa: RUF009
    api_kafka_email_dlq: DataContract = api_kafka_email


class KafkaExtractor:
    def __init__(self) -> None:
        self.consumer = self.get_consumer()

    def _avro_deserializer(self, data: bytes) -> DataFileReader:
        return DataFileReader(BytesIO(data), DatumReader())

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    def get_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *settings.kafka_topics,
            group_id=settings.kafka_group_id,
            bootstrap_servers=settings.kafka_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=self._avro_deserializer,
        )

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aenter__(self) -> Self:
        await self.consumer.start()
        return self

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if exc_type is None:
            await self.consumer.commit()

        await self.consumer.stop()

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def extract(self) -> AsyncIterator[defaultdict[Callable[..., Coroutine[Any, Any, Any]], list[Task]] | None]:
        try:
            data = await self.consumer.getmany(timeout_ms=100, max_records=settings.kafka_max_records)
        except KafkaError:
            logger.exception("Ошибка при получении сообщений от kafka")
            return

        if not data:
            logger.info("Нет новых сообщений от kafka")

        for topic_partition, messages in data.items():
            assert isinstance(topic_partition, TopicPartition)

            topic = topic_partition.topic
            logger.info(f"Получил {len(messages)} сообщений от kafka,  тема {topic}")
            for message in messages:
                assert isinstance(message, ConsumerRecord)

                if (values := message.value) is None:
                    logger.info("Данные отсутствуют")
                    continue

                assert isinstance(values, DataFileReader)
                if (key := message.key) is None or (contract := getattr(Contracts, key.decode(), None)) is None:
                    logger.info("Нет контракта")
                    continue

                assert isinstance(contract, DataContract)
                tasks: defaultdict[Callable[..., Coroutine[Any, Any, Any]], list[Task]] = defaultdict(list)
                for value in values:
                    logger.info(f"Сообщение: {value}")
                    try:
                        task = contract.model.model_validate(value)
                    except ValidationError:
                        logger.exception(f"Ошибка при анализе данных события {data}")
                        await sender_producer([value], contract.dlq)
                        continue

                    task.value = value
                    task.key = key.decode()
                    task.key_dlq = contract.dlq
                    func = contract.func
                    tasks[func].append(task)

                    assert task.value is not None
                    assert task.key is not None
                    assert task.key_dlq is not None

                yield tasks
