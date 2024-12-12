import uuid
from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from config import configs


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=255, unique=True)
    rights = models.CharField(default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # строка с именем поля модели, которая используется в качестве уникального идентификатора
    USERNAME_FIELD = "login"

    def has_perm(self, perm: Any, obj: Any = None) -> bool:
        return perm in self.rights or configs.admin_right_name in self.rights

    def has_module_perms(self, app_label: Any) -> Literal[True]:
        return True

    def __str__(self) -> str:
        return f"{self.id}:{self.login}"
