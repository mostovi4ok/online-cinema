from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from aiohttp import ClientSession


@pytest_asyncio.fixture(name="aio_session", scope="session")
async def aio_session() -> AsyncGenerator[ClientSession, Any]:
    async with ClientSession() as session:
        yield session
