"""
This type stub file was generated by pyright.
"""

import abc

from .stat import AbstractStat

class AbstractCompoundStat(AbstractStat, abc.ABC):
    """
    A compound stat is a stat where a single measurement and associated
    data structure feeds many metrics. This is the example for a
    histogram which has many associated percentiles.
    """

    def stats(self):
        """
        Return list of NamedMeasurable
        """

class NamedMeasurable:
    def __init__(self, metric_name, measurable_stat) -> None: ...
    @property
    def name(self):  # -> Any:
        ...
    @property
    def stat(self):  # -> Any:
        ...
