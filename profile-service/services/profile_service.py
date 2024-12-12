from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update

from api.v1.models.profile import ProfileInfo, ProfileModel, ProfileUpdate
from db.postgres_db import get_session
from models.alchemy_model import Profile
from services.custom_error import ResponseError


class ProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_profile(self, profile_data: ProfileInfo) -> ProfileModel:
        """Создание профиля пользователя"""
        stmt = select(Profile).where(Profile.id == profile_data.id)
        profile = (await self.session.execute(stmt)).scalars().first()
        if profile is None:
            profile = Profile(**profile_data.model_dump())
            self.session.add(profile)
            await self.session.commit()
            await self.session.refresh(profile)
        elif profile.is_deleted is False:
            raise ResponseError(f"Профиль с id '{profile_data.id}' уже существует")
        else:
            profile.email = profile_data.email
            profile.fio = None
            profile.phone_number = None
            profile.email_confirmed = False
            profile.is_deleted = False
            await self.session.commit()

        return ProfileModel(**profile.__dict__)

    async def get_profile(self, user_id: str | int | UUID | None) -> ProfileModel:
        """Получение профиля пользователя"""
        stmt = select(Profile).where(Profile.id == user_id, Profile.is_deleted == False)  # noqa: E712
        result = await self.session.execute(stmt)
        profile = result.scalars().first()
        if profile is None:
            raise ResponseError(f"Профиль с id '{user_id}' не найден")

        return ProfileModel(**profile.__dict__)

    async def update_profile(self, user_id: str | int | UUID | None, new_data: ProfileUpdate) -> ProfileModel:
        """Изменение профиля пользователя"""
        stmt = (
            update(Profile)
            .where(Profile.id == user_id, Profile.is_deleted == False)  # noqa: E712
            .values(**new_data.model_dump(exclude_none=True))
            .returning(Profile)
        )
        try:
            profile_ = (await self.session.scalars(stmt)).one()
        except NoResultFound:
            raise ResponseError(f"Профиля с id '{user_id}' не существует")

        await self.session.commit()
        return ProfileModel(
            id=profile_.id,
            login=profile_.login,
            fio=profile_.fio,
            email=profile_.email,
            phone_number=profile_.phone_number,
        )

    async def delete_profile(self, user_id: str | int | UUID | None) -> str:
        """Удаление профиля пользователя"""
        stmt = update(Profile).values(is_deleted=True).where(Profile.id == user_id)
        try:
            await self.session.execute(stmt)
        except NoResultFound:
            raise ResponseError(f"Профиля с id '{user_id}' не существует")

        await self.session.commit()
        return f"Пользователь с id '{user_id}' удален"

    async def confirm_email(self, user_id: str | int | UUID) -> None:
        profile = await self.session.get(Profile, user_id)
        if profile is None:
            raise ResponseError(f"Профиль с id '{user_id}' не найден")

        profile.email_confirmed = True
        await self.session.commit()


@lru_cache
def get_profile_service(
    postgres: Annotated[AsyncSession, Depends(get_session)],
) -> ProfileService:
    return ProfileService(postgres)
