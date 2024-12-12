from config.config import *  # noqa: F403

from .celery import app as app  # pyright: ignore[reportUnknownVariableType] # noqa: PLC0414, TID252


__all__ = ("app",)
