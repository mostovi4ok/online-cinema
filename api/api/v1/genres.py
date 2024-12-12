from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from api.v1.models import FullGenreQuery, Genre
from services.genre import GenreService, get_genre_service


router = APIRouter()
genres_tags_metadata = {"name": "Жанры", "description": "Получение информации по жанрам"}


@router.get(
    "/",
    summary="Информация о жанрах",
    description="Информация о жанрах",
    response_description="Список найденных жанров",
    tags=["Жанры"],
)
async def genres_list(
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
) -> list[Genre]:
    genres = await genre_service.search(FullGenreQuery(None, page_number, page_size))
    return [Genre(**genre.model_dump()) for genre in genres]


@router.get(
    "/{genre_id}",
    summary="Информация о кинопроизведении",
    description="Полная информация о конкретном кинопроизведениям",
    response_description="Полная информация по фильму",
    tags=["Жанры"],
)
async def genre_details(
    genre_id: Annotated[str, Path(description="ID жанра")],
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    return Genre(**genre.model_dump())
