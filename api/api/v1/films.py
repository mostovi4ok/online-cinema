from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from api.v1.models import Film, FullFilmQuery, ShortFilm
from core.config import configs
from jwt_auth_helpers import rights_required
from services.film import FilmService, get_film_service


router = APIRouter()
films_tags_metadata = {"name": "Фильмы", "description": "Получение информации по фильмам"}


@router.get(
    "/",
    summary="Информация о кинопроизведениях",
    description="Краткая информация о кинопроизведениях с фильтрами",
    response_description="Список найденных по фильтру фильмов",
    tags=["Фильмы"],
)
async def films_list(
    film_service: Annotated[FilmService, Depends(get_film_service)],
    sort: Annotated[str | None, Query(description="Поле для сортировки")] = None,
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
    genre: Annotated[str | None, Query(description="Жанр искомых фильмов")] = None,
) -> list[ShortFilm]:
    films = await film_service.search(FullFilmQuery(None, sort, page_number, page_size, genre))
    return [ShortFilm(**film.model_dump()) for film in films]


@router.get(
    "/{film_id}",
    summary="Информация о кинопроизведении",
    description="Полная информация о конкретном кинопроизведениям",
    response_description="Полная информация по фильму",
    tags=["Фильмы"],
)
@rights_required({configs.subscriber_right_name})
async def film_details(
    request: Request,
    film_id: Annotated[str, Path(description="ID фильма")],
    film_service: Annotated[FilmService, Depends(get_film_service)],
) -> Film:
    film = await film_service.get_by_id(film_id)
    return Film(**film.model_dump())


@router.get(
    "/search/",
    summary="Поиск кинопроизведений",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="Название и рейтинг фильма",
    tags=["Фильмы"],
)
async def film_search(
    film_service: Annotated[FilmService, Depends(get_film_service)],
    query: Annotated[str | None, Query(description="Текст для поиска")] = None,
    sort: Annotated[str | None, Query(description="Поле для сортировки")] = None,
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
) -> list[ShortFilm]:
    films = await film_service.search(FullFilmQuery(query, sort, page_number, page_size))
    return [ShortFilm(**film.model_dump()) for film in films]
