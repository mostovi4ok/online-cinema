"""
This type stub file was generated by pyright.
"""

from aiokafka.metrics.compound_stat import AbstractCompoundStat

from .sampled_stat import AbstractSampledStat

class BucketSizing:
    CONSTANT = ...
    LINEAR = ...

class Percentiles(AbstractSampledStat, AbstractCompoundStat):
    """A compound stat that reports one or more percentiles"""

    def __init__(self, size_in_bytes, bucketing, max_val, min_val=..., percentiles=...) -> None: ...
    def stats(self):  # -> list[Any]:
        ...
    def value(self, config, now, quantile):  # -> float:
        ...
    def combine(self, samples, config, now):  # -> float:
        ...
    def new_sample(self, time_ms):  # -> HistogramSample:
        ...
    def update(self, sample, config, value, time_ms):  # -> None:
        ...

    class HistogramSample(AbstractSampledStat.Sample):
        def __init__(self, scheme, now) -> None: ...
