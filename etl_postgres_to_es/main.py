from datetime import datetime
from time import sleep
from typing import Any, cast

import backoff
import psycopg
import sentry_sdk
from elastic_transport import ConnectionError as ElasticConnectionError
from elasticsearch import Elasticsearch
from loguru import logger
from psycopg.rows import dict_row
from redis import Redis
from redis import exceptions as redis_exceptions

from configs.settings import settings
from postgres_to_es.postgres_to_es import fetch_changed_data, save_in_es, transform_pg_to_es
from schemes_index_es import GENRE_SCHEMES_INDEX_ES, MOVIES_SCHEMES_INDEX_ES, PERSON_SCHEMES_INDEX_ES
from state.state import State
from state.storage import STATE_KEY, JsonFileStorage


if settings.sentry_on:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


@backoff.on_exception(
    backoff.expo,
    (
        psycopg.OperationalError,
        ElasticConnectionError,
        redis_exceptions.RedisClusterException,
    ),
)
def main() -> None:
    indexs_es = {
        "movies": MOVIES_SCHEMES_INDEX_ES,
        "persons": PERSON_SCHEMES_INDEX_ES,
        "genres": GENRE_SCHEMES_INDEX_ES,
    }
    with (
        psycopg.connect(  # pyright: ignore
            **settings.postgres_dsn,  # pyright: ignore[reportArgumentType]
            row_factory=dict_row,
            cursor_factory=psycopg.ClientCursor,
        ) as conn,  # pyright: ignore
        conn.cursor() as cursor_movie,  # pyright: ignore
        conn.cursor() as cursor_person,  # pyright: ignore
        conn.cursor() as cursor_genre,  # pyright: ignore
        Elasticsearch(settings.elastic_dsn) as client,
        Redis(host=settings.redis_host, port=settings.redis_port) as con_redis,
    ):
        cursor_movie = cast(psycopg.Cursor[Any], cursor_movie)
        cursor_person = cast(psycopg.Cursor[Any], cursor_person)
        cursor_genre = cast(psycopg.Cursor[Any], cursor_genre)

        state = State(JsonFileStorage(logger=logger, con_redis=con_redis))

        for ind_name, scheme in indexs_es.items():
            if not client.indices.exists(index=ind_name):
                client.indices.create(index=ind_name, body=scheme)

        while True:
            logger.info("Starting ETL process ...")
            if last_updated := state.get_state(STATE_KEY):
                last_updated = datetime.fromisoformat(last_updated)

            save_in_es(
                data=transform_pg_to_es(
                    objects=fetch_changed_data(cursor=cursor_movie, last_modified=last_updated or datetime.min),
                    cursor_person=cursor_person,
                    cursor_genre=cursor_genre,
                ),
                state=state,
                client=client,
            )
            sleep(settings.restart_time)


if __name__ == "__main__":
    main()
