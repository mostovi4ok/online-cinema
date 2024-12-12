from uuid import UUID  # noqa: A005

from pydantic import BaseModel, Field


class ProfileModel(BaseModel):
    id: UUID = Field(description="Идентификатор профиля", title="Идентификатор")
    login: str = Field(description="Логин пользователя", title="Логин")
    fio: str | None = Field(default=None, description="ФИО пользователя", title="ФИО")
    email: str = Field(description="Электронная почта пользователя", title="Email")
    phone_number: str | None = Field(default=None, description="Номер телефона пользователя", title="Номер телефона")


class ProfileInfo(BaseModel):
    id: UUID = Field(description="Идентификатор профиля", title="Идентификатор")
    login: str = Field(description="Логин пользователя", title="Логин")
    email: str = Field(description="Электронная почта пользователя", title="Email")


class ProfileUpdate(BaseModel):
    fio: str | None = Field(default=None, description="ФИО пользователя", title="ФИО")
    phone_number: str | None = Field(default=None, description="Номер телефона пользователя", title="Номер телефона")
