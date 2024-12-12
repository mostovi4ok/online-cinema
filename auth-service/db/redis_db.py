from functools import lru_cache

from redis.asyncio import Redis

from core.config import configs


@lru_cache
def get_redis() -> Redis:
    return Redis(host=configs.redis_host, port=configs.redis_port)
