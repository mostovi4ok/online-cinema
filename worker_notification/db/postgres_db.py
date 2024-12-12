from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from configs.settings import settings


engine_admin = create_async_engine(settings.postgres_dsn_admin)
async_session_admin = async_sessionmaker(engine_admin, expire_on_commit=False)

session_pg_admin: AsyncSession | None = None


async def start_session_pg_admin() -> AsyncGenerator[None, Any]:
    async with async_session_admin() as session:
        global session_pg_admin  # noqa: PLW0603
        session_pg_admin = session
        yield


def get_admin_session() -> AsyncSession:
    assert session_pg_admin is not None
    return session_pg_admin


engine_auth = create_async_engine(settings.postgres_dsn_auth)
async_session_auth = async_sessionmaker(engine_auth, expire_on_commit=False)

session_pg_auth: AsyncSession | None = None


async def start_session_pg_auth() -> AsyncGenerator[None, Any]:
    async with async_session_auth() as session:
        global session_pg_auth  # noqa: PLW0603
        session_pg_auth = session
        yield


def get_auth_session() -> AsyncSession:
    assert session_pg_auth is not None
    return session_pg_auth
