"""
This type stub file was generated by pyright.
"""

from kafka.record.abc import ABCRecord, ABCRecordBatch, ABCRecordBatchBuilder

class LegacyRecordBase:
    __slots__ = ...
    HEADER_STRUCT_V0 = ...
    HEADER_STRUCT_V1 = ...
    CRC_OFFSET = ...
    MAGIC_OFFSET = ...
    RECORD_OVERHEAD_V0 = ...
    RECORD_OVERHEAD_V1 = ...
    KEY_OFFSET_V0 = ...
    KEY_OFFSET_V1 = ...
    VALUE_LENGTH = ...
    CODEC_MASK = ...
    CODEC_NONE = ...
    CODEC_GZIP = ...
    CODEC_SNAPPY = ...
    CODEC_LZ4 = ...
    TIMESTAMP_TYPE_MASK = ...
    LOG_APPEND_TIME = ...
    CREATE_TIME = ...
    NO_TIMESTAMP = ...

class LegacyRecordBatch(ABCRecordBatch, LegacyRecordBase):
    __slots__ = ...
    def __init__(self, buffer, magic) -> None: ...
    @property
    def timestamp_type(self):  # -> Literal[1, 0] | None:
        """0 for CreateTime; 1 for LogAppendTime; None if unsupported.

        Value is determined by broker; produced messages should always set to 0
        Requires Kafka >= 0.10 / message version >= 1
        """

    @property
    def compression_type(self):  # -> Any:
        ...
    def validate_crc(self):  # -> Any:
        ...
    def __iter__(self):  # -> Generator[LegacyRecord, Any, None]:
        ...

class LegacyRecord(ABCRecord):
    __slots__ = ...
    def __init__(self, offset, timestamp, timestamp_type, key, value, crc) -> None: ...
    @property
    def offset(self):  # -> Any:
        ...
    @property
    def timestamp(self):  # -> Any:
        """Epoch milliseconds"""

    @property
    def timestamp_type(self):  # -> Any:
        """CREATE_TIME(0) or APPEND_TIME(1)"""

    @property
    def key(self):  # -> Any:
        """Bytes key or None"""

    @property
    def value(self):  # -> Any:
        """Bytes value or None"""

    @property
    def headers(self):  # -> list[Any]:
        ...
    @property
    def checksum(self):  # -> Any:
        ...
    def __repr__(self):  # -> LiteralString:
        ...

class LegacyRecordBatchBuilder(ABCRecordBatchBuilder, LegacyRecordBase):
    __slots__ = ...
    def __init__(self, magic, compression_type, batch_size) -> None: ...
    def append(self, offset, timestamp, key, value, headers=...):  # -> LegacyRecordMetadata | None:
        """Append message to batch."""

    def build(self):  # -> bytearray:
        """Compress batch to be ready for send"""

    def size(self):  # -> int:
        """Return current size of data written to buffer"""

    def size_in_bytes(self, offset, timestamp, key, value, headers=...):  # -> int:
        """Actual size of message to add"""

    @classmethod
    def record_size(cls, magic, key, value):  # -> int:
        ...
    @classmethod
    def record_overhead(cls, magic):  # -> int:
        ...
    @classmethod
    def estimate_size_in_bytes(cls, magic, compression_type, key, value):  # -> int:
        """Upper bound estimate of record size."""

class LegacyRecordMetadata:
    __slots__ = ...
    def __init__(self, offset, crc, size, timestamp) -> None: ...
    @property
    def offset(self):  # -> Any:
        ...
    @property
    def crc(self):  # -> Any:
        ...
    @property
    def size(self):  # -> Any:
        ...
    @property
    def timestamp(self):  # -> Any:
        ...
    def __repr__(self):  # -> LiteralString:
        ...
