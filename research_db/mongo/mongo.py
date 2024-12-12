from collections.abc import Generator
from typing import Any
from uuid import UUID

from loguru import logger
from pymongo import MongoClient
from pymongo.collection import Collection

from configs.settings import settings
from generator_events.decorators import time_it
from generator_events.generate_data import Event, generate_events


TOTAL = 1_000_000
BATCH_SIZE = 1_000


def mongo_conn() -> Collection[Any]:
    client: MongoClient[Any] = MongoClient(settings.mongo_host, settings.mongo_port)
    db = client["test_db"]
    return db["users"]


@time_it(TOTAL)
def insert_data(users_collection: Collection[Any], event_generator: Generator[list[Event], None, None]) -> list[UUID]:
    uuids: list[UUID] = []
    for i, batch in enumerate(event_generator):
        logger.info(f"Вставка батча №{i}")
        users_collection.insert_many(event.model_dump(mode="json") for event in batch)
        uuids.extend(ev.user_id for ev in batch)

    return uuids


@time_it(TOTAL)
def select_data(uuids: list[UUID], users_collection: Collection[Any]) -> None:
    for i, uuid in enumerate(uuids):
        users_collection.find_one({"user_id": str(uuid)})
        if i % BATCH_SIZE == 0:
            logger.info(f"Чтение записи №{i}")


def main() -> None:
    users_collection = mongo_conn()

    logger.info("Вставка данных в бд.")
    uuids = insert_data(users_collection, generate_events(count=TOTAL, batch_size=BATCH_SIZE))
    logger.info("Вставка данных в бд закончена.")

    logger.info("Чтение данных из бд.")
    select_data(uuids, users_collection)
    logger.info("Чтение данных из бд закончено.")

    users_collection.delete_many({})


if __name__ == "__main__":
    main()
