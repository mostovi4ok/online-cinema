import json
from typing import TYPE_CHECKING
from uuid import UUID

import backoff
from aiohttp import BasicAuth, ClientSession, ClientTimeout

from configs.settings import settings
from mongo_db import State
from sender_producer import sender_producer


if TYPE_CHECKING:
    from models import Task


logger = settings.logger


async def send_email(tasks: list["Task"]) -> None:
    for task in tasks:
        if (state := await State.find_one(State.notification_id == task.notification_id)) is None or state.send:
            continue

        assert task.key_dlq is not None
        if not (await sender_emails(task.recipient_variables, task.subject, task.content, task.notification_id)):
            await sender_producer(
                [{"subject": task.subject, "content": task.content, "recipient_variables": task.recipient_variables}],
                task.key_dlq,
            )


@backoff.on_exception(backoff.expo, OSError)
async def sender_emails(
    recipients: dict[str, dict[str, str | int]], subject: str, message: str, notification_id: UUID
) -> bool:
    to_address = list(recipients.keys())

    logger.info(f"Отправляем {len(to_address)} писем...")

    async with (
        ClientSession() as session,
        session.post(
            url=settings.mailgun_api_url,
            auth=BasicAuth(login="api", password=settings.mailgun_api_key),
            data={
                "from": settings.from_email_address,
                "to": to_address,
                "subject": subject,
                "text": message,
                "recipient-variables": json.dumps(recipients),
            },
            timeout=ClientTimeout(connect=3, sock_read=10),
        ) as response,
    ):
        if response.status == 200:
            logger.info(f"Электронное письмо успешно отправлено получателям {to_address} через API Mailgun.")

            if (state := await State.find_one(State.notification_id == notification_id)) is not None:
                state.send = True
                await state.save()

            return True

        logger.error(
            f"Не удалось отправить электронные письма получателям {to_address}, причина: {await response.text()}"
        )
        return False
