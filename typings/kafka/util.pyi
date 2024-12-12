"""
This type stub file was generated by pyright.
"""

from kafka.vendor import six

if six.PY3:
    MAX_INT = ...
    TO_SIGNED = ...
    def crc32(data):  # -> int:
        ...

else: ...

class WeakMethod:
    """
    Callable that weakly references a method and the object it is bound to. It
    is based on https://stackoverflow.com/a/24287465.

    Arguments:
        object_dot_method: A bound instance method (i.e. 'object.method').

    """

    def __init__(self, object_dot_method) -> None: ...
    def __call__(self, *args, **kwargs):
        """
        Calls the method on target with args and kwargs.
        """

    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...

class Dict(dict):
    """Utility class to support passing weakrefs to dicts

    See: https://docs.python.org/2/library/weakref.html
    """
