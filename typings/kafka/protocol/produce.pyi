"""
This type stub file was generated by pyright.
"""

from kafka.protocol.api import Request, Response

class ProduceResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v2(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v3(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v4(Response):
    """
    The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 3
    """

    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v5(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v6(Response):
    """
    The version number is bumped to indicate that on quota violation brokers send out responses before throttling.
    """

    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v7(Response):
    """
    V7 bumped up to indicate ZStandard capability. (see KIP-110)
    """

    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceResponse_v8(Response):
    """
    V8 bumped up to add two new fields record_errors offset list and error_message
    (See KIP-467)
    """

    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class ProduceRequest(Request):
    API_KEY = ...
    def expect_response(self):  # -> bool:
        ...

class ProduceRequest_v0(ProduceRequest):
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v1(ProduceRequest):
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v2(ProduceRequest):
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v3(ProduceRequest):
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v4(ProduceRequest):
    """
    The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 3
    """

    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v5(ProduceRequest):
    """
    Same as v4. The version number is bumped since the v5 response includes an additional
    partition level field: the log_start_offset.
    """

    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v6(ProduceRequest):
    """
    The version number is bumped to indicate that on quota violation brokers send out responses before throttling.
    """

    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v7(ProduceRequest):
    """
    V7 bumped up to indicate ZStandard capability. (see KIP-110)
    """

    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class ProduceRequest_v8(ProduceRequest):
    """
    V8 bumped up to add two new fields record_errors offset list and error_message to PartitionResponse
    (See KIP-467)
    """

    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

ProduceRequest = ...
ProduceResponse = ...
