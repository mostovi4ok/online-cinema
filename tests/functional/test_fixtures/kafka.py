from collections.abc import AsyncGenerator
from io import BytesIO
from typing import Any

import backoff
import pytest_asyncio
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from avro.datafile import DataFileReader
from avro.io import DatumReader

from core.settings import test_settings


class KafkaExtractor:
    def __init__(self) -> None:
        self.consumer = self.get_consumer()

    def _avro_deserializer(self, data: bytes) -> DataFileReader:
        return DataFileReader(BytesIO(data), DatumReader())

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    def get_consumer(self) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *test_settings.kafka_topics,
            group_id=test_settings.kafka_group_id,
            bootstrap_servers=test_settings.kafka_urls,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=self._avro_deserializer,
        )

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aenter__(self) -> AIOKafkaConsumer:
        await self.consumer.start()
        return self.consumer

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        await self.consumer.stop()


@pytest_asyncio.fixture(name="consumer", scope="session")
async def consumer() -> AsyncGenerator[AIOKafkaConsumer, Any]:
    async with KafkaExtractor() as consumer:
        yield consumer
