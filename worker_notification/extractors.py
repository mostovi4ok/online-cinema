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
from models.task_models import (
    ApiKafkaEmailConfirmation,
    ApiKafkaNotificationInProfile,
    ApiKafkaNotificationNewFilms,
    ApiKafkaNotificationNewSeries,
    FunctionsSend,
    Task,
)
from sender import sender


logger = settings.logger


@dataclass(frozen=True)
class DataContract:
    model: type[Task]
    dlq: str


@dataclass(frozen=True)
class Contracts:
    api_kafka_email_confirmation: DataContract = DataContract(  # noqa: RUF009
        model=ApiKafkaEmailConfirmation, dlq="api_kafka_email_confirmation_dlq"
    )
    api_kafka_email_confirmation_dlq: DataContract = api_kafka_email_confirmation

    api_kafka_notification_new_films: DataContract = DataContract(  # noqa: RUF009
        model=ApiKafkaNotificationNewFilms, dlq="api_kafka_notification_new_films_dlq"
    )
    api_kafka_notification_new_films_dlq: DataContract = api_kafka_notification_new_films
    api_kafka_notification_new_series: DataContract = DataContract(  # noqa: RUF009
        model=ApiKafkaNotificationNewSeries, dlq="api_kafka_notification_new_series_dlq"
    )
    api_kafka_notification_new_series_dlq: DataContract = api_kafka_notification_new_series
    api_kafka_notification_in_profile: DataContract = DataContract(  # noqa: RUF009
        model=ApiKafkaNotificationInProfile, dlq="api_kafka_notification_in_profile_dlq"
    )
    api_kafka_notification_in_profile_dlq: DataContract = api_kafka_notification_in_profile


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
                        logger.exception(f"Ошибка при анализе данных {value}")
                        if not await sender([value], contract.dlq):
                            logger.exception(f"Ошибка при отправки данныя {value} в очередь DLQ")

                        continue

                    task.value = value
                    task.key = key.decode()
                    task.key_send_dlq = contract.dlq
                    func: tuple[Callable[[list[Task]], Coroutine[Any, Any, None]], str] = getattr(
                        FunctionsSend, task.method_send
                    )
                    task.key_send = func[1]

                    tasks[func[0]].append(task)

                    assert task.value is not None
                    assert task.key is not None
                    assert task.key_send_dlq is not None

                yield tasks
