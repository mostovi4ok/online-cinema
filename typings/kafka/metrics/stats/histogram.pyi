"""
This type stub file was generated by pyright.
"""

class Histogram:
    def __init__(self, bin_scheme) -> None: ...
    def record(self, value):  # -> None:
        ...
    def value(self, quantile):  # -> float:
        ...
    @property
    def counts(self): ...
    def clear(self):  # -> None:
        ...

    class ConstantBinScheme:
        def __init__(self, bins, min_val, max_val) -> None: ...
        @property
        def bins(self):  # -> int:
            ...
        def from_bin(self, b):  # -> float:
            ...
        def to_bin(self, x):  # -> int:
            ...

    class LinearBinScheme:
        def __init__(self, num_bins, max_val) -> None: ...
        @property
        def bins(self):  # -> Any:
            ...
        def from_bin(self, b):  # -> float:
            ...
        def to_bin(self, x):  # -> int:
            ...
