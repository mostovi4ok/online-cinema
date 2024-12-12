from asyncio import get_event_loop
from contextlib import suppress

import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from configs.logger import setup_logger
from configs.settings import settings
from db.mongo_db import init_mongo
from db.postgres_db import start_session_pg_admin, start_session_pg_auth
from extractors import KafkaExtractor


logger = settings.logger


if settings.sentry_on:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


async def main() -> None:
    await anext(start_session_pg_admin())
    await anext(start_session_pg_auth())
    await anext(init_mongo())
    logger.info("Старт etl")
    async with KafkaExtractor() as extractor:
        async for item in extractor.extract():
            if item is not None:
                for func, tasks in item.items():
                    if tasks:
                        await func(tasks)

    logger.info("Etl завершен")


if __name__ == "__main__":
    setup_logger()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        main, "interval", seconds=settings.run_interval_seconds, max_instances=settings.scheduler_max_instances
    )
    logger.info("Запуск планировщика")
    scheduler.start()

    with suppress(KeyboardInterrupt, SystemExit):
        get_event_loop().run_forever()
