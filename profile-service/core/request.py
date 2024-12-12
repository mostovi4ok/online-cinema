from collections.abc import AsyncGenerator
from typing import Any

from aiohttp import ClientSession


async def get_aio_session() -> AsyncGenerator[ClientSession, Any]:
    async with ClientSession(raise_for_status=True, conn_timeout=3, read_timeout=10) as session:
        yield session
