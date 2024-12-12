import uuid

from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=60, unique=True, null=False, blank=False)
    fio = models.CharField(max_length=60, blank=True, default=None)
    email = models.CharField(max_length=60, unique=True, null=False, blank=False)
    email_confirmed = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "profile"
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"{self.id}:{self.login}"
