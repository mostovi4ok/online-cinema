import http
from collections.abc import Callable, Coroutine
from http.cookies import SimpleCookie
from typing import Any
from uuid import uuid4

import pytest
from aiokafka import AIOKafkaConsumer

from core.settings import test_settings


@pytest.mark.parametrize(
    "expected_answer",
    [{"status": http.HTTPStatus.OK, "length": 1}],
)
@pytest.mark.asyncio(scope="session")
async def test_confirm_email(
    profile_create_database: Callable[[], Coroutine[Any, Any, None]],
    profile_drop_database: Callable[[], Coroutine[Any, Any, None]],
    auth_create_database: Callable[[], Coroutine[Any, Any, None]],
    auth_drop_database: Callable[[], Coroutine[Any, Any, None]],
    make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
    make_get_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
    consumer: AIOKafkaConsumer,
    expected_answer: dict[str, int],
) -> None:
    # 1. Создаем таблицы в базе данных
    await consumer.seek_to_end()
    await auth_create_database()
    await profile_create_database()

    # 2.  Создаем профиль

    body, status, _ = await make_post_request(
        url=f"{test_settings.service_profile_url}api/v1/profile/",
        json={"id": str(uuid4()), "login": "as", "email": "as"},
    )

    # 3. Получаем сообщение из Kafka

    message = await consumer.getone()
    assert message.value is not None
    value = next(iter(message.value))
    assert isinstance(value, dict)
    link = value["link"]

    # 4. Подтверждаем почту

    body, status = await make_get_request(url=link)

    # 5. Проверяем ответ

    try:
        assert status == expected_answer["status"]
        assert len(body) == expected_answer["length"]

    # 6.  Стираем таблицы  в базе данных

    finally:
        await auth_drop_database()
        await profile_drop_database()
