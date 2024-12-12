import http
from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any
from uuid import uuid4

import pytest

from core.settings import test_settings
from src.models_auth import AccountModel


@pytest.mark.parametrize(
    "expected_answer",
    [{"status": http.HTTPStatus.OK, "length": 4}],
)
@pytest.mark.asyncio(scope="session")
async def test_add_reviews(
    profile_create_database: Callable[[], Coroutine[Any, Any, None]],
    profile_drop_database: Callable[[], Coroutine[Any, Any, None]],
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    login_auth: Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]],
    expected_answer: dict[str, int],
    init_mongo: None,
) -> None:
    # 1. Создаем таблицы в базе данных

    await auth_create_database()
    await profile_create_database()

    # 2. Генерируем данные

    account = AccountModel(login="login", password="password", email="email")

    # 3. Регистрируемся

    await make_post_request(url=f"{test_settings.service_auth_url}api/v1/auth/register/", json=account.model_dump())

    # 4. Логинимся

    cookies, headers = await login_auth(
        action_db=False,
        create_user=False,
        login=account.login,
        password=account.password,
        email=account.email,
    )

    # 5. Создаем ревью

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_ugc_url}api/v1/reviews/{uuid4()}",
        cookies=cookies,
        headers=headers,
        json={"review": "qwerty"},
    )

    # 6. Проверяем ответ

    try:
        assert status == expected_answer["status"]
        assert len(body) == expected_answer["length"]

    # 7. Стираем таблицы  в базе данных

    finally:
        await auth_drop_database()
        await profile_drop_database()
