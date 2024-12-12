from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from api.v1.models import JWTRequestModel, NotificationModel
from services.notification_service import NotificationService, get_notification_service


router = APIRouter()
notifications_tags_metadata = {
    "name": "Уведомления",
    "description": "Уведомления пользователей",
}


@router.get(
    "/",
    summary="Просмотр пользовательских уведомллений",
    description="Просмотр пользовательских уведомллений",
    response_description="Список пользовательских уведомллений",
    responses={status.HTTP_200_OK: {"model": NotificationModel}},
    tags=["Уведомления"],
)
async def get_notifications(
    request: JWTRequestModel,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
) -> list[NotificationModel]:
    return await notification_service.get_notifications(request.jwt_user.id)


@router.post(
    "/{notification_id}",
    summary="Прочтение оповещений",
    description="Прочтение оповещений",
    response_description="Статус",
    responses={status.HTTP_200_OK: {}},
    tags=["Уведомления"],
)
async def read_notifications(
    request: JWTRequestModel,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    notification_id: Annotated[UUID, Path(description="ID уведомления")],
) -> NotificationModel | None:
    return await notification_service.read_notifications(request.jwt_user.id, notification_id)
