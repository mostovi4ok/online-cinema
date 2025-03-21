"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod

DEFAULT_CAP = ...
DEFAULT_BASE = ...

class AbstractBackoff(ABC):
    """Backoff interface"""

    def reset(self):  # -> None:
        """
        Reset internal state before an operation.
        `reset` is called once at the beginning of
        every call to `Retry.call_with_retry`
        """

    @abstractmethod
    def compute(self, failures: int) -> float:
        """Compute backoff in seconds upon failure"""
        ...

class ConstantBackoff(AbstractBackoff):
    """Constant backoff upon failure"""

    def __init__(self, backoff: float) -> None:
        """`backoff`: backoff time in seconds"""

    def compute(self, failures: int) -> float: ...

class NoBackoff(ConstantBackoff):
    """No backoff upon failure"""

    def __init__(self) -> None: ...

class ExponentialBackoff(AbstractBackoff):
    """Exponential backoff upon failure"""

    def __init__(self, cap: float = ..., base: float = ...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """

    def compute(self, failures: int) -> float: ...

class FullJitterBackoff(AbstractBackoff):
    """Full jitter backoff upon failure"""

    def __init__(self, cap: float = ..., base: float = ...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """

    def compute(self, failures: int) -> float: ...

class EqualJitterBackoff(AbstractBackoff):
    """Equal jitter backoff upon failure"""

    def __init__(self, cap: float = ..., base: float = ...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """

    def compute(self, failures: int) -> float: ...

class DecorrelatedJitterBackoff(AbstractBackoff):
    """Decorrelated jitter backoff upon failure"""

    def __init__(self, cap: float = ..., base: float = ...) -> None:
        """
        `cap`: maximum backoff time in seconds
        `base`: base backoff time in seconds
        """

    def reset(self) -> None: ...
    def compute(self, failures: int) -> float: ...

def default_backoff():  # -> EqualJitterBackoff:
    ...
