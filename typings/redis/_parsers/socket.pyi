"""
This type stub file was generated by pyright.
"""

import socket

from ..utils import SSL_AVAILABLE

NONBLOCKING_EXCEPTION_ERROR_NUMBERS = ...
if SSL_AVAILABLE: ...
NONBLOCKING_EXCEPTIONS = ...
SERVER_CLOSED_CONNECTION_ERROR = ...
SENTINEL = ...
SYM_CRLF = ...

class SocketBuffer:
    def __init__(self, socket: socket.socket, socket_read_size: int, socket_timeout: float) -> None: ...
    def unread_bytes(self) -> int:
        """
        Remaining unread length of buffer
        """

    def can_read(self, timeout: float) -> bool: ...
    def read(self, length: int) -> bytes: ...
    def readline(self) -> bytes: ...
    def get_pos(self) -> int:
        """
        Get current read position
        """

    def rewind(self, pos: int) -> None:
        """
        Rewind the buffer to a specific position, to re-start reading
        """

    def purge(self) -> None:
        """
        After a successful read, purge the read part of buffer
        """

    def close(self) -> None: ...
