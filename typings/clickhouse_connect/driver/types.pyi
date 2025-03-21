"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, TypeAlias

Matrix: TypeAlias = Sequence[Sequence[Any]]

class Closable(ABC):
    @abstractmethod
    def close(self):  # -> None:
        ...

class ByteSource(Closable):
    last_message = ...
    @abstractmethod
    def read_leb128(self) -> int: ...
    @abstractmethod
    def read_leb128_str(self) -> str: ...
    @abstractmethod
    def read_uint64(self) -> int: ...
    @abstractmethod
    def read_bytes(self, sz: int) -> bytes: ...
    @abstractmethod
    def read_str_col(self, num_rows: int, encoding: str, nullable: bool = ..., null_obj: Any = ...):  # -> None:
        ...
    @abstractmethod
    def read_bytes_col(self, sz: int, num_rows: int):  # -> None:
        ...
    @abstractmethod
    def read_fixed_str_col(self, sz: int, num_rows: int, encoding: str):  # -> None:
        ...
    @abstractmethod
    def read_array(self, array_type: str, num_rows: int):  # -> None:
        ...
    @abstractmethod
    def read_byte(self) -> int: ...
