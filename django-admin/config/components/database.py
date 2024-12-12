from config import configs


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": configs.movies_db_name,
        "USER": configs.movies_db_user,
        "PASSWORD": configs.movies_db_password,
        "HOST": configs.movies_db_host,
        "PORT": configs.movies_db_port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    },
    "auth": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": configs.auth_db_name,
        "USER": configs.auth_db_user,
        "PASSWORD": configs.auth_db_password,
        "HOST": configs.auth_db_host,
        "PORT": configs.auth_db_port,
    },
    "profile": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": configs.profile_db_name,
        "USER": configs.profile_db_user,
        "PASSWORD": configs.profile_db_password,
        "HOST": configs.profile_db_host,
        "PORT": configs.profile_db_port,
    },
}

DATABASE_ROUTERS = ["config.components.db_routers.ProfileRouter", "config.components.db_routers.AuthApiRouter"]
