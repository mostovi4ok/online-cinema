import os
from pathlib import Path

from split_settings.tools import include

from config import configs


include(
    "components/database.py",
    "components/templates.py",
    "components/apps_middleware.py",
    "components/pass_validators.py",
    "components/sentry.py",
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = configs.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = configs.debug

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _: DEBUG}  # pyright: ignore[reportUnknownLambdaType, reportUnknownVariableType]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:81", "http://localhost:81"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:81", "http://localhost:81"]

SHOW_TOOLBAR_CALLBACK = True

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-RU"

LOCALE_PATHS = ["movies/locale"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa: PTH118

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "users.backends.CustomAuthBackend",
]

CELERY_BROKER_URL = f"redis://{configs.redis_host}:{configs.redis_port}/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
