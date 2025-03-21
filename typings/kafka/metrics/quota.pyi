"""
This type stub file was generated by pyright.
"""

class Quota:
    """An upper or lower bound for metrics"""

    def __init__(self, bound, is_upper) -> None: ...
    @staticmethod
    def upper_bound(upper_bound):  # -> Quota:
        ...
    @staticmethod
    def lower_bound(lower_bound):  # -> Quota:
        ...
    def is_upper_bound(self):  # -> Any:
        ...
    @property
    def bound(self):  # -> Any:
        ...
    def is_acceptable(self, value):  # -> Literal[False]:
        ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
