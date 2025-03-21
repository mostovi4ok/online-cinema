"""
This type stub file was generated by pyright.
"""

from kafka.metrics.stats.sampled_stat import AbstractSampledStat

class Max(AbstractSampledStat):
    """An AbstractSampledStat that gives the max over its samples."""

    def __init__(self) -> None: ...
    def update(self, sample, config, value, now):  # -> None:
        ...
    def combine(self, samples, config, now):  # -> float:
        ...
