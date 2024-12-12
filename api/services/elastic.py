from typing import Any

import backoff
from elastic_transport import ConnectionError as ElasticConnectionError
from elastic_transport._response import ObjectApiResponse
from elasticsearch import AsyncElasticsearch, BadRequestError, NotFoundError


class ElasticService:
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    @backoff.on_exception(backoff.expo, ElasticConnectionError)
    async def search(self, index: str, **kwargs: Any) -> ObjectApiResponse[Any] | None:
        try:
            return await self.elastic.search(index=index, **kwargs)
        except (NotFoundError, BadRequestError):
            return None

    @backoff.on_exception(backoff.expo, ElasticConnectionError)
    async def get(self, index: str, id: str) -> ObjectApiResponse[Any] | None:
        try:
            return await self.elastic.get(index=index, id=id)
        except (NotFoundError, BadRequestError):
            return None
