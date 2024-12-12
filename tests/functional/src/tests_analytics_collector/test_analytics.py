from collections.abc import Callable, Coroutine
from http import HTTPStatus
from http.cookies import SimpleCookie
from typing import Any

import pytest

from core.settings import test_settings
from testdata.analytics import CHANGE_QUAL_DATA, CLICK_DATA, FILMTIME_DATA, SEARCH_DATA, URLTIME_DATA


@pytest.mark.parametrize(
    ("data", "message_type", "status_answer"),
    [
        (URLTIME_DATA, "api_kafka_urltime", HTTPStatus.OK),
        (CHANGE_QUAL_DATA, "api_kafka_change_qual", HTTPStatus.OK),
        (FILMTIME_DATA, "api_kafka_moviestop", HTTPStatus.OK),
        (SEARCH_DATA, "api_kafka_filter", HTTPStatus.OK),
        (CLICK_DATA[0:2], "api_kafka_click", HTTPStatus.OK),
        (CLICK_DATA[0:2], "bad_type", HTTPStatus.BAD_REQUEST),
        (CLICK_DATA[0:1001], "api_kafka_click", HTTPStatus.REQUEST_ENTITY_TOO_LARGE),
        (CLICK_DATA[1002], "api_kafka_click", HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_analytics(
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    login_auth: Callable[..., Coroutine[Any, Any, tuple[SimpleCookie, dict[str, str]]]],
    data: list[Any],
    message_type: str,
    status_answer: int,
) -> None:
    cookies, headers = await login_auth()

    _, status, _ = await make_post_request(
        url=f"{test_settings.service_analytics_collector_url}/api/v1/analytics",
        json=data,
        params={"message_type": message_type},
        headers=headers,
        cookies=cookies,
    )
    assert status == status_answer
