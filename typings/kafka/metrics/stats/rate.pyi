"""
This type stub file was generated by pyright.
"""

from kafka.metrics.measurable_stat import AbstractMeasurableStat
from kafka.metrics.stats.sampled_stat import AbstractSampledStat

class TimeUnit:
    _names = ...
    NANOSECONDS = ...
    MICROSECONDS = ...
    MILLISECONDS = ...
    SECONDS = ...
    MINUTES = ...
    HOURS = ...
    DAYS = ...
    @staticmethod
    def get_name(time_unit):  # -> int:
        ...

class Rate(AbstractMeasurableStat):
    """
    The rate of the given quantity. By default this is the total observed
    over a set of samples from a sampled statistic divided by the elapsed
    time over the sample windows. Alternative AbstractSampledStat
    implementations can be provided, however, to record the rate of
    occurrences (e.g. the count of values measured over the time interval)
    or other such values.
    """

    def __init__(self, time_unit=..., sampled_stat=...) -> None: ...
    def unit_name(self):  # -> int:
        ...
    def record(self, config, value, time_ms):  # -> None:
        ...
    def measure(self, config, now): ...
    def window_size(self, config, now): ...
    def convert(self, time_ms): ...

class SampledTotal(AbstractSampledStat):
    def __init__(self, initial_value=...) -> None: ...
    def update(self, sample, config, value, time_ms):  # -> None:
        ...
    def combine(self, samples, config, now):  # -> float:
        ...
