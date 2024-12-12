from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import and_, or_, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.v1.models.access_control import (
    ChangeRightModel,
    CreateRightModel,
    ResponseUserModel,
    RightModel,
    RightsModel,
    SearchRightModel,
    UserModel,
)
from core.config import admin_config
from db.postgres_db import get_session
from models.alchemy_model import Right, User
from services.custom_error import ResponseError
from services.redis_service import RedisService, get_redis


NOT_ENOUGH_INFO = "Недостаточно информации"


class RightsManagementService:
    def __init__(self, redis: RedisService, session: AsyncSession) -> None:
        self.redis = redis
        self.session = session

    async def create(self, create_right: CreateRightModel) -> RightModel:
        """Создание права в системе"""
        stmt = select(Right).where(Right.name == create_right.name)
        try:
            (await self.session.scalars(stmt)).one()
        except NoResultFound:
            right_ = Right(**create_right.model_dump())
            self.session.add(right_)
            await self.session.commit()
            await self.session.refresh(right_)
            right = RightModel(id=right_.id, name=right_.name, description=right_.description)
            await self.redis.add_right(right)
            return right

        raise ResponseError(f"Право с названием '{create_right.name}' уже существует")

    async def delete(self, right: SearchRightModel) -> str:
        """Удаление права в системе"""
        if not right.model_dump(exclude_none=True):
            raise ResponseError(NOT_ENOUGH_INFO)

        stmt = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(f"Право '{right.name or right.id}' не существует")

        if right_.name == admin_config.right_name:
            raise ResponseError("Нельзя удалять право Администратора!")

        await self.session.delete(right_)
        await self.session.commit()
        await self.redis.delete_right(right_.id, right_.name)
        return f"Право '{right.name or right.id}' удалено"

    async def update(self, right_old: SearchRightModel, right_new: ChangeRightModel) -> RightModel:
        """Изменение свойств права в системе"""
        if not right_old.model_dump(exclude_none=True) or not right_new.model_dump(exclude_none=True):
            raise ResponseError(NOT_ENOUGH_INFO)

        admin_right = await self.get_admin_right()
        if right_old.id == admin_right.id or right_old.name == admin_right.name:
            raise ResponseError("Нельзя изменять право Администратора!")

        stmt = (
            update(Right)
            .where(or_(Right.name == right_old.name, Right.id == right_old.id))
            .values(**right_new.model_dump(exclude_none=True, exclude={"id", "current_name"}))
            .returning(Right)
        )
        try:
            right_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(f"Право '{right_old.name or right_old.id}' не существует")
        except IntegrityError:
            raise ResponseError(f"Право с названием '{right_new.name}' уже существует")

        await self.session.commit()
        right = RightModel(id=right_.id, name=right_.name, description=right_.description)
        if right_new.name != right_old.name:
            await self.redis.update_right(right)

        return right

    async def get_all(self) -> RightsModel:
        """Выгрузка всех прав"""
        all_rights = RightsModel(
            rights=[
                RightModel(id=right.id, name=right.name, description=right.description)
                for right in (await self.session.scalars(select(Right))).fetchall()
            ]
        )
        await self.redis.set_all_rights(all_rights.rights)
        return all_rights

    async def get_admin_right(self) -> Right:
        """Выгрузка права Администратора"""
        try:
            right_ = (await self.session.scalars(select(Right).where(Right.name == admin_config.right_name))).one()
        except NoResultFound:
            raise ResponseError("Право Администратора не существует")

        return right_

    async def assign(self, right: SearchRightModel, user: UserModel) -> ResponseUserModel:
        """Назначение права пользователю"""
        if not right.model_dump(exclude_none=True) or not user.model_dump(exclude_none=True):
            raise ResponseError(NOT_ENOUGH_INFO)

        stmt_right = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(f"Право '{right.name or right.id}' не существует")

        stmt_user = (
            select(User)
            .options(selectinload(User.rights))
            .where(
                and_(
                    or_(User.id == user.id, User.login == user.login, User.email == user.email),
                    User.is_deleted == False,  # noqa: E712
                )
            )
        )
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(f"Пользователь '{user.id or user.login or user.email}' не существует")

        if right_ in user_.rights:
            raise ResponseError(
                f"Пользователь '{user.id or user.login or user.email}' уже имеет право '{right.name or right.id}'"
            )

        user_.rights.append(right_)
        result = ResponseUserModel(
            id=user_.id,
            login=user_.login,
            email=user_.email,
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in user_.rights],
        )
        await self.session.commit()
        await self.redis.add_user_right(user_.id, right_.id)
        return result

    async def take_away(self, right: SearchRightModel, user: UserModel) -> ResponseUserModel:
        """Отъём права у пользователя"""
        if not right.model_dump(exclude_none=True) or not user.model_dump(exclude_none=True):
            raise ResponseError(NOT_ENOUGH_INFO)

        stmt_right = select(Right).where(or_(Right.name == right.name, Right.id == right.id))
        try:
            right_ = (await self.session.scalars(stmt_right)).one()
        except NoResultFound:
            raise ResponseError(f"Право '{right.name or right.id}' не существует")

        stmt_user = (
            select(User)
            .options(selectinload(User.rights))
            .where(
                and_(
                    or_(User.id == user.id, User.login == user.login, User.email == user.email),
                    User.is_deleted == False,  # noqa: E712
                )
            )
        )
        try:
            user_ = (await self.session.scalars(stmt_user)).one()
        except NoResultFound:
            raise ResponseError(f"Пользователь '{user.id or user.login or user.email}' не существует")

        try:
            user_.rights.remove(right_)
        except ValueError:
            raise ResponseError(
                f"Пользователь '{user.id or user.login or user.email}' не имеет право '{right.name or right.id}'"
            )

        result = ResponseUserModel(
            id=user_.id,
            login=user_.login,
            email=user_.email,
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in user_.rights],
        )
        await self.session.commit()
        await self.redis.delete_user_right(user_.id, right_.id)
        return result

    async def get_user_rights(self, user: UserModel) -> RightsModel:
        """Выгрузка всех прав пользователя"""
        if not user.model_dump(exclude_none=True):
            raise ResponseError(NOT_ENOUGH_INFO)

        stmt = (
            select(User)
            .options(selectinload(User.rights))
            .where(
                and_(
                    or_(User.id == user.id, User.login == user.login, User.email == user.email),
                    User.is_deleted == False,  # noqa: E712
                )
            )
        )
        try:
            rights = (await self.session.scalars(stmt)).unique().one()
        except NoResultFound:
            raise ResponseError(f"Пользователь '{user.id or user.login or user.email}' не существует")

        return RightsModel(
            rights=[RightModel(id=right.id, name=right.name, description=right.description) for right in rights.rights]
        )


@lru_cache
def get_rights_management_service(
    redis: Annotated[RedisService, Depends(get_redis)], postgres: Annotated[AsyncSession, Depends(get_session)]
) -> RightsManagementService:
    return RightsManagementService(redis, postgres)
