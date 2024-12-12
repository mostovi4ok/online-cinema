from typing import Annotated, cast
from uuid import UUID

from aiohttp import ClientResponseError, ClientSession
from async_fastapi_jwt_auth.auth_jwt import AuthJWT, AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response

from api.v1.models import (
    AccountHistoryModel,
    AccountModel,
    ActualTokensModel,
    ChangePasswordModel,
    HistoryModel,
    LoginModel,
    RightsAccountModel,
    SecureAccountModel,
)
from core.config import configs
from core.request import get_aio_session
from models.alchemy_model import Action
from services.password_service import Password, PasswordService, get_password_service
from services.redis_service import RedisService, get_redis
from services.rights_management_service import RightsManagementService, get_rights_management_service
from services.user_service import UserService, get_user_service


router = APIRouter()
auth_dep = AuthJWTBearer()
auth_tags_metadata = {"name": "Авторизация", "description": "Авторизация в API."}


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя",
    response_description="Пользователь зарегистрирован",
    responses={status.HTTP_200_OK: {"model": AccountModel}},
    tags=["Авторизация"],
)
async def register(
    request: Request,
    data: AccountModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
    aio_session: Annotated[ClientSession, Depends(get_aio_session)],
) -> SecureAccountModel:
    # Проверка наличия обязательных данных
    if not data.login:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Нужен логин")

    if not data.email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Нужна почта")

    # Проверки на уникальность введённых данных
    if await user_service.get_user(data.login):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Логин уже занят")

    if await user_service.get_user_by_email(data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Почта уже занята")

    # Создание пользователя
    user = await user_service.create_user(data)
    # Создание ссылки подтверждения
    try:
        # Отправка запроса в Profile на создание профиля
        async with aio_session.post(
            url=f"{configs.profile_dsn}api/v1/profile/",
            json={
                "id": str(user.id),
                "login": user.login,
                "email": user.email,
            },
            headers={"X-Request-Id": request.headers.get("X-Request-Id", "")},
        ):
            ...
    except (OSError, ClientResponseError):
        await user_service.delete_user(user)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return SecureAccountModel(**user.__dict__)


@router.post(
    "/change_password",
    summary="Изменение пароля",
    description="Изменение пароля",
    response_description="Пароль изменён",
    responses={status.HTTP_200_OK: {}, status.HTTP_401_UNAUTHORIZED: {}},
    tags=["Авторизация"],
)
async def change_password(
    request: Request,
    data: ChangePasswordModel,
    redis: Annotated[RedisService, Depends(get_redis)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> Response:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Проверить введённый старый пароль
    if not (user := await user_service.get_user_by_id(str(user_id))) or not password_service.check_password(
        data.old_password, Password(*user.password)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль или аккаунт удалён")

    # Смена пароля
    await user_service.change_password(user, data.new_password)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизация пользователя",
    response_description="Пользователь авторизован",
    responses={status.HTTP_200_OK: {"model": ActualTokensModel}, status.HTTP_401_UNAUTHORIZED: {}},
    tags=["Авторизация"],
)
async def login(
    request: Request,
    data: LoginModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
    rights_management_service: Annotated[RightsManagementService, Depends(get_rights_management_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> RightsAccountModel:
    # Обновление всех прав в Redis
    await rights_management_service.get_all()
    # Проверить введённые данные
    if not (user := await user_service.get_user(data.login)) or not password_service.check_password(
        data.password, Password(*user.password)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

    # Сгеренить новые токены
    access_token = await authorize.create_access_token(subject=str(user.id))
    refresh_token = await authorize.create_refresh_token(subject=access_token)
    # Записать рефреш-токен в Redis
    await redis.add_valid_refresh(user.id, refresh_token, access_token)
    # Записать права в Redis
    await redis.add_user_right(user.id, [right.id for right in user.rights])
    # Записать логин в БД
    await user_service.save_history(
        HistoryModel(
            user_id=user.id,
            ip_address=request.client.host if request.client else "",
            action=Action.LOGIN,
            browser_info=request.headers.get("user-agent", ""),
            system_info=request.headers.get("sec-ch-ua-platform", ""),
        )
    )
    # Отдать токены
    await authorize.set_access_cookies(access_token)
    await authorize.set_refresh_cookies(refresh_token)
    return RightsAccountModel.model_validate(user)


@router.post(
    "/refresh",
    summary="Обновление токенов",
    description="Обновление токенов",
    response_description="Токены обновлены",
    responses={status.HTTP_200_OK: {"model": ActualTokensModel}},
    tags=["Авторизация"],
)
async def refresh(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> ActualTokensModel:
    # Проверка токена на корректность и просрочку
    await authorize.jwt_refresh_token_required()
    # Вытащить Access токен из Refresh
    current_access_token = await authorize.get_jwt_subject()
    # Достать из Access информацию по юзеру
    try:
        # Изменить допустимую просрочку на срок годности Refresh токена
        authorize._decode_leeway = authorize._refresh_token_expires
        access_token_data = await authorize._verified_token(current_access_token)
    finally:
        # Вернуть допустимую просрочку к 0 в любом сценарии
        authorize._decode_leeway = 0

    user_id = cast(UUID, access_token_data.get("sub"))
    # Проверить Refresh на logout
    if not await redis.check_valid_refresh(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Сгенерить новые токены
    new_access_token = await authorize.create_access_token(subject=user_id)
    new_refresh_token = await authorize.create_refresh_token(subject=new_access_token)
    # Удалить старый рефреш
    await redis.delete_refresh(user_id, authorize._token)
    # Добавить новый рефреш
    await redis.add_valid_refresh(user_id, new_refresh_token, new_access_token)
    # Добавить старый аксес (как блокировка)
    await redis.add_banned_access(user_id, str(current_access_token), str(user_id))
    # Отдать новые токены
    await authorize.set_access_cookies(new_access_token)
    await authorize.set_refresh_cookies(new_refresh_token)
    return ActualTokensModel(access_token=new_access_token, refresh_token=new_refresh_token)


@router.get(
    "/logout",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def logout(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> None:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    access_token = authorize._token
    user_id = await authorize.get_jwt_subject()
    # Достать refresh
    await authorize.jwt_refresh_token_required()
    refresh_token = authorize._token
    # Удалить рефреш из Redis
    await redis.delete_refresh(user_id, refresh_token)
    # Добавить аксес в Redis (как блокировка)
    await redis.add_banned_access(user_id, access_token, user_id)
    # Отдать ответ о выходе из системы
    await authorize.unset_jwt_cookies()


@router.get(
    "/logout_all",
    summary="Выход из системы",
    description="Выход из системы",
    response_description="Пользователь вышел из системы",
    tags=["Авторизация"],
)
async def logout_all(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> None:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Удалить все рефреш из Redis и достать все Access
    all_user_access_tokens = await redis.delete_all_refresh(user_id)
    # Добавить все аксесы в Redis (как блокировка)
    for token in all_user_access_tokens:
        await redis.add_banned_access(user_id, token, user_id)

    # Отдать ответ о выходе из системы
    await authorize.unset_jwt_cookies()


@router.delete(
    "/delete",
    summary="Удаление аккаунта",
    description="Удаление аккаунта",
    response_description="Аккаунт удалён",
    responses={status.HTTP_204_NO_CONTENT: {}},
    tags=["Авторизация"],
)
async def delete(
    request: Request,
    redis: Annotated[RedisService, Depends(get_redis)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
) -> Response:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Найти аккаунт в БД
    user = await user_service.get_user_by_id(str(user_id))
    if user:
        # Удалить аккаунт в БД
        await user_service.delete_user(user)

    # Удалить все рефреш из Redis и достать все Access
    all_user_access_tokens = await redis.delete_all_refresh(user_id)
    # Добавить все аксесы в Redis (как блокировка)
    for token in all_user_access_tokens:
        await redis.add_banned_access(user_id, token, user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/history",
    summary="Получение истории входов в аккаунт",
    description="Получение истории входов в аккаунт",
    response_description="История входов в аккаунт получена",
    responses={status.HTTP_200_OK: {"model": list[AccountHistoryModel]}},
    tags=["Авторизация"],
)
async def history(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    redis: Annotated[RedisService, Depends(get_redis)],
    authorize: Annotated[AuthJWT, Depends(auth_dep)],
    page_number: Annotated[int, Query(description="Номер страницы для пагинации", ge=1)] = 1,
    page_size: Annotated[int, Query(description="Размер страницы для пагинации", ge=1)] = 10,
) -> list[AccountHistoryModel]:
    # Проверить токен на корректность и просрочку
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    # Проверить Access на logout
    if await redis.check_banned_access(user_id, authorize._token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Получить историю входов в аккаунт из БД
    user_login_history = await user_service.get_user_login_history(user_id, page_number, page_size)
    # Отдать историю входов в аккаунт
    return [AccountHistoryModel(**history.__dict__) for history in user_login_history]
