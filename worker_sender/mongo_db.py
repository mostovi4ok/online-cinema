from collections.abc import AsyncGenerator
from typing import Annotated, Any
from uuid import UUID

from beanie import Document, Indexed, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from configs.settings import settings


class State(Document):
    notification_id: Annotated[UUID, Indexed()]
    send: bool

    class Settings:
        name = "state"


client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)


async def init_mongo() -> AsyncGenerator[None, Any]:
    await init_beanie(database=getattr(client, settings.mongo_name), document_models=[State])
    yield
