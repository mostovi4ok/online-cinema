from collections.abc import Generator
from typing import Any, cast
from uuid import UUID

from loguru import logger
from psycopg import ClientCursor, Cursor, connect  # pyright: ignore[reportUnknownVariableType]
from psycopg.rows import dict_row

from configs.settings import settings
from generator_events.decorators import time_it
from generator_events.generate_data import Event, generate_events


TOTAL = 1_000_000
BATCH_SIZE = 1_000


@time_it(TOTAL)
def insert_data(event_generator: Generator[list[Event], None, None], cursor: Cursor[Any]) -> list[UUID]:
    uuids: list[UUID] = []
    for i, batch in enumerate(event_generator):
        logger.info(f"Вставка батча №{i}")
        query = (
            f"INSERT INTO public.test ({",".join(f for f in Event.model_fields)}) "  # noqa: S608
            f"VALUES ({",".join("%s" for _ in Event.model_fields)})"
        )
        values = tuple(tuple(value.model_dump().values()) for value in batch)
        cursor.executemany(query, values)  # pyright: ignore[reportArgumentType]
        uuids.extend(ev.user_id for ev in batch)

    return uuids


@time_it(TOTAL)
def select_data(uuids: list[UUID], cursor: Cursor[Any]) -> None:
    for i, uuid in enumerate(uuids):
        cursor.execute(f"SELECT * FROM public.test WHERE user_id = '{uuid}'")  # pyright: ignore[reportArgumentType]  # noqa: S608
        if i % BATCH_SIZE == 0:
            logger.info(f"Чтение записи №{i}")


def main() -> None:
    with (
        connect(**settings.postgres_dsn, row_factory=dict_row, cursor_factory=ClientCursor) as conn,  # pyright: ignore[reportCallIssue, reportUnknownVariableType, reportArgumentType]
        conn.cursor() as cursor,  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    ):
        cursor = cast(Cursor[Any], cursor)

        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS public.test "
            f"({", ".join(f"{name} {info.description}" for name, info in Event.model_fields.items())});"  # pyright: ignore[reportArgumentType]
        )
        logger.info("Вставка данных в бд.")
        uuids = insert_data(generate_events(count=TOTAL, batch_size=BATCH_SIZE), cursor)
        logger.info("Вставка данных в бд закончена.")

        logger.info("Чтение данных из бд.")
        select_data(uuids, cursor)
        logger.info("Чтение данных из бд закончено.")

        cursor.execute("""DROP TABLE IF EXISTS public.test""")


if __name__ == "__main__":
    main()
