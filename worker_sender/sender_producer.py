from typing import Any

import backoff
from aiohttp import ClientResponseError, ClientSession, ClientTimeout

from configs.settings import settings


LEN_REQUEST = 1000

logger = settings.logger


@backoff.on_exception(backoff.expo, OSError)
async def sender_producer(messages: Any, message_type: str) -> bool:
    async with (
        ClientSession(f"{settings.producer_dsn}") as session,
        session.post(
            "/api/v1/producer",
            params={"message_type": message_type},
            json=messages,
            timeout=ClientTimeout(connect=3, sock_read=10),
        ) as response,
    ):
        try:
            response.raise_for_status()
        except ClientResponseError:
            return False

        return True
