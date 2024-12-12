import uuid

from sqlalchemy import UUID, Boolean, DateTime, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    fio: Mapped[str | None] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="False")
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
