import http
from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any
from uuid import uuid4

import pytest

from core.settings import test_settings


@pytest.mark.parametrize(
    "expected_answer",
    [{"status": http.HTTPStatus.OK, "lenth": 5}],
)
@pytest.mark.asyncio(scope="session")
async def test_create_profile(
    profile_create_database: Callable[[], Coroutine[Any, Any, None]],
    profile_drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных
    await profile_create_database()

    # 2.  Создаем профиль

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_profile_url}api/v1/profile/",
        json={"id": str(uuid4()), "login": "as", "email": "as"},
    )

    # 3. Проверяем ответ

    try:
        assert status == expected_answer["status"]
        assert len(body) == expected_answer["lenth"]
    finally:
        # 4. Стираем таблицы  в базе данных

        await profile_drop_database()
