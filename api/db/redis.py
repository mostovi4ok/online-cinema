from typing import cast

from redis.asyncio import Redis

from services.redis import RedisService


redis: Redis | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> RedisService:  # noqa: RUF029
    return RedisService(cast(Redis, redis))
