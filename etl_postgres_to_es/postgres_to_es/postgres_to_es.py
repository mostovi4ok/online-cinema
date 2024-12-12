import uuid
from collections import defaultdict
from collections.abc import Iterable, Mapping
from datetime import datetime
from typing import Any

import psycopg
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from querys import QUERY_GENRE, QUERY_MOVIE, QUERY_PERSON
from state.schemes import GenreElastic, GenresByMovie, Movie, MovieElastic, MovieGenre, MoviePerson, PersonElastic, Role
from state.state import State
from state.storage import STATE_KEY


def fetch_changed_data(cursor: psycopg.Cursor[Any], last_modified: datetime) -> Iterable[list[Movie]]:
    cursor.execute(QUERY_MOVIE, {STATE_KEY: last_modified})
    while results := cursor.fetchmany(size=100):
        yield [Movie(**movie_dict) for movie_dict in results]


def get_movies_elastic(
    movies: list[Movie],
    data_movie_persons: Mapping[uuid.UUID, Mapping[Role, list[MoviePerson]]],
    data_movie_genres: Mapping[uuid.UUID, list[GenresByMovie]],
) -> list[MovieElastic]:
    return [
        MovieElastic(
            uuid=movie.id,
            imdb_rating=movie.rating,
            genres=data_movie_genres[movie.id],
            title=movie.title,
            description=movie.description,
            actors=[
                {"uuid": person.person_id, "full_name": person.full_name}
                for person in data_movie_persons[movie.id]["actor"]
            ],
            directors=[
                {"uuid": person.person_id, "full_name": person.full_name}
                for person in data_movie_persons[movie.id]["director"]
            ],
            writers=[
                {"uuid": person.person_id, "full_name": person.full_name}
                for person in data_movie_persons[movie.id]["writer"]
            ],
        )
        for movie in movies
    ]


def get_persons_elastic(
    data_movie_person_films: Mapping[uuid.UUID, Mapping[uuid.UUID, list[Role]]],
    data_movie_person_name: Mapping[uuid.UUID, str],
) -> dict[uuid.UUID, PersonElastic]:
    return {
        person_id: PersonElastic(
            uuid=person_id,
            full_name=data_movie_person_name[person_id],
            films=[
                {"uuid": film_work_id, "roles": roles}
                for film_work_id, roles in data_movie_person_films[person_id].items()
            ],
        )
        for person_id in data_movie_person_films
    }


def get_genres_elastic(
    movie_genres: list[MovieGenre], data_movie_genre_films: Mapping[uuid.UUID, list[uuid.UUID]]
) -> dict[uuid.UUID, GenreElastic]:
    return {
        genre.genre_id: GenreElastic(
            uuid=genre.genre_id,
            name=genre.name,
            description=genre.description,
            films=data_movie_genre_films[genre.genre_id],
        )
        for genre in movie_genres
    }


