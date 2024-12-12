"""
This type stub file was generated by pyright.
"""

from datetime import date, datetime

from clickhouse_connect.datatypes.base import ClickHouseType, TypeDef

epoch_start_date = ...
epoch_start_datetime = ...

class Date(ClickHouseType):
    _array_type = ...
    np_type = ...
    nano_divisor = ...
    valid_formats = ...
    python_type = date
    byte_size = ...

class Date32(Date):
    byte_size = ...
    _array_type = ...

from_ts_naive = ...
from_ts_tz = ...

class DateTimeBase(ClickHouseType, registered=False):
    __slots__ = ...
    valid_formats = ...
    python_type = datetime

class DateTime(DateTimeBase):
    _array_type = ...
    np_type = ...
    nano_divisor = ...
    byte_size = ...
    def __init__(self, type_def: TypeDef) -> None: ...

class DateTime64(DateTimeBase):
    __slots__ = ...
    byte_size = ...
    def __init__(self, type_def: TypeDef) -> None: ...
    @property
    def np_type(self):  # -> str:
        ...
    @property
    def nano_divisor(self): ...
