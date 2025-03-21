"""
This type stub file was generated by pyright.
"""

class TagType:
    STRING = ...
    DOUBLE = ...
    BOOL = ...
    LONG = ...
    BINARY = ...
    _VALUES_TO_NAMES = ...
    _NAMES_TO_VALUES = ...

class SpanRefType:
    CHILD_OF = ...
    FOLLOWS_FROM = ...
    _VALUES_TO_NAMES = ...
    _NAMES_TO_VALUES = ...

class Tag:
    """
    Attributes:
     - key
     - vType
     - vStr
     - vDouble
     - vBool
     - vLong
     - vBinary

    """

    thrift_spec = ...
    def __init__(self, key=..., vType=..., vStr=..., vDouble=..., vBool=..., vLong=..., vBinary=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class Log:
    """
    Attributes:
     - timestamp
     - fields

    """

    thrift_spec = ...
    def __init__(self, timestamp=..., fields=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class SpanRef:
    """
    Attributes:
     - refType
     - traceIdLow
     - traceIdHigh
     - spanId

    """

    thrift_spec = ...
    def __init__(self, refType=..., traceIdLow=..., traceIdHigh=..., spanId=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class Span:
    """
    Attributes:
     - traceIdLow
     - traceIdHigh
     - spanId
     - parentSpanId
     - operationName
     - references
     - flags
     - startTime
     - duration
     - tags
     - logs

    """

    thrift_spec = ...
    def __init__(
        self,
        traceIdLow=...,
        traceIdHigh=...,
        spanId=...,
        parentSpanId=...,
        operationName=...,
        references=...,
        flags=...,
        startTime=...,
        duration=...,
        tags=...,
        logs=...,
    ) -> None: ...
    def read(self, iprot): ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class Process:
    """
    Attributes:
     - serviceName
     - tags

    """

    thrift_spec = ...
    def __init__(self, serviceName=..., tags=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class Batch:
    """
    Attributes:
     - process
     - spans

    """

    thrift_spec = ...
    def __init__(self, process=..., spans=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class BatchSubmitResponse:
    """
    Attributes:
     - ok

    """

    thrift_spec = ...
    def __init__(self, ok=...) -> None: ...
    def read(self, iprot):  # -> None:
        ...
    def write(self, oprot):  # -> None:
        ...
    def validate(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
