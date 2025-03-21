"""
This type stub file was generated by pyright.
"""

from abc import abstractmethod

import brotli

available_compression = ...
if brotli: ...
comp_map = ...

class Compressor:
    def __init_subclass__(cls, tag: str, thread_safe: bool = ...):  # -> None:
        ...
    @abstractmethod
    def compress_block(self, block) -> bytes | bytearray: ...
    def flush(self):  # -> None:
        ...

class GzipCompressor(Compressor, tag="gzip", thread_safe=False):
    def __init__(self, level: int = ..., wbits: int = ...) -> None: ...
    def compress_block(self, block):  # -> bytes:
        ...
    def flush(self):  # -> bytes:
        ...

class Lz4Compressor(Compressor, tag="lz4", thread_safe=False):
    def __init__(self) -> None: ...
    def compress_block(self, block): ...

class ZstdCompressor(Compressor, tag="zstd"):
    def compress_block(self, block):  # -> bytes:
        ...

class BrotliCompressor(Compressor, tag="br"):
    def compress_block(self, block): ...

null_compressor = ...

def get_compressor(compression: str) -> Compressor: ...
