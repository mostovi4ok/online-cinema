from typing import Any

import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_mongo import Favourite, ProfileBell, Rating, Review


client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(test_settings.mongo_host, test_settings.mongo_port)


@pytest_asyncio.fixture(name="init_mongo", scope="session")
async def init_mongo(
    profile_async_session: async_sessionmaker[AsyncSession],
) -> None:
    await init_beanie(
        database=getattr(client, test_settings.mongo_name), document_models=[ProfileBell, Rating, Review, Favourite]
    )
