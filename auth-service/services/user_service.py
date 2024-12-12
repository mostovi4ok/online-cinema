from collections.abc import Sequence
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from api.v1.models.auth import AccountModel, HistoryModel
from db.postgres_db import get_session
from models.alchemy_model import Action, History, User
from services.password_service import PasswordService, get_password_service


class UserService:
    def __init__(self, session: AsyncSession, password: PasswordService) -> None:
        self.session = session
        self.password = password

    async def get_user(self, login: str) -> User | None:
        stmt = select(User).options(selectinload(User.rights)).where(User.login == login, User.is_deleted == False)  # noqa: E712
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_id(self, id_: str) -> User | None:
        stmt = select(User).options(selectinload(User.rights)).where(User.id == id_, User.is_deleted == False)  # noqa: E712
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).options(selectinload(User.rights)).where(User.email == email, User.is_deleted == False)  # noqa: E712
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_user(self, data: AccountModel) -> User:
        stmt = select(User).options(selectinload(User.rights)).where(User.login == data.login)
        result = await self.session.execute(stmt)
        deleted_user = result.scalars().first()
        if not deleted_user:
            user = User(
                login=data.login,
                password=self.password.compute_hash(data.password),
                email=data.email,
            )
            self.session.add(user)
        else:
            user = deleted_user
            user.email = data.email
            user.password = self.password.compute_hash(data.password)
            user.is_deleted = False

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        user.is_deleted = True
        user.histories.clear()
        user.rights.clear()
        self.session.add(user)
        await self.session.commit()

    async def change_password(self, user: User, new_password: str) -> None:
        user.password = self.password.compute_hash(new_password)
        await self.session.commit()
        await self.session.refresh(user)

    async def save_history(self, data: HistoryModel) -> History:
        history = History(**data.model_dump())
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_user_login_history(
        self, user_id: str | int | UUID | None, page_number: int, page_size: int
    ) -> Sequence[History]:
        stmt = (
            select(History)
            .where(History.user_id == user_id, History.action == Action.LOGIN)
            .order_by(History.created_at.desc())
            .limit(page_size)
            .offset((page_number - 1) * page_size)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


@lru_cache
def get_user_service(
    postgres: Annotated[AsyncSession, Depends(get_session)],
    password: Annotated[PasswordService, Depends(get_password_service)],
) -> UserService:
    return UserService(postgres, password)
