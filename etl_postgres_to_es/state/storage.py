from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from loguru import Logger
    from redis import Redis


STATE_KEY = "last_modified"


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None: ...

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]: ...


class JsonFileStorage(BaseStorage):
    def __init__(self, logger: Logger, con_redis: Redis) -> None:
        self._logger = logger
        self.con_redis = con_redis

    def save_state(self, state: dict[str, Any]) -> None:
        self.con_redis.mset(state)
        self._logger.info(f"All changes until {state[STATE_KEY]} have been postponed")

    def retrieve_state(self) -> dict[str, Any]:
        try:
            return {STATE_KEY: self.con_redis.get(STATE_KEY).decode("utf-8")}  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
        except AttributeError:
            self._logger.warning("No state.")
            return {}
