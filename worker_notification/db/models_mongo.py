from datetime import datetime
from typing import Annotated
from uuid import UUID

from beanie import Document, Indexed
from pydantic import Field


class State(Document):
    notification_id: Annotated[UUID, Indexed()]
    send: bool = False

    class Settings:
        name = "state"


class ProfileBell(Document):
    notification_id: Annotated[UUID, Indexed()]
    profile_id: Annotated[UUID, Indexed()]
    message: str
    viewed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    viewed_at: datetime | None = None

    class Settings:
        name = "profile_bell"
