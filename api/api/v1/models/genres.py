from dataclasses import dataclass

from pydantic import BaseModel


class Genre(BaseModel):
    uuid: str
    name: str
    description: str | None
    films: list[str]


@dataclass
class FullGenreQuery:
    q: str | None
    page_number: int
    page_size: int
