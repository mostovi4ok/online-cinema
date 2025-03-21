"""
This type stub file was generated by pyright.
"""

from thrift.Thrift import TProcessor

from .ttypes import *

class Iface:
    def submitBatches(self, batches):  # -> None:
        """
        Parameters
        ----------
         - batches

        """

class Client(Iface):
    def __init__(self, iprot, oprot=...) -> None: ...
    def submitBatches(self, batches):  # -> list[Any]:
        """
        Parameters
        ----------
         - batches

        """

    def send_submitBatches(self, batches):  # -> None:
        ...
    def recv_submitBatches(self):  # -> list[Any]:
        ...

class Processor(Iface, TProcessor):
    def __init__(self, handler) -> None: ...
    def process(self, iprot, oprot):  # -> Literal[True] | None:
        ...
    def process_submitBatches(self, seqid, iprot, oprot):  # -> None:
        ...

class submitBatches_args:
    """
    Attributes:
     - batches

    """

    thrift_spec = ...
    def __init__(self, batches=...) -> None: ...
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

class submitBatches_result:
    """
    Attributes:
     - success

    """

    thrift_spec = ...
    def __init__(self, success=...) -> None: ...
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
