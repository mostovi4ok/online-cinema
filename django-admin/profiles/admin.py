from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.http.request import HttpRequest

from profiles.models import Profile
from users.models import User


class CustomRequest(HttpRequest):
    user: User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    using = "profile"

    list_display = ("login", "fio", "email", "email_confirmed", "is_deleted")
    search_fields = ("login", "fio", "email", "phone_number")
    empty_value_display = "--empty--"

    def has_add_permission(self, request: CustomRequest) -> bool:
        has_permission = self.using in request.user.rights
        opts = self.opts
        codename = get_permission_codename("add", opts)
        return has_permission or request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_change_permission(self, request: CustomRequest, obj: Profile | None = None) -> bool:
        has_permission = self.using in request.user.rights
        opts = self.opts
        codename = get_permission_codename("change", opts)
        return has_permission or request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_delete_permission(self, request: CustomRequest, obj: Profile | None = None) -> bool:
        has_permission = self.using in request.user.rights
        opts = self.opts
        codename = get_permission_codename("delete", opts)
        return has_permission or request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_view_permission(self, request: CustomRequest, obj: Profile | None = None) -> bool:
        has_permission = self.using in request.user.rights
        opts = self.opts
        codename_view = get_permission_codename("view", opts)
        codename_change = get_permission_codename("change", opts)
        return (
            has_permission
            or request.user.has_perm(f"{opts.app_label}.{codename_view}")
            or request.user.has_perm(f"{opts.app_label}.{codename_change}")
        )
