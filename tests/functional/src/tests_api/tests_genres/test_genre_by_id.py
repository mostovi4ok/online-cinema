import http
import uuid
from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any

import pytest

from core.settings import test_settings
from src.models_api import Genre


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        ("ef86b8ff-3c82-4d31-ad8e-72b69f4e3f9w", {"status": http.HTTPStatus.OK, "length": 4}),
        ("qwerty", {"status": http.HTTPStatus.BAD_REQUEST, "length": 1}),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_genre_by_id(
    es_write_data: Callable[..., Coroutine[Any, Any, None]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    es_clear_data: Callable[..., Coroutine[Any, Any, None]],
    login_auth: Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]],
    query_data: dict[str, str],
    expected_answer: dict[str, int],
) -> None:
    # 0. Логинимся

    cookies, headers = await login_auth()

    # 1. Генерируем данные для ES

    es_films = [
        Genre(
            uuid="ef86b8ff-3c82-4d31-ad8e-72b69f4e3f9w",
            description="Action",
            name="Action",
            films=[str(uuid.uuid4()) for _ in range(5)],
        ).model_dump()
    ]
    bulk_query_films: list[dict[str, Any]] = []
    for row in es_films:
        data: dict[str, Any] = {"_index": test_settings.es_index_genres, "_id": row[test_settings.es_id_field]}
        data.update({"_source": row})
        bulk_query_films.append(data)

    # 2. Загружаем данные в ES

    await es_write_data(bulk_query_films, test_settings.es_index_genres, test_settings.es_index_mapping_genres)

    # 3. Запрашиваем данные из ES по API

    body, status = await make_get_request(
        url=f"{test_settings.service_api_url}api/v1/genres/{query_data}", cookies=cookies, headers=headers
    )

    # 4. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]

    # 5. Очищаем данные в ES

    await es_clear_data((test_settings.es_index_genres,))

    # 6. Запрашиваем данные из Redis по API

    body, status = await make_get_request(
        url=f"{test_settings.service_api_url}api/v1/genres/{query_data}", cookies=cookies, headers=headers
    )

    # 7. Проверяем ответ

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]
