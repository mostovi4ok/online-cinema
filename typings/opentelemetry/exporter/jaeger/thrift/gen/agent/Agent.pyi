"""
This type stub file was generated by pyright.
"""

from thrift.Thrift import TProcessor

from .ttypes import *

class Iface:
    def emitZipkinBatch(self, spans):  # -> None:
        """
        Parameters
        ----------
         - spans

        """

    def emitBatch(self, batch):  # -> None:
        """
        Parameters
        ----------
         - batch

        """

class Client(Iface):
    def __init__(self, iprot, oprot=...) -> None: ...
    def emitZipkinBatch(self, spans):  # -> None:
        """
        Parameters
        ----------
         - spans

        """

    def send_emitZipkinBatch(self, spans):  # -> None:
        ...
    def emitBatch(self, batch):  # -> None:
        """
        Parameters
        ----------
         - batch

        """

    def send_emitBatch(self, batch):  # -> None:
        ...

class Processor(Iface, TProcessor):
    def __init__(self, handler) -> None: ...
    def process(self, iprot, oprot):  # -> Literal[True] | None:
        ...
    def process_emitZipkinBatch(self, seqid, iprot, oprot):  # -> None:
        ...
    def process_emitBatch(self, seqid, iprot, oprot):  # -> None:
        ...

class emitZipkinBatch_args:
    """
    Attributes:
     - spans

    """

    thrift_spec = ...
    def __init__(self, spans=...) -> None: ...
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

class emitBatch_args:
    """
    Attributes:
     - batch

    """

    thrift_spec = ...
    def __init__(self, batch=...) -> None: ...
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
