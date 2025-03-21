"""
This type stub file was generated by pyright.
"""

from typing import Final

from opentelemetry.metrics import Histogram, Meter, UpDownCounter

HTTP_CLIENT_ACTIVE_REQUESTS: Final = ...

def create_http_client_active_requests(meter: Meter) -> UpDownCounter:
    """Number of active HTTP requests"""

HTTP_CLIENT_CONNECTION_DURATION: Final = ...

def create_http_client_connection_duration(meter: Meter) -> Histogram:
    """The duration of the successfully established outbound HTTP connections"""

HTTP_CLIENT_OPEN_CONNECTIONS: Final = ...

def create_http_client_open_connections(meter: Meter) -> UpDownCounter:
    """Number of outbound HTTP connections that are currently active or idle on the client"""

HTTP_CLIENT_REQUEST_BODY_SIZE: Final = ...

def create_http_client_request_body_size(meter: Meter) -> Histogram:
    """Size of HTTP client request bodies"""

HTTP_CLIENT_REQUEST_DURATION: Final = ...

def create_http_client_request_duration(meter: Meter) -> Histogram:
    """Duration of HTTP client requests"""

HTTP_CLIENT_RESPONSE_BODY_SIZE: Final = ...

def create_http_client_response_body_size(meter: Meter) -> Histogram:
    """Size of HTTP client response bodies"""

HTTP_SERVER_ACTIVE_REQUESTS: Final = ...

def create_http_server_active_requests(meter: Meter) -> UpDownCounter:
    """Number of active HTTP server requests"""

HTTP_SERVER_REQUEST_BODY_SIZE: Final = ...

def create_http_server_request_body_size(meter: Meter) -> Histogram:
    """Size of HTTP server request bodies"""

HTTP_SERVER_REQUEST_DURATION: Final = ...

def create_http_server_request_duration(meter: Meter) -> Histogram:
    """Duration of HTTP server requests"""

HTTP_SERVER_RESPONSE_BODY_SIZE: Final = ...

def create_http_server_response_body_size(meter: Meter) -> Histogram:
    """Size of HTTP server response bodies"""
