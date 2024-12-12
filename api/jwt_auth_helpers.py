from collections.abc import Callable, Collection, Coroutine
from functools import wraps
from typing import Annotated, Any, ParamSpec, TypeVar, cast
from uuid import UUID

from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

from api.v1.models import JWTUserModel
from db.redis import RedisService, get_redis


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def rights_required(
    required_rights_names_list: Collection[str],
) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, Coroutine[Any, Any, F_Return]]]:
    def decorator(function: Callable[F_Spec, Any]) -> Callable[F_Spec, Coroutine[Any, Any, F_Return]]:
        @wraps(function)
        async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            # Доствём ранее положенные данные из запроса
            user = cast(JWTUserModel, kwargs.get("request").jwt_user)  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue, reportUnknownMemberType]
            # Проверяем, что текущий пользователь имеет все требуемые права
            if not user or any(right not in user.rights for right in required_rights_names_list):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

            return await function(*args, **kwargs)

        return wrapper

    return decorator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, request: Request, redis_service: Annotated[RedisService, Depends(get_redis)]
    ) -> JWTUserModel:
        authorize = AuthJWT(req=request)
        # Достаём Access Token и проверяем его на коректность
        await authorize.jwt_optional()
        # Получаем идентификатор текущего пользователя из Access Token'а
        user_id = cast(str | None, await authorize.get_jwt_subject())
        # Проверяем, токен на logout
        if not user_id or await redis_service.check_banned_access(UUID(user_id), authorize._token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # Получаем права текущего пользователя из Redis'а
        user_rights = await redis_service.get_user_rights(UUID(user_id))
        all_rights = await redis_service.get_all_rights()
        user_rights = {right[1] for right in all_rights if right[0] in user_rights}
        # Возвращаем модель JWT пользователя с его ID и правами
        return JWTUserModel(id=user_id, rights=user_rights)


async def get_jwt_user_global(request: Request, user: Annotated[JWTUserModel, Depends(JWTBearer())]) -> None:  # noqa: RUF029
    # Кладём в request пользователя токена с его правами
    request.jwt_user = user  # pyright: ignore[reportAttributeAccessIssue]
