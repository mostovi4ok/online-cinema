from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class ProfileBell(Document):
    notification_id: Annotated[UUID, Indexed()]
    profile_id: Annotated[UUID, Indexed()]
    message: str
    viewed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    viewed_at: datetime | None = None

    class Settings:
        name = "profile_bell"


class Rating(Document):
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)  # pyright: ignore[reportIncompatibleVariableOverride]
    user_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    film_id: UUID = Field(default_factory=uuid4)
    rating: float

    class Settings:
        name = "ratings"


class Review(Document):
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)  # pyright: ignore[reportIncompatibleVariableOverride]
    user_id: UUID = Field(default_factory=uuid4)
    film_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    review: str

    class Settings:
        name = "reviews"


class Favourite(Document):
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)  # pyright: ignore[reportIncompatibleVariableOverride]
    user_id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    film_id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "favourites"
