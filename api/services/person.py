import json
from dataclasses import asdict
from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends

from api.v1.models import FullPersonQuery
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.elastic import ElasticService
from services.errors import ContentError
from services.redis import DEFAULT_REDIS, RedisService


class PersonService:
    def __init__(self, redis: RedisService, elastic: ElasticService) -> None:
        self.redis = redis
        self.elastic = elastic
        self.index = "persons"
        self.prefix_general = "person"

    async def get_by_id(self, person_id: str) -> Person:
        person = await self.redis.get(self.prefix_general, "by_id", person_id)
        if person is None:
            doc = await self.elastic.get(self.index, person_id)
            person = None if doc is None else Person(**doc["_source"])
            await self.redis.set(self.prefix_general, "by_id", person_id, person)

        if person is None or person is DEFAULT_REDIS:
            raise ContentError(message="person not found")

        return cast(Person, person)

    async def search(self, query: FullPersonQuery) -> list[Person]:
        full_query = json.dumps(asdict(query))
        persons = await self.redis.get(self.prefix_general, "search", full_query)
        if persons is None:
            docs = await self.elastic.search(
                index=self.index, q=query.q, from_=(query.page_number - 1) * query.page_size, size=query.page_size
            )
            persons = [] if docs is None else [Person(**doc["_source"]) for doc in list(docs["hits"]["hits"])]
            await self.redis.set(self.prefix_general, "search", full_query, persons)

        if not persons or persons is DEFAULT_REDIS:
            raise ContentError(message="persons not found")

        return cast(list[Person], persons)


@lru_cache
def get_person_service(
    redis: Annotated[RedisService, Depends(get_redis)], elastic: Annotated[ElasticService, Depends(get_elastic)]
) -> PersonService:
    return PersonService(redis, elastic)
