import enum
import uuid
from typing import Any

from sqlalchemy import JSON, UUID, Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase): ...


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Template(id={self.id!r}, name={self.name!r})"


class Action(enum.Enum):
    LOGIN = 1
    LOGOUT = 2


user_right = Table(
    "user_right",
    Base.metadata,
    Column[Any]("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column[Any]("right_id", ForeignKey("right.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    password: Mapped[tuple[str, int, str, str]] = mapped_column(JSON, nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    rights: Mapped[list["Right"]] = relationship(secondary=user_right, back_populates="users", lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r})"


class Right(Base):
    __tablename__ = "right"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    users: Mapped[list[User]] = relationship(secondary=user_right, back_populates="rights", lazy="selectin")

    def __repr__(self) -> str:
        return f"Right(id={self.id!r}, name={self.name!r})"
