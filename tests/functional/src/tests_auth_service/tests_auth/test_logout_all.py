from collections.abc import Callable, Coroutine
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_auth import AccountModel, LoginModel
from test_fixtures.password import Password
from testdata.auth_db_model import User


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"name": "login", "password": "password", "iters": 5},
            {"status": (HTTPStatus.OK, HTTPStatus.UNAUTHORIZED), "length": (None, 1)},
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_logout_all(
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    auth_pg_session: AsyncSession,
    compute_hash: Callable[..., Coroutine[Any, Any, Password]],
    query_data: dict[str, str | int],
    expected_answer: dict[str, tuple[int, int]],
) -> None:
    # 1. Создаем таблицы в базе данных

    await auth_create_database()

    # 2. Генерируем данные

    password = await compute_hash(query_data["password"])

    login = LoginModel(login=query_data["name"], password=query_data["password"])

    account = AccountModel(login=query_data["name"], password=password, email="email")

    # 3. Создаем пользователя в бд

    auth_pg_session.add(User(**account.model_dump()))
    await auth_pg_session.commit()

    # 4. Логинимся

    cookies: list[SimpleCookie] = []
    for _ in range(query_data["iters"]):
        _, _, cookie = await make_post_request(
            url=f"{test_settings.service_auth_url}api/v1/auth/login/",
            json=login.model_dump(),
            headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
        )
        cookies.append(cookie)

    # 5. Разлогиниваемся

    body, status = await make_get_request(
        url=f"{test_settings.service_auth_url}api/v1/auth/logout_all/", cookies=cookies[0]
    )

    # 6. Проверяем ответ

    assert status == expected_answer["status"][0]
    assert body is expected_answer["length"][0]

    # 7. Пробуем разлогиниться с другими куками

    body, status = await make_get_request(
        url=f"{test_settings.service_auth_url}api/v1/auth/logout_all/", cookies=cookies[-1]
    )

    # 6. Проверяем ответ
    try:
        assert status == expected_answer["status"][1]
        assert len(body) == expected_answer["length"][1]
    finally:
        # 7. Стираем таблицы  в базе данных

        await auth_drop_database()
