import json
from dataclasses import asdict
from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends

from api.v1.models import FullFilmQuery
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.elastic import ElasticService
from services.errors import ContentError
from services.redis import DEFAULT_REDIS, RedisService


class FilmService:
    def __init__(self, redis: RedisService, elastic: ElasticService) -> None:
        self.redis = redis
        self.elastic = elastic
        self.index = "movies"
        self.prefix_general = "movie"

    async def get_by_id(self, film_id: str) -> Film:
        film = await self.redis.get(self.prefix_general, "by_id", film_id)
        if film is None:
            doc = await self.elastic.get(self.index, film_id)
            film = None if doc is None else Film(**doc["_source"])
            await self.redis.set(self.prefix_general, "by_id", film_id, film)

        if film is None or film is DEFAULT_REDIS:
            raise ContentError(message="film not found")

        return cast(Film, film)

    async def search(self, query: FullFilmQuery) -> list[Film]:
        full_query = json.dumps(asdict(query))
        films = await self.redis.get(self.prefix_general, "search", full_query)
        if films is None:
            docs = await self.elastic.search(
                self.index,
                query=query.generate_query(),
                sort=query.sort,
                from_=(query.page_number - 1) * query.page_size,
                size=query.page_size,
            )
            films = [] if docs is None else [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]
            await self.redis.set(self.prefix_general, "search", full_query, films)

        if not films or films is DEFAULT_REDIS:
            raise ContentError(message="films not found")

        return cast(list[Film], films)


@lru_cache
def get_film_service(
    redis: Annotated[RedisService, Depends(get_redis)], elastic: Annotated[ElasticService, Depends(get_elastic)]
) -> FilmService:
    return FilmService(redis, elastic)
