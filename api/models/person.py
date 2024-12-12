from typing import TypedDict

from pydantic import BaseModel


class FilmPerson(TypedDict):
    uuid: str
    roles: list[str]


class Person(BaseModel):
    uuid: str
    full_name: str
    films: list[FilmPerson]
