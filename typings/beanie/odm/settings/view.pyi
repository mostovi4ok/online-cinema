"""
This type stub file was generated by pyright.
"""

from typing import Any

from beanie.odm.settings.base import ItemSettings

class ViewSettings(ItemSettings):
    source: str | type
    pipeline: list[dict[str, Any]]
    max_nesting_depths_per_field: dict = ...
    max_nesting_depth: int = ...
