"""
This type stub file was generated by pyright.
"""

log = ...
ConsumerPair = ...

def is_sublist(source, target):  # -> bool:
    """Checks if one list is a sublist of another.

    Arguments:
      source: the list in which to search for the occurrence of target.
      target: the list to search for as a sublist of source

    Returns:
      true if target is in source; false otherwise

    """

class PartitionMovements:
    """
    This class maintains some data structures to simplify lookup of partition movements among consumers.
    At each point of time during a partition rebalance it keeps track of partition movements
    corresponding to each topic, and also possible movement (in form a ConsumerPair object) for each partition.
    """

    def __init__(self) -> None: ...
    def move_partition(self, partition, old_consumer, new_consumer):  # -> None:
        ...
    def get_partition_to_be_moved(self, partition, old_consumer, new_consumer): ...
    def are_sticky(self):  # -> bool:
        ...
