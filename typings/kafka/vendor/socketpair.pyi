"""
This type stub file was generated by pyright.
"""

import socket

_LOCALHOST = ...
_LOCALHOST_V6 = ...
if not hasattr(socket, "socketpair"):
    def socketpair(family=..., type=..., proto=...):  # -> tuple[socket, socket]:
        ...
