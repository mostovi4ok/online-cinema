from collections.abc import AsyncGenerator
from typing import Any

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from configs.settings import settings
from db.models_mongo import ProfileBell, State


client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)


async def init_mongo() -> AsyncGenerator[None, Any]:
    await init_beanie(database=getattr(client, settings.mongo_name), document_models=[State, ProfileBell])
    yield
