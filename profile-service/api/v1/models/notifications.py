from uuid import UUID

from pydantic import BaseModel, Field


class NotificationModel(BaseModel):
    notification_id: UUID = Field(description="Идентификатор уведомления", title="Идентификатор")
    message: str = Field(description="Текст уведомления", title="Уведомление")
    viewed: bool = Field(description="Прочитано", title="Прочитано")
