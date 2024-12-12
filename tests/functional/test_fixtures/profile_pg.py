from collections.abc import AsyncGenerator, Callable, Coroutine
from typing import Any

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from testdata.profile_db_model import Base


@pytest_asyncio.fixture(name="profile_engine", scope="session")
def profile_engine() -> AsyncEngine:
    return create_async_engine(test_settings.profile_postgres_url)


@pytest_asyncio.fixture(name="profile_async_session", scope="session")
def profile_async_session(profile_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(profile_engine, expire_on_commit=False)


@pytest_asyncio.fixture(name="profile_pg_session", scope="session")
async def profile_pg_session(profile_async_session: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with profile_async_session() as session:
        yield session


@pytest_asyncio.fixture(name="profile_create_database")
def profile_create_database(profile_engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with profile_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return inner


@pytest_asyncio.fixture(name="profile_drop_database")
def profile_drop_database(profile_engine: AsyncEngine) -> Callable[[], Coroutine[Any, Any, None]]:
    async def inner() -> None:
        async with profile_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    return inner
