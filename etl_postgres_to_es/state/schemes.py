import uuid
from datetime import date, datetime
from typing import Literal, TypedDict

from pydantic import BaseModel


Role = Literal["actor", "writer", "director"]


class GenresByMovie(TypedDict):
    uuid: uuid.UUID
    name: str


class FilmsByPerson(TypedDict):
    uuid: uuid.UUID
    roles: list[Role]


class Movie(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    creation_date: date | None
    rating: float | None
    type: str
    last_modified: datetime


class MoviePerson(BaseModel):
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: Role
    full_name: str


class MovieGenre(BaseModel):
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    name: str
    description: str | None


class MovieElastic(BaseModel):
    title: str
    description: str | None
    imdb_rating: float | None
    genres: list[GenresByMovie]
    actors: list[dict[str, str | uuid.UUID]]
    directors: list[dict[str, str | uuid.UUID]]
    writers: list[dict[str, str | uuid.UUID]]
    uuid: uuid.UUID


class PersonElastic(BaseModel):
    full_name: str
    films: list[FilmsByPerson]
    uuid: uuid.UUID


class GenreElastic(BaseModel):
    name: str
    description: str | None
    films: list[uuid.UUID]
    uuid: uuid.UUID
