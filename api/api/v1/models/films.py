from dataclasses import dataclass
from typing import Any, TypedDict

from pydantic import BaseModel


class Genres(TypedDict):
    uuid: str
    name: str


class Person(TypedDict):
    uuid: str
    full_name: str


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None
    description: str | None
    genres: list[Genres]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


class ShortFilm(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None


@dataclass
class FullFilmQuery:
    query: str | None
    sort: str | None
    page_number: int
    page_size: int
    genre: str | None = None
    person: str | None = None

    def __post_init__(self) -> None:
        if self.sort:
            sort_instances = self.sort.split(",")
            self.sort = ""
            for instance in sort_instances:
                instance_ = instance.strip()
                self.sort += instance_[1:] + ":desc," if instance_.startswith("-") else instance_ + ","

            self.sort = self.sort.rstrip(",")

    def generate_query(self) -> dict[str, Any]:
        match self.query, self.genre, self.person:
            case str(), None, None:
                return {"match": {"title": {"query": self.query}}}
            case None, str(), None:
                return {
                    "nested": {"path": "genres", "query": {"bool": {"must": [{"match": {"genres.uuid": self.genre}}]}}}
                }
            case None, None, str():
                return {
                    "bool": {
                        "should": [
                            {
                                "nested": {
                                    "path": "actors",
                                    "query": {"bool": {"must": [{"match": {"actors.uuid": {"query": self.person}}}]}},
                                }
                            },
                            {
                                "nested": {
                                    "path": "writers",
                                    "query": {"bool": {"must": [{"match": {"writers.uuid": {"query": self.person}}}]}},
                                }
                            },
                            {
                                "nested": {
                                    "path": "directors",
                                    "query": {
                                        "bool": {"must": [{"match": {"directors.uuid": {"query": self.person}}}]}
                                    },
                                }
                            },
                        ]
                    }
                }
            case None, None, None:
                return {"match_all": {}}
            case _:
                return {"match_all": {}}
