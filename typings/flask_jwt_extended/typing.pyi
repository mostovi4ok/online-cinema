"""
This type stub file was generated by pyright.
"""

from datetime import timedelta
from typing import Literal, TypeAlias

ExpiresDelta: TypeAlias = Literal[False] | timedelta
Fresh: TypeAlias = bool | float | timedelta
