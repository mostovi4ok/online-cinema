import json
from dataclasses import asdict
from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends

from api.v1.models import FullGenreQuery
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.elastic import ElasticService
from services.errors import ContentError
from services.redis import DEFAULT_REDIS, RedisService


class GenreService:
    def __init__(self, redis: RedisService, elastic: ElasticService) -> None:
        self.redis = redis
        self.elastic = elastic
        self.index = "genres"
        self.prefix_general = "genre"

    async def get_by_id(self, genre_id: str) -> Genre:
        genre = await self.redis.get(self.prefix_general, "by_id", genre_id)
        if genre is None:
            doc = await self.elastic.get(self.index, genre_id)
            genre = None if doc is None else Genre(**doc["_source"])
            await self.redis.set(self.prefix_general, "by_id", genre_id, genre)

        if genre is None or genre is DEFAULT_REDIS:
            raise ContentError(message="genre not found")

        return cast(Genre, genre)

    async def search(self, query: FullGenreQuery) -> list[Genre]:
        full_query = json.dumps(asdict(query))
        genres = await self.redis.get(self.prefix_general, "search", full_query)
        if genres is None:
            docs = await self.elastic.search(
                index=self.index, q=query.q, from_=(query.page_number - 1) * query.page_size, size=query.page_size
            )
            genres = [] if docs is None else [Genre(**doc["_source"]) for doc in list(docs["hits"]["hits"])]
            await self.redis.set(self.prefix_general, "search", full_query, genres)

        if not genres or genres is DEFAULT_REDIS:
            raise ContentError(message="genres not found")

        return cast(list[Genre], genres)


@lru_cache
def get_genre_service(
    redis: Annotated[RedisService, Depends(get_redis)], elastic: Annotated[ElasticService, Depends(get_elastic)]
) -> GenreService:
    return GenreService(redis, elastic)
