import datetime
from typing import Annotated
from uuid import UUID

from beanie import Document, Indexed
from pydantic import Field


class ProfileBell(Document):
    notification_id: Annotated[UUID, Indexed()]
    profile_id: Annotated[UUID, Indexed()]
    message: str
    viewed: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    viewed_at: datetime.datetime | None = None

    class Settings:
        name = "profile_bell"
