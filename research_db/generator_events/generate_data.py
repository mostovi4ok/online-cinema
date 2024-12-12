from collections.abc import Generator
from datetime import datetime
from uuid import UUID, uuid4

import faker
from pydantic import BaseModel, Field


fake = faker.Faker()


class Event(BaseModel):
    user_id: UUID = Field(description="uuid NOT NULL", default_factory=uuid4)
    film_id: str | None = Field(description="varchar(256)", default_factory=fake.text)
    prev_qual: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    new_qual: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    element_id: str | None = Field(description="varchar(256)", default_factory=fake.text)
    group_id: str | None = Field(description="varchar(256)", default_factory=fake.text)
    time: str | None = Field(description="varchar(256)", default_factory=fake.text)
    action: str | None = Field(description="varchar(256)", default_factory=fake.text)
    feedback: str | None = Field(description="varchar(256)", default_factory=fake.text)
    review: str | None = Field(description="varchar(256)", default_factory=fake.text)
    rating: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    filter_id_genre: list[str] = Field(description="text[]", default_factory=fake.texts)
    filter_rating: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    filter_id_actor: list[str] = Field(description="text[]", default_factory=fake.texts)
    film_curr_time: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    film_abs_time: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    url: str | None = Field(description="varchar(256)", default_factory=fake.url)
    spent_time: int | None = Field(description="INTEGER NOT NULL", default_factory=fake.random_digit)
    timestamp: datetime = Field(description="timestamp with time zone NOT NULL", default_factory=fake.date_time)


def generate_events(count: int, batch_size: int) -> Generator[list[Event], None, None]:
    def event_generator() -> Generator[list[Event], None, None]:
        batch: list[Event] = []
        for _ in range(count):
            batch.append(Event())
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

    return event_generator()
