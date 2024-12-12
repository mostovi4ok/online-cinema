from collections.abc import AsyncGenerator, Callable, Coroutine
from typing import Any

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from testdata.auth_db_model import Base


@pytest_asyncio.fixture(name="auth_engine", scope="session")
def auth_engine() -> AsyncEngine:
    return create_async_engine(test_settings.auth_postgres_url)


@pytest_asyncio.fixture(name="auth_async_session", scope="session")
def auth_async_session(auth_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(auth_engine, expire_on_commit=False)


@pytest_asyncio.fixture(name="auth_pg_session", scope="session")
async def auth_pg_session(
    auth_async_session: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, Any]:
    async with auth_async_session() as session:
        yield session


@pytest_asyncio.fixture(name="auth_create_database")
def auth_create_database(auth_engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with auth_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return inner


@pytest_asyncio.fixture(name="auth_drop_database")
def auth_drop_database(auth_engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with auth_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    return inner
