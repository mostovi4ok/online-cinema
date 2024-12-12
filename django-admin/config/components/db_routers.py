from typing import Any

from django.db.models import Model


class ProfileRouter:
    route_app_label = "profiles"
    route_db_label = "profile"

    def db_for_read(self, model: Model, **hints: dict[str, Any]) -> str | None:
        if model._meta.app_label == self.route_app_label:
            return self.route_db_label
        return None

    def db_for_write(self, model: Model, **hints: dict[str, Any]) -> str | None:
        if model._meta.app_label == self.route_app_label:
            return self.route_db_label
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: str | None = None, **hints: dict[str, Any]
    ) -> bool | None:
        if app_label == self.route_app_label:
            return False
        return None


class AuthApiRouter:
    route_app_label = "auth_api"
    route_db_label = "auth"

    def db_for_read(self, model: Model, **hints: dict[str, Any]) -> str | None:
        if model._meta.app_label == self.route_app_label:
            return self.route_db_label
        return None

    def db_for_write(self, model: Model, **hints: dict[str, Any]) -> str | None:
        if model._meta.app_label == self.route_app_label:
            return self.route_db_label
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: str | None = None, **hints: dict[str, Any]
    ) -> bool | None:
        if app_label == self.route_app_label:
            return False
        return None
