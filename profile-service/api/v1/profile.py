from contextlib import suppress  # noqa: A005
from typing import Annotated
from uuid import UUID

from aiohttp import ClientResponseError, ClientSession
from async_fastapi_jwt_auth.auth_jwt import AuthJWT, AuthJWTBearer
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import NoResultFound

from api.v1.models import ProfileInfo, ProfileModel, ProfileUpdate
from core.config import configs
from core.request import get_aio_session
from jwt_auth_helpers import get_jwt_user_global
from services.notification_service import NotificationService, get_notification_service
from services.profile_service import ProfileService, get_profile_service
from services.redis_service import RedisService, get_redis_service


router = APIRouter()
auth_dep = AuthJWTBearer()
profile_tags_metadata = {
    "name": "Профили",
    "description": "Управление профилями пользователей",
}


@router.post(
    "/",
    summary="Добавление профиля пользователя",
    description="Добавление профиля пользователя",
    response_description="Данные профиля пользователя",
    responses={status.HTTP_201_CREATED: {"model": ProfileModel}},
    tags=["Профили"],
)
async def create_profile(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    redis: Annotated[RedisService, Depends(get_redis_service)],
    aio_session: Annotated[ClientSession, Depends(get_aio_session)],
    profile_data: Annotated[ProfileInfo, Body(description="Данные профиля")],
) -> ProfileModel:
    profile = await profile_service.create_profile(profile_data)

    link = await redis.add_email_confirmation_url(profile.id)
    try:
        async with aio_session.post(
            url=f"{configs.producer_dsn}api/v1/producer",
            params={"message_type": "api_kafka_email_confirmation"},
            json=[{"user_email": profile.email, "link": link}],
        ):
            ...
    except (OSError, ClientResponseError):
        await profile_service.delete_profile(profile_data.id)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    with suppress(OSError, ClientResponseError):
        async with aio_session.post(
            url=f"{configs.producer_dsn}api/v1/producer",
            params={"message_type": "api_kafka_notification_in_profile"},
            json=[
                {
                    "profile_id": str(profile.id),
                    "message": "Welcome! We're glad you're with us.",
                    "method_send": "profile",
                }
            ],
        ):
            ...

    return profile


@router.get(
    "/confirm_email/{link}",
    summary="Подтверждение электронной почты",
    description="Подтверждение электронной почты",
    response_description="Пользователь подтвержден",
    responses={status.HTTP_302_FOUND: {}},
    tags=["Авторизация"],
)
async def confirm_email(
    link: Annotated[UUID, Path(description="Ссылка подтверждения")],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    redis: Annotated[RedisService, Depends(get_redis_service)],
) -> RedirectResponse:
    if not (user_id := await redis.get_email_confirmation(link)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        await profile_service.confirm_email(user_id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return RedirectResponse(configs.email_confirmation_redirect, status_code=302)


@router.get(
    "/",
    summary="Просмотр профиля пользователя",
    description="Просмотр профиля пользователя",
    response_description="Данные профиля пользователя",
    responses={status.HTTP_200_OK: {"model": ProfileModel}},
    tags=["Профили"],
    dependencies=[Depends(get_jwt_user_global)],
)
async def get_profile(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ProfileModel:
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    return await profile_service.get_profile(user_id)


@router.patch(
    "/",
    summary="Изменение профиля пользователя",
    description="Изменение профиля пользователя",
    response_description="Новые данные профиля",
    responses={status.HTTP_200_OK: {"model": ProfileModel}},
    tags=["Профили"],
    dependencies=[Depends(get_jwt_user_global)],
)
async def update_profile(
    request: Request,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    new_data: Annotated[ProfileUpdate, Body(description="Данные профиля")],
) -> ProfileModel:
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    return await profile_service.update_profile(user_id, new_data)


@router.delete(
    "/",
    summary="Удаление профиля пользователя",
    description="Удаление профиля пользователя",
    response_description="Подтверждение удаления профиля пользователя",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Профили"],
    dependencies=[Depends(get_jwt_user_global)],
)
async def delete_profile(
    request: Request,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    aio_session: Annotated[ClientSession, Depends(get_aio_session)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
) -> str:
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    try:
        for link in (
            f"{configs.ugc_dsn}api/v1/favourites/",
            f"{configs.ugc_dsn}api/v1/ratings/",
            f"{configs.ugc_dsn}api/v1/reviews/",
            f"{configs.auth_dsn}api/v1/auth/delete",
        ):
            async with aio_session.delete(url=link, headers=request.headers, cookies=request.cookies):
                ...
    except (OSError, ClientResponseError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    await notification_service.delete_all_notifications(user_id)
    return await profile_service.delete_profile(user_id)
