"""
This type stub file was generated by pyright.
"""

from .commands import *

class AbstractBloom:
    """
    The client allows to interact with RedisBloom and use all of
    it's functionality.

    - BF for Bloom Filter
    - CF for Cuckoo Filter
    - CMS for Count-Min Sketch
    - TOPK for TopK Data Structure
    - TDIGEST for estimate rank statistics
    """

    @staticmethod
    def append_items(params, items):  # -> None:
        """Append ITEMS to params."""

    @staticmethod
    def append_error(params, error):  # -> None:
        """Append ERROR to params."""

    @staticmethod
    def append_capacity(params, capacity):  # -> None:
        """Append CAPACITY to params."""

    @staticmethod
    def append_expansion(params, expansion):  # -> None:
        """Append EXPANSION to params."""

    @staticmethod
    def append_no_scale(params, noScale):  # -> None:
        """Append NONSCALING tag to params."""

    @staticmethod
    def append_weights(params, weights):  # -> None:
        """Append WEIGHTS to params."""

    @staticmethod
    def append_no_create(params, noCreate):  # -> None:
        """Append NOCREATE tag to params."""

    @staticmethod
    def append_items_and_increments(params, items, increments):  # -> None:
        """Append pairs of items and increments to params."""

    @staticmethod
    def append_values_and_weights(params, items, weights):  # -> None:
        """Append pairs of items and weights to params."""

    @staticmethod
    def append_max_iterations(params, max_iterations):  # -> None:
        """Append MAXITERATIONS to params."""

    @staticmethod
    def append_bucket_size(params, bucket_size):  # -> None:
        """Append BUCKETSIZE to params."""

class CMSBloom(CMSCommands, AbstractBloom):
    def __init__(self, client, **kwargs) -> None:
        """Create a new RedisBloom client."""

class TOPKBloom(TOPKCommands, AbstractBloom):
    def __init__(self, client, **kwargs) -> None:
        """Create a new RedisBloom client."""

class CFBloom(CFCommands, AbstractBloom):
    def __init__(self, client, **kwargs) -> None:
        """Create a new RedisBloom client."""

class TDigestBloom(TDigestCommands, AbstractBloom):
    def __init__(self, client, **kwargs) -> None:
        """Create a new RedisBloom client."""

class BFBloom(BFCommands, AbstractBloom):
    def __init__(self, client, **kwargs) -> None:
        """Create a new RedisBloom client."""
