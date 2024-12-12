from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.fields import Field

from models.alchemy_model import Action


class SecureRightModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(description="Название права", title="Название")


class ChangePasswordModel(BaseModel):
    old_password: str = Field(description="Старый пароль", title="Old Password", min_length=4)
    new_password: str = Field(description="Новый пароль", title="New Password", min_length=4)


class SecureAccountModel(BaseModel):
    login: str = Field(description="Логин пользователя", title="Login")
    email: str = Field(description="Почта пользователя", title="Email Address")


class RightsAccountModel(SecureAccountModel):
    model_config = ConfigDict(from_attributes=True)

    rights: list[SecureRightModel | str] = Field(description="Права пользователя", title="Права")

    @field_validator("rights")
    def handle_rights_model(cls, v: list[SecureRightModel]) -> list[object]:  # noqa: N805
        return [instance.name for instance in v]


class AccountModel(SecureAccountModel):
    password: str = Field(description="Пароль пользователя", title="Password", min_length=4)


class LoginModel(BaseModel):
    login: str = Field(description="Логин пользователя", title="Login")
    password: str = Field(description="Пароль пользователя", title="Password")


class ActualTokensModel(BaseModel):
    access_token: str = Field(description="Токен доступа", title="Access Token")
    refresh_token: str = Field(description="Токен обновления", title="Refresh Token")


class HistoryModel(BaseModel):
    user_id: UUID = Field(description="ID пользователя", title="User ID")
    ip_address: str = Field(description="IP устройства", title="IP Adress")
    action: Action = Field(description="Действие", title="Action")
    browser_info: str = Field(description="Описание браузера", title="Browser Info")
    system_info: str = Field(description="Описание системы", title="System Info")


class AccountHistoryModel(BaseModel):
    created_at: datetime = Field(description="Дата действия", title="Created At")
    ip_address: str = Field(description="IP устройства", title="IP Adress")
    browser_info: str = Field(description="Описание браузера", title="Browser Info")
    system_info: str = Field(description="Описание системы", title="System Info")


class JWTUserModel(BaseModel):
    id: str = Field(description="Идентификатор юзера", title="Идентификатор")
    rights: set[UUID] = Field(description="Права юзера", title="Права")
