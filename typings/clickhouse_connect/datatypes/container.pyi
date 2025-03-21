"""
This type stub file was generated by pyright.
"""

import typing
from collections.abc import Sequence

from clickhouse_connect.datatypes.base import ClickHouseType, TypeDef
from clickhouse_connect.driver.insert import InsertContext
from clickhouse_connect.driver.query import QueryContext
from clickhouse_connect.driver.types import ByteSource

logger = ...

class Array(ClickHouseType):
    __slots__ = ...
    python_type = list
    def __init__(self, type_def: TypeDef) -> None: ...
    def read_column_prefix(self, source: ByteSource):  # -> None:
        ...
    def read_column_data(self, source: ByteSource, num_rows: int, ctx: QueryContext):  # -> list[Any]:
        ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...
    def write_column_data(self, column: Sequence, dest: bytearray, ctx: InsertContext):  # -> None:
        ...

class Tuple(ClickHouseType):
    _slots = ...
    python_type = tuple
    valid_formats = ...
    def __init__(self, type_def: TypeDef) -> None: ...
    def read_column_prefix(self, source: ByteSource):  # -> None:
        ...
    def read_column_data(
        self, source: ByteSource, num_rows: int, ctx: QueryContext
    ):  # -> list[Any] | list[dict[Any, Any]] | tuple[Any, ...]:
        ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...
    def write_column_data(self, column: Sequence, dest: bytearray, ctx: InsertContext):  # -> None:
        ...
    def convert_dict_insert(self, column: Sequence) -> Sequence: ...

class Point(Tuple):
    def __init__(self, type_def) -> None: ...

class Map(ClickHouseType):
    _slots = ...
    python_type = dict
    def __init__(self, type_def: TypeDef) -> None: ...
    def read_column_prefix(self, source: ByteSource):  # -> None:
        ...
    def read_column_data(self, source: ByteSource, num_rows: int, ctx: QueryContext):  # -> list[Any]:
        ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...
    def write_column_data(self, column: Sequence, dest: bytearray, ctx: InsertContext):  # -> None:
        ...

class Nested(ClickHouseType):
    __slots__ = ...
    python_type: typing.TypeAlias = Sequence[dict]
    def __init__(self, type_def) -> None: ...
    def read_column_prefix(self, source: ByteSource):  # -> None:
        ...
    def read_column_data(self, source: ByteSource, num_rows: int, ctx: QueryContext):  # -> list[list[dict[Any, Any]]]:
        ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...
    def write_column_data(self, column: Sequence, dest: bytearray, ctx: InsertContext):  # -> None:
        ...

class JSON(ClickHouseType):
    python_type = dict
    valid_formats = ...
    def write_column_prefix(self, dest: bytearray):  # -> None:
        ...
    def write_column_data(self, column: Sequence, dest: bytearray, ctx: InsertContext):  # -> None:
        ...

class Object(JSON):
    python_type = dict
    def __init__(self, type_def) -> None: ...
