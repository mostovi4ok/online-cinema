from typing import Any
from uuid import UUID

from pydantic import BaseModel


type Task = EmailTask


class BaseTask(BaseModel):
    key: str | None = None
    key_dlq: str | None = None
    value: Any | None = None

    notification_id: UUID


class EmailTask(BaseTask):
    subject: str
    content: str
    recipient_variables: dict[str, dict[str, str | int]]
