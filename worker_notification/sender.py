from collections import defaultdict
from typing import Any

import backoff
from aiohttp import ClientResponseError, ClientSession, ClientTimeout

from configs.settings import settings


LEN_REQUEST = 1000


async def pack_and_send(messages: dict[str, list[dict[str, Any]]]) -> defaultdict[str, list[tuple[bool, int, int]]]:
    result: defaultdict[str, list[tuple[bool, int, int]]] = defaultdict(list)
    for message_type, message in messages.items():
        if (len_message := len(message)) < LEN_REQUEST:
            result[message_type].append((
                await sender(message, message_type),
                0,
                LEN_REQUEST,
            ))
        else:
            count = len_message // LEN_REQUEST + len_message % LEN_REQUEST

            for num in range(count):
                start = LEN_REQUEST * num
                end = start + LEN_REQUEST
                result[message_type].append((
                    await sender(message[start:end], message_type),
                    start,
                    end,
                ))

    return result


@backoff.on_exception(backoff.expo, OSError)
async def sender(messages: Any, message_type: str) -> bool:
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
