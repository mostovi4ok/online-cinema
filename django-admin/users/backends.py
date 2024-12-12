import http
import json
from typing import Any
from uuid import UUID

import requests
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from auth_api.models import AuthUser
from config import configs
from users.models import User


class CustomAuthBackend(BaseBackend):
    def authenticate(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, request: HttpRequest, username: str | None = None, password: str | None = None, **kwargs: Any
    ) -> User | None:
        try:
            response = requests.post(
                configs.auth_api_login_url or "",
                data=json.dumps({"login": username, "password": password}),
                headers={"X-Request-Id": request.headers.get("X-Request-Id")},
                timeout=(3, 10),
            )
        except requests.exceptions.ConnectionError:
            return None

        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, _ = User.objects.get_or_create(login=data["login"])
            user.login = data.get("login")
            user.is_admin = configs.admin_right_name in data.get("rights")
            user.is_staff = configs.admin_right_name in data.get("rights") or configs.moderator_right_name in data.get(
                "rights"
            )
            user.is_active = True
            user.save()
        except Exception:  # noqa: BLE001
            return None

        return user

    def get_user(self, user_id: UUID) -> User | None:  # pyright: ignore[reportIncompatibleMethodOverride]
        try:
            user = User.objects.get(pk=user_id)
            auth_user = AuthUser.objects.get(login=user.login, is_deleted=False)
        except (User.DoesNotExist, AuthUser.DoesNotExist):
            return None
        user.rights = ", ".join(auth_user.rights.all().values_list("name", flat=True))
        user.save()
        return user
