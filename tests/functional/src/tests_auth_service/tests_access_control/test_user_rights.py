from collections.abc import Callable, Coroutine
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_access_control import UserModel
from src.models_auth import AccountModel, LoginModel
from test_fixtures.password import Password
from testdata.auth_db_model import Right, User


@pytest.mark.parametrize(
    ("query_data", "expected_answer"),
    [
        (
            {"name": "admin", "right": "admin", "password": "password", "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
            {"status": HTTPStatus.OK, "length": 1},
        ),
        (
            {"name": "qwerty", "right": "qwerty", "password": "password", "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
            {"status": HTTPStatus.FORBIDDEN, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_user_rights(
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    auth_pg_session: AsyncSession,
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    compute_hash: Callable[..., Coroutine[Any, Any, Password]],
    query_data: dict[str, str | UUID],
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных

    await auth_create_database()

    # 2. Генерируем данные

    password = await compute_hash(query_data["password"])

    login = LoginModel(login=query_data["name"], password=query_data["password"])

    account = AccountModel(login=query_data["name"], password=password, email="email")
    right = Right(name=query_data["right"])

    user = User(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        login="login_assign",
        password=password,
        email="email_assign",
        rights=[right],
    )

    user_resp = UserModel(id=query_data["id"])

    # 3. Создаем данные в бд

    if query_data["right"] != "admin":
        auth_pg_session.add(Right(name="admin"))

    auth_pg_session.add(right)
    auth_pg_session.add(user)
    auth_pg_session.add(User(**account.model_dump(), rights=[right]))
    await auth_pg_session.commit()

    # 4. Логинимся

    _, _, cookies = await make_post_request(
        url=f"{test_settings.service_auth_url}api/v1/auth/login/",
        json=login.model_dump(),
        headers={"user-agent": "test", "sec-ch-ua-platform": "test"},
    )

    # 5. Получаем список прав через api

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_auth_url}api/v1/access_control/rights/get_user_rights/",
        json=user_resp.model_dump(mode="json"),
        cookies=cookies,
    )

    # 6. Проверяем ответ
    try:
        assert status == expected_answer["status"]
        assert len(body) == expected_answer["length"]
    finally:
        # 7. Стираем таблицы  в базе данных

        await auth_drop_database()
