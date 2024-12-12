"""
This type stub file was generated by pyright.
"""

from kafka.protocol.api import Request, Response

class MetadataResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataResponse_v2(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataResponse_v3(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataResponse_v4(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataResponse_v5(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class MetadataRequest_v0(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...

class MetadataRequest_v1(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...
    NO_TOPICS = ...

class MetadataRequest_v2(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...
    NO_TOPICS = ...

class MetadataRequest_v3(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...
    NO_TOPICS = ...

class MetadataRequest_v4(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...
    NO_TOPICS = ...

class MetadataRequest_v5(Request):
    """
    The v5 metadata request is the same as v4.
    An additional field for offline_replicas has been added to the v5 metadata response
    """

    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    ALL_TOPICS = ...
    NO_TOPICS = ...

MetadataRequest = ...
MetadataResponse = ...
