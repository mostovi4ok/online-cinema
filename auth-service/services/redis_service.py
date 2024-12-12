import hashlib
import pickle  # noqa: S403
from functools import lru_cache
from typing import Any, cast
from uuid import UUID

import backoff
from fastapi import HTTPException, status
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

from api.v1.models.access_control import RightModel
from core.config import configs


redis: Redis | None = None


class RedisService:
    def __init__(self, redis_instance: Redis) -> None:
        self._redis = redis_instance

    def _compute_hash(self, data: str) -> str:
        data_bytes = data.encode("utf-8")
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _add_token(
        self,
        user_id: str | int | UUID | None,
        token_type: str,
        token: str,
        data: str | int | UUID | None,
        time_to_exp: int,
    ) -> None:
        """Добавляет токен в Redis с ключем в формате '{user_id}:{token_type}:{token_hash}'"""
        token_hash = self._compute_hash(token)
        return await self._redis.setex(
            f"{user_id}:{token_type}:{token_hash}", time_to_exp, pickle.dumps((data,), protocol=pickle.HIGHEST_PROTOCOL)
        )

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def _check_token(self, user_id: str | int | UUID | None, token_type: str, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:{token_type}:{token_hash}'"""
        token_hash = self._compute_hash(token)
        token_value: Any = await self._redis.get(f"{user_id}:{token_type}:{token_hash}")
        return token_value is not None

    async def add_banned_access(
        self, user_id: str | int | UUID | None, token: str, data: str | int | UUID | None
    ) -> None:
        """Добавляет в Redis запись с ключем в формате '{user_id}:access:{token_hash}'"""
        time_to_exp = configs.access_token_min * 60
        return await self._add_token(user_id, "access", token, data, time_to_exp)

    async def add_valid_refresh(self, user_id: UUID, token: str, data: str) -> None:
        """Добавляет в Redis запись с ключем в формате '{user_id}:refresh:{token_hash}'"""
        time_to_exp = configs.refresh_token_min * 60
        return await self._add_token(user_id, "refresh", token, data, time_to_exp)

    async def check_banned_access(self, user_id: str | int | UUID | None, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:access:{token_hash}'"""
        return await self._check_token(user_id, "access", token)

    async def check_valid_refresh(self, user_id: UUID, token: str) -> bool:
        """Проверяет наличие в Redis записи с ключем в формате '{user_id}:refresh:{token_hash}'"""
        return await self._check_token(user_id, "refresh", token)

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_refresh(self, user_id: str | int | UUID | None, token: str) -> str:
        """Удаляет из Redis запись с ключем в формате '{user_id}:refresh:{token_hash}' и возвращает её значение"""
        token_hash = self._compute_hash(token)
        refresh_in_redis: Any = await self._redis.get(f"{user_id}:refresh:{token_hash}")
        if not refresh_in_redis:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        deleted_token_data = pickle.loads(refresh_in_redis)[0]  # noqa: S301
        await self._redis.delete(f"{user_id}:refresh:{token_hash}")
        return deleted_token_data

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_all_refresh(self, user_id: str | int | UUID | None) -> list[str]:
        """Удаляет из Redis все записи с ключем в формате '{user_id}:refresh:*' и возвращает их значения"""
        keys: Any = await self._redis.keys(pattern=f"{user_id}:refresh:*")
        deleted_tokens_data = [pickle.loads(await self._redis.get(key))[0] for key in keys]  # noqa: S301
        if keys:
            await self._redis.delete(*keys)

        return deleted_tokens_data

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def add_user_right(self, user_id: UUID, data: list[UUID] | UUID) -> None:
        """Добавляет в Redis запись с ключем в формате '{user_id}:rights' или добавляет в него значение right"""
        if not data:
            return

        if not isinstance(data, list):
            data = [data]

        data_ = [pickle.dumps(right, protocol=pickle.HIGHEST_PROTOCOL) for right in data]
        await self._redis.sadd(f"{user_id}:rights", *data_)

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_user_rights(self, user_id: UUID) -> set[UUID]:
        """Возвращает все права пользователя из Redis записи с ключем в формате '{user_id}:rights'"""
        rights_bytes = await self._redis.smembers(f"{user_id}:rights")
        return {pickle.loads(right) for right in rights_bytes}  # noqa: S301

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def get_all_rights(self) -> set[tuple[UUID, str]]:
        """Возвращает все права из Redis записи с ключем 'rights'"""
        rights_bytes = await self._redis.smembers("rights")
        return {pickle.loads(right) for right in rights_bytes}  # noqa: S301

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def set_all_rights(self, rights: list[RightModel]) -> None:
        """Устанавливает в Redis запись с ключем 'rights' и/или заменяет её значениями rights"""
        await self._redis.delete("rights")
        for right in rights:
            await self._redis.sadd("rights", pickle.dumps((right.id, right.name), protocol=pickle.HIGHEST_PROTOCOL))

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def add_right(self, right: RightModel) -> None:
        """Добавляет в Redis запись с ключем 'rights' и/или добавляет в него значение right"""
        await self._redis.sadd("rights", pickle.dumps((right.id, right.name), protocol=pickle.HIGHEST_PROTOCOL))

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def update_right(self, right: RightModel) -> None:
        """Обновляет в Redis запись с ключем 'rights' существующее значение right на новое"""
        current_rights_dict = {right[0]: right[1] for right in await self.get_all_rights()}
        if right.id in current_rights_dict:
            await self._redis.srem(
                "rights", pickle.dumps((right.id, current_rights_dict[right.id]), protocol=pickle.HIGHEST_PROTOCOL)
            )

        await self._redis.sadd("rights", pickle.dumps((right.id, right.name), protocol=pickle.HIGHEST_PROTOCOL))

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_user_right(self, user_id: UUID, right: UUID) -> None:
        """Удаляет из зписи в Redis с ключем в формате '{user_id}:rights' значение right"""
        await self._redis.srem(f"{user_id}:rights", pickle.dumps(right, protocol=pickle.HIGHEST_PROTOCOL))

    @backoff.on_exception(backoff.expo, RedisConnectionError)
    async def delete_right(self, right_id: UUID, right_name: str) -> None:
        """Удаляет из всех зписей в Redis с ключем в формате '*rights*' значение right"""
        keys = cast(list[str], await self._redis.keys(pattern="*rights*"))
        for key in keys:
            await self._redis.srem(key, pickle.dumps(right_id, protocol=pickle.HIGHEST_PROTOCOL))

        await self._redis.srem("rights", pickle.dumps((right_id, right_name), protocol=pickle.HIGHEST_PROTOCOL))


@lru_cache
def get_redis() -> RedisService:
    return RedisService(cast(Redis, redis))
