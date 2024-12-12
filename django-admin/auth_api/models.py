import uuid

from django.db import models


class AuthRight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True, null=False, blank=False)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "right"

    def __str__(self) -> str:
        return f"{self.name}"


class AuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)
    rights = models.ManyToManyField(
        AuthRight,
        through="AuthUserRight",
        related_name="users",
        verbose_name="Права",
        blank=True,
    )

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "user"

    def __str__(self) -> str:
        return f"{self.id}:{self.login}"


class AuthUserRight(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    right = models.ForeignKey(AuthRight, on_delete=models.CASCADE)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "user_right"

    def __str__(self) -> str:
        return f"{self.user.login}:{self.right.name}"
