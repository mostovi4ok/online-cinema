"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Iterable

from aiokafka.util import NO_EXTENSIONS

def encode_varint_py(value: int, write: Callable[[int], None]) -> int:
    """Encode an integer to a varint presentation. See
    https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    on how those can be produced.

    Arguments:
            value (int): Value to encode
            write (function): Called per byte that needs to be written

    Returns:
            int: Number of bytes written

    """

def size_of_varint_py(value: int) -> int:
    """Number of bytes needed to encode an integer in variable-length format."""

def decode_varint_py(buffer: bytearray, pos: int = ...) -> tuple[int, int]:
    """Decode an integer from a varint presentation. See
    https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    on how those can be produced.

    Arguments:
            buffer (bytearry): buffer to read from.
            pos (int): optional position to read from

    Returns:
            (int, int): Decoded int value and next read position

    """

def calc_crc32c_py(memview: Iterable[int]) -> int:
    """Calculate CRC-32C (Castagnoli) checksum over a memoryview of data"""

calc_crc32c: Callable[[bytes | bytearray], int]
decode_varint: Callable[[bytearray, int], tuple[int, int]]
size_of_varint: Callable[[int], int]
encode_varint: Callable[[int, Callable[[int], None]], int]
if NO_EXTENSIONS:
    calc_crc32c = ...
    decode_varint = ...
    size_of_varint = ...
    encode_varint = ...
else:
    decode_varint = ...
    encode_varint = ...
    size_of_varint = ...
    calc_crc32c = ...