def transform_pg_to_es(
    objects: Iterable[list[Movie]], cursor_person: psycopg.Cursor[Any], cursor_genre: psycopg.Cursor[Any]
) -> Iterable[tuple[str, list[MovieElastic], dict[uuid.UUID, PersonElastic], dict[uuid.UUID, GenreElastic]]]:
    for movies in objects:
        id_movies = [movie.id for movie in movies]

        cursor_person.execute(QUERY_PERSON, [id_movies])
        data_movie_persons: defaultdict[uuid.UUID, defaultdict[Role, list[MoviePerson]]] = defaultdict(
            lambda: defaultdict(list)
        )
        data_movie_person_films: defaultdict[uuid.UUID, defaultdict[uuid.UUID, list[Role]]] = defaultdict(
            lambda: defaultdict(list)
        )
        data_movie_person_name: dict[uuid.UUID, str] = {}
        for movie_person in [MoviePerson(**person) for person in cursor_person.fetchall()]:
            data_movie_persons[movie_person.film_work_id][movie_person.role].append(movie_person)
            data_movie_person_films[movie_person.person_id][movie_person.film_work_id].append(movie_person.role)
            data_movie_person_name[movie_person.person_id] = movie_person.full_name

        cursor_genre.execute(QUERY_GENRE, [id_movies])
        data_movie_genres: defaultdict[uuid.UUID, list[GenresByMovie]] = defaultdict(list)
        data_movie_genre_films: defaultdict[uuid.UUID, list[uuid.UUID]] = defaultdict(list)
        movie_genres = [MovieGenre(**genre) for genre in cursor_genre.fetchall()]
        for movie_genre in movie_genres:
            data_movie_genres[movie_genre.film_work_id].append({"uuid": movie_genre.genre_id, "name": movie_genre.name})
            data_movie_genre_films[movie_genre.genre_id].append(movie_genre.film_work_id)

        movies_elastic = get_movies_elastic(movies, data_movie_persons, data_movie_genres)
        persons_elastic = get_persons_elastic(data_movie_person_films, data_movie_person_name)
        genres_elastic = get_genres_elastic(movie_genres, data_movie_genre_films)

        yield (movies[-1].last_modified.isoformat(), movies_elastic, persons_elastic, genres_elastic)


def save_movies(client: Elasticsearch, movies: list[MovieElastic]) -> None:
    bulk(client, [{"_index": "movies", "_id": f"{obj.uuid}", **obj.model_dump()} for obj in movies])


def save_persons(client: Elasticsearch, persons: dict[uuid.UUID, PersonElastic]) -> None:
    saved_persons: dict[uuid.UUID, PersonElastic] = {
        uuid.UUID(obj["_source"]["uuid"]): PersonElastic(
            full_name=obj["_source"]["full_name"], films=obj["_source"]["films"], uuid=obj["_source"]["uuid"]
        )
        for obj in client.search(
            index="persons", body={"query": {"ids": {"values": list(persons.keys())}}}, size=len(persons)
        )["hits"]["hits"]
    }
    for id_person, person in persons.items():
        if id_person in saved_persons:
            person.films.extend(saved_persons[id_person].films)
            conv: defaultdict[uuid.UUID, set[Role]] = defaultdict(set)
            for obj in person.films:
                conv[obj["uuid"]].update(obj["roles"])

            persons[id_person].films = [{"uuid": idx, "roles": list(roles)} for idx, roles in conv.items()]

    bulk(
        client,
        [{"_index": "persons", "_id": f"{obj.uuid}", **obj.model_dump()} for obj in persons.values()],
        refresh="wait_for",
    )


def save_genres(client: Elasticsearch, genres: dict[uuid.UUID, GenreElastic]) -> None:
    saved_genres: dict[uuid.UUID, GenreElastic] = {
        uuid.UUID(obj["_source"]["uuid"]): GenreElastic(
            name=obj["_source"]["name"],
            description=obj["_source"]["description"],
            films=obj["_source"]["films"],
            uuid=obj["_source"]["uuid"],
        )
        for obj in client.search(
            index="genres", body={"query": {"ids": {"values": list(genres.keys())}}}, size=len(genres)
        )["hits"]["hits"]
    }
    for id_genre, genre in genres.items():
        if id_genre in saved_genres:
            genre.films.extend(saved_genres[id_genre].films)
            genres[id_genre].films = list(set(genre.films))

    bulk(
        client,
        [{"_index": "genres", "_id": f"{obj.uuid}", **obj.model_dump()} for obj in genres.values()],
        refresh="wait_for",
    )


def save_in_es(
    data: Iterable[tuple[str, list[MovieElastic], dict[uuid.UUID, PersonElastic], dict[uuid.UUID, GenreElastic]]],
    state: State,
    client: Elasticsearch,
) -> None:
    for last_modified, movies, persons, genres in data:
        save_movies(client, movies)
        save_persons(client, persons)
        save_genres(client, genres)

        state.set_state(STATE_KEY, last_modified)
