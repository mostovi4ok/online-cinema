"""
This type stub file was generated by pyright.
"""

from clickhouse_connect.datatypes.base import ArrayType, ClickHouseType, TypeDef, UnsupportedType
from clickhouse_connect.driver.types import ByteSource

empty_uuid_b = ...

class UUID(ClickHouseType):
    valid_formats = ...
    np_type = ...
    byte_size = ...
    def python_null(self, ctx):  # -> UUID | Literal['']:
        ...

class Nothing(ArrayType):
    _array_type = ...
    def __init__(self, type_def: TypeDef) -> None: ...

class SimpleAggregateFunction(ClickHouseType):
    _slots = ...
    def __init__(self, type_def: TypeDef) -> None: ...
    def read_column_prefix(self, source: ByteSource):  # -> None:
        ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...

class AggregateFunction(UnsupportedType): ...
