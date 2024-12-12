from datetime import datetime
from functools import lru_cache
from uuid import UUID

from api.v1.models import NotificationModel
from models.mongo_models import ProfileBell


class NotificationService:
    async def get_notifications(self, user_id: UUID) -> list[NotificationModel]:
        notifications = await ProfileBell.find_many(ProfileBell.profile_id == user_id).to_list()
        return [NotificationModel.model_validate(notification.model_dump()) for notification in notifications]

    async def read_notifications(self, user_id: UUID, notification_id: UUID) -> NotificationModel | None:
        notification = await ProfileBell.find_one(
            ProfileBell.profile_id == user_id, ProfileBell.notification_id == notification_id
        )
        if notification is not None:
            notification.viewed = True
            notification.viewed_at = datetime.now()
            await notification.save()
            return NotificationModel.model_validate(notification.model_dump())

    async def delete_all_notifications(self, user_id: str | int | UUID | None) -> None:
        await ProfileBell.find_many(ProfileBell.profile_id == user_id).delete()


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
