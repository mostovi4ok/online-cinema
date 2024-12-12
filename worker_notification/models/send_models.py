from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SendEmail(BaseModel):
    notification_id: UUID = Field(default_factory=uuid4)
    subject: str
    content: str
    recipient_variables: dict[str, dict[str, str | int]]
