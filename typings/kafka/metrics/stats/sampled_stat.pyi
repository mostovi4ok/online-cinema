"""
This type stub file was generated by pyright.
"""

import abc

from kafka.metrics.measurable_stat import AbstractMeasurableStat

class AbstractSampledStat(AbstractMeasurableStat):
    """
    An AbstractSampledStat records a single scalar value measured over
    one or more samples. Each sample is recorded over a configurable
    window. The window can be defined by number of events or elapsed
    time (or both, if both are given the window is complete when
    *either* the event count or elapsed time criterion is met).

    All the samples are combined to produce the measurement. When a
    window is complete the oldest sample is cleared and recycled to
    begin recording the next sample.

    Subclasses of this class define different statistics measured
    using this basic pattern.
    """

    __metaclass__ = abc.ABCMeta
    def __init__(self, initial_value) -> None: ...
    @abc.abstractmethod
    def update(self, sample, config, value, time_ms): ...
    @abc.abstractmethod
    def combine(self, samples, config, now): ...
    def record(self, config, value, time_ms):  # -> None:
        ...
    def new_sample(self, time_ms):  # -> Sample:
        ...
    def measure(self, config, now):  # -> float:
        ...
    def current(self, time_ms): ...
    def oldest(self, now): ...
    def purge_obsolete_samples(self, config, now):  # -> None:
        """
        Timeout any windows that have expired in the absence of any events
        """

    class Sample:
        def __init__(self, initial_value, now) -> None: ...
        def reset(self, now):  # -> None:
            ...
        def is_complete(self, time_ms, config): ...
