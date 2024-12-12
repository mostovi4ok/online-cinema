from typing import cast

from elasticsearch import AsyncElasticsearch

from services.elastic import ElasticService


es: AsyncElasticsearch | None = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> ElasticService:  # noqa: RUF029
    return ElasticService(cast(AsyncElasticsearch, es))
