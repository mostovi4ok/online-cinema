import builtins
import hashlib
import pickle  # noqa: S403
from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

import backoff
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

from core.config import configs


redis: Redis = Redis(host=configs.redis_host, port=configs.redis_port)
DEFAULT_REDIS = object()


class RedisService:
    def __init__(self, redis_instance: Redis) -> None:
        self._redis = redis_instance

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get(self, prefix_general: str, prefix_local: str, key: str) -> None | Any | object:
        if (data := await self._redis.get(f"{prefix_general}_{prefix_local}:{key}")) is None:
            return None

        result = pickle.loads(data)[0]  # noqa: S301
        return DEFAULT_REDIS if result is None else result

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _check_token(self, user_id: UUID, token_type: str, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:{token_type}:{token_hash}'"""
        token_hash = self._compute_hash(token)
        token_value = await self._redis.get(f"{user_id}:{token_type}:{token_hash}")
        return token_value is not None

    async def check_banned_access(self, user_id: UUID, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:access:{token_hash}'"""
        return await self._check_token(user_id, "access", token)

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_user_rights(self, user_id: UUID) -> builtins.set[UUID]:
        """Возвращает все права пользователя из Redis записи с ключем в формате '{user_id}:rights'"""
        rights_bytes = await self._redis.smembers(f"{user_id}:rights")
        return {pickle.loads(right) for right in rights_bytes}  # noqa: S301

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_all_rights(self) -> builtins.set[tuple[UUID, str]]:
        """Возвращает все права из Redis записи с ключем 'rights'"""
        rights_bytes = await self._redis.smembers("rights")
        return {pickle.loads(right) for right in rights_bytes}  # noqa: S301

    def _compute_hash(self, data: str) -> str:
        data_bytes = data.encode("utf-8")
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()

    async def add_email_confirmation_url(self, user_id: UUID) -> str:
        """Создает, кладёт в Redis и возвращает URL для подтверждения почты пользователя"""
        user_link = str(uuid4())
        url = f"{configs.email_confirmation_url}/{user_link}"
        await self._redis.setex(
            f"email_confirmation:{user_link}",
            configs.email_confirmation_lifetime_min * 60,
            pickle.dumps((user_id,), protocol=pickle.HIGHEST_PROTOCOL),
        )
        return url

    async def get_email_confirmation(self, url: UUID) -> UUID | None:
        """Возвращает user_id из Redis по URL для подтверждения почты"""
        user_id_bytes = await self._redis.get(f"email_confirmation:{url}")
        if user_id_bytes:
            await self._redis.delete(f"email_confirmation:{url}")
            return pickle.loads(user_id_bytes)[0]  # noqa: S301

        return None


@lru_cache
def get_redis_service() -> RedisService:
    return RedisService(redis)
