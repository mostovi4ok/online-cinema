from dataclasses import dataclass
from typing import TypedDict

from pydantic import BaseModel


class FilmPerson(TypedDict):
    uuid: str
    roles: list[str]


class Person(BaseModel):
    uuid: str
    full_name: str
    films: list[FilmPerson]


@dataclass
class FullPersonQuery:
    q: str | None
    page_number: int
    page_size: int
