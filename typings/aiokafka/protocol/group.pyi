"""
This type stub file was generated by pyright.
"""

from .api import Request, Response
from .struct import Struct

class JoinGroupResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class JoinGroupResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class JoinGroupResponse_v2(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class JoinGroupResponse_v5(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class JoinGroupRequest_v0(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    UNKNOWN_MEMBER_ID = ...

class JoinGroupRequest_v1(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    UNKNOWN_MEMBER_ID = ...

class JoinGroupRequest_v2(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    UNKNOWN_MEMBER_ID = ...

class JoinGroupRequest_v5(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...
    UNKNOWN_MEMBER_ID = ...

JoinGroupRequest = ...
JoinGroupResponse = ...

class ProtocolMetadata(Struct):
    SCHEMA = ...

class SyncGroupResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class SyncGroupResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class SyncGroupResponse_v3(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class SyncGroupRequest_v0(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class SyncGroupRequest_v1(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class SyncGroupRequest_v3(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

SyncGroupRequest = ...
SyncGroupResponse = ...

class MemberAssignment(Struct):
    SCHEMA = ...

class HeartbeatResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class HeartbeatResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class HeartbeatRequest_v0(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class HeartbeatRequest_v1(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

HeartbeatRequest = ...
HeartbeatResponse = ...

class LeaveGroupResponse_v0(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class LeaveGroupResponse_v1(Response):
    API_KEY = ...
    API_VERSION = ...
    SCHEMA = ...

class LeaveGroupRequest_v0(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

class LeaveGroupRequest_v1(Request):
    API_KEY = ...
    API_VERSION = ...
    RESPONSE_TYPE = ...
    SCHEMA = ...

LeaveGroupRequest = ...
LeaveGroupResponse = ...
