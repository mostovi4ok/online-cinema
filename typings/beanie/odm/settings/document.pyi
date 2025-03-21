"""
This type stub file was generated by pyright.
"""

from beanie.odm.fields import IndexModelField
from beanie.odm.settings.base import ItemSettings
from beanie.odm.settings.timeseries import TimeSeriesConfig
from beanie.odm.utils.pydantic import IS_PYDANTIC_V2

if IS_PYDANTIC_V2: ...

class DocumentSettings(ItemSettings):
    use_state_management: bool = ...
    state_management_replace_objects: bool = ...
    state_management_save_previous: bool = ...
    validate_on_save: bool = ...
    use_revision: bool = ...
    single_root_inheritance: bool = ...
    indexes: list[IndexModelField] = ...
    merge_indexes: bool = ...
    timeseries: TimeSeriesConfig | None = ...
    lazy_parsing: bool = ...
    keep_nulls: bool = ...
    max_nesting_depths_per_field: dict = ...
    max_nesting_depth: int = ...
    if IS_PYDANTIC_V2:
        model_config = ...
    else:
        class Config:
            arbitrary_types_allowed = ...
