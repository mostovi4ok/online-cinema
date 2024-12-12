"""
This type stub file was generated by pyright.
"""

from enum import Enum
from typing import Final

NETWORK_LOCAL_ADDRESS: Final = ...
NETWORK_LOCAL_PORT: Final = ...
NETWORK_PEER_ADDRESS: Final = ...
NETWORK_PEER_PORT: Final = ...
NETWORK_PROTOCOL_NAME: Final = ...
NETWORK_PROTOCOL_VERSION: Final = ...
NETWORK_TRANSPORT: Final = ...
NETWORK_TYPE: Final = ...

class NetworkTransportValues(Enum):
    TCP = ...
    UDP = ...
    PIPE = ...
    UNIX = ...
    QUIC = ...

class NetworkTypeValues(Enum):
    IPV4 = ...
    IPV6 = ...
