from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any
from uuid import UUID, uuid4

import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.settings import test_settings
from src.models_auth import LoginModel
from test_fixtures.password import Password
from testdata.auth_db_model import Right, User


@pytest_asyncio.fixture(name="login_auth")
def login_auth(
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    auth_pg_session: AsyncSession,
    compute_hash: Callable[..., Coroutine[Any, Any, Password]],
) -> Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]]:
    async def inner(
        action_db: bool = True,
        create_user: bool = True,
        login: str = "login",
        password: str = "password",
        email: str = "email_assign",
        id_: UUID = uuid4(),
    ) -> tuple[SimpleCookie, dict[str, str]]:
        if action_db:
            await auth_create_database()

        if create_user:
            right = Right(name="subscriber")
            auth_pg_session.add(right)
            auth_pg_session.add(
                User(
                    id=id_,
                    login=login,
                    password=await compute_hash(password),
                    email=email,
                    rights=[right],
                )
            )
            await auth_pg_session.commit()

        _, _, cookies = await make_post_request(
            url=f"{test_settings.service_auth_url}api/v1/auth/login/",
            json=LoginModel(login=login, password=password).model_dump(),
        )

        if action_db:
            await auth_drop_database()

        headers = {
            "cookie": (
                f"access_token_cookie={cookies.get("access_token_cookie").value}; "
                f"refresh_token_cookie={cookies.get("refresh_token_cookie").value}"
            )
        }
        return cookies, headers

    return inner
