from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from api.v1.models import FullFilmQuery, FullPersonQuery, Person, ShortFilm
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service


router = APIRouter()
persons_tags_metadata = {"name": "Персоны", "description": "Получение информации по персонам"}


@router.get(
    "/",
    summary="Информация о персонах",
    description="Информация о персонах",
    response_description="Список найденных персон",
    tags=["Персоны"],
)
async def persons_list(
    person_service: Annotated[PersonService, Depends(get_person_service)],
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
) -> list[Person]:
    persons = await person_service.search(FullPersonQuery(None, page_number, page_size))
    return [Person(**person.model_dump()) for person in persons]


@router.get(
    "/{person_id}",
    summary="Информация о персоне",
    description="Полная информация о конкретной персоне",
    response_description="Полная информация по персоне",
    tags=["Персоны"],
)
async def person_details(
    person_id: Annotated[str, Path(description="ID персоны")],
    person_service: Annotated[PersonService, Depends(get_person_service)],
) -> Person:
    person = await person_service.get_by_id(person_id)
    return Person(**person.model_dump())


@router.get(
    "/{person_id}/film/",
    summary="Фильмы по персоне",
    description="Полный список фильмов по персоне",
    response_description="Список фильмов по персоне",
    tags=["Персоны"],
)
async def person_films(
    person_id: Annotated[str, Path(description="ID персоны")],
    film_service: Annotated[FilmService, Depends(get_film_service)],
    sort: Annotated[str | None, Query(description="Поле для сортировки")] = None,
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
) -> list[ShortFilm]:
    films = await film_service.search(FullFilmQuery(None, sort, page_number, page_size, None, person_id))
    return [ShortFilm(**film.model_dump()) for film in films]
