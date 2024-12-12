import http
from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any

import pytest

from core.settings import test_settings


@pytest.mark.parametrize(
    "expected_status",
    [http.HTTPStatus.NO_CONTENT],
)
@pytest.mark.asyncio(scope="session")
async def test_delete(
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    login_auth: Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]],
    make_delete_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    expected_status: int,
) -> None:
    await auth_create_database()

    cookies, headers = await login_auth(action_db=False)

    _, status, _ = await make_delete_request(
        url=f"{test_settings.service_auth_url}api/v1/auth/delete",
        headers=headers,
        cookies=cookies,
    )

    try:
        assert status == expected_status
    finally:
        await auth_drop_database()
