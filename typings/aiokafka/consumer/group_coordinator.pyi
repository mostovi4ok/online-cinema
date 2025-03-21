"""
This type stub file was generated by pyright.
"""

log = ...
UNKNOWN_OFFSET = ...

class BaseCoordinator:
    def __init__(self, client, subscription, *, exclude_internal_topics=...) -> None: ...

class NoGroupCoordinator(BaseCoordinator):
    """
    When `group_id` consumer option is not used we don't have the functionality
    provided by Coordinator node in Kafka cluster, like committing offsets (
    Kafka based offset storage) or automatic partition assignment between
    consumers. But `GroupCoordinator` class has some other responsibilities,
    that this class takes care of to avoid code duplication, like:

        * Static topic partition assignment when we subscribed to topic.
          Partition changes will be noticed by metadata update and assigned.
        * Pattern topic subscription. New topics will be noticed by metadata
          update and added to subscription.
    """

    def __init__(self, *args, **kw) -> None: ...
    def assign_all_partitions(self, check_unknown=...):  # -> None:
        """Assign all partitions from subscribed topics to this consumer.
        If `check_unknown` we will raise UnknownTopicOrPartitionError if
        subscribed topic is not found in metadata response.
        """

    async def close(self):  # -> None:
        ...
    def check_errors(self):  # -> None:
        ...

class GroupCoordinator(BaseCoordinator):
    """
    GroupCoordinator implements group management for single group member
    by interacting with a designated Kafka broker (the coordinator). Group
    semantics are provided by extending this class.

    From a high level, Kafka's group management protocol consists of the
    following sequence of actions:

    1. Group Registration: Group members register with the coordinator
       providing their own metadata
       (such as the set of topics they are interested in).

    2. Group/Leader Selection: The coordinator (one of Kafka nodes) select
       the members of the group and chooses one member (one of client's)
       as the leader.

    3. State Assignment: The leader receives metadata for all members and
       assigns partitions to them.

    4. Group Stabilization: Each member receives the state assigned by the
       leader and begins processing.
       Between each phase coordinator awaits all clients to respond. If some
       do not respond in time - it will revoke their membership

    NOTE: Try to maintain same log messages and behaviour as Java and
          kafka-python clients:

        https://github.com/apache/kafka/blob/0.10.1.1/clients/src/main/java/\
          org/apache/kafka/clients/consumer/internals/AbstractCoordinator.java
        https://github.com/apache/kafka/blob/0.10.1.1/clients/src/main/java/\
          org/apache/kafka/clients/consumer/internals/ConsumerCoordinator.java
    """

    def __init__(
        self,
        client,
        subscription,
        *,
        group_id=...,
        group_instance_id=...,
        session_timeout_ms=...,
        heartbeat_interval_ms=...,
        retry_backoff_ms=...,
        enable_auto_commit=...,
        auto_commit_interval_ms=...,
        assignors=...,
        exclude_internal_topics=...,
        max_poll_interval_ms=...,
        rebalance_timeout_ms=...,
    ) -> None:
        """Initialize the coordination manager.

        Parameters (see AIOKafkaConsumer)
        """

    def check_errors(self):  # -> None:
        """Check if coordinator is well and no authorization or unrecoverable
        errors occurred
        """

    async def close(self):  # -> None:
        """Close the coordinator, leave the current group
        and reset local generation/memberId.
        """

    def maybe_leave_group(self):  # -> Task[None]:
        ...
    def coordinator_dead(self):  # -> None:
        """Mark the current coordinator as dead.
        NOTE: this will not force a group rejoin. If new coordinator is able to
        recognize this member we will just continue with current generation.
        """

    def reset_generation(self):  # -> None:
        """Coordinator did not recognize either generation or member_id. Will
        need to re-join the group.
        """

    def request_rejoin(self):  # -> None:
        ...
    def need_rejoin(self, subscription):  # -> bool:
        """Check whether the group should be rejoined

        Returns:
            bool: True if consumer should rejoin group, False otherwise

        """

    async def ensure_coordinator_known(self):  # -> None:
        """Block until the coordinator for this group is known."""

    async def ensure_active_group(self, subscription, prev_assignment):  # -> None:
        ...
    def start_commit_offsets_refresh_task(self, assignment):  # -> None:
        ...
    async def commit_offsets(self, assignment, offsets):  # -> None:
        """Commit specific offsets

        Arguments:
            offsets (dict {TopicPartition: OffsetAndMetadata}): what to commit

        Raises KafkaError on failure

        """

    async def fetch_committed_offsets(self, partitions):  # -> dict[Any, Any]:
        """Fetch the current committed offsets for specified partitions

        Arguments:
            partitions (list of TopicPartition): partitions to fetch

        Returns:
            dict: {TopicPartition: OffsetAndMetadata}

        """

class CoordinatorGroupRebalance:
    """An adapter, that encapsulates rebalance logic and will have a copy of
    assigned topics, so we can detect assignment changes. This includes
    subscription pattern changes.

    On how to handle cases read in https://cwiki.apache.org/confluence/\
            display/KAFKA/Kafka+Client-side+Assignment+Proposal
    """

    def __init__(
        self, coordinator, group_id, coordinator_id, subscription, assignors, session_timeout_ms, retry_backoff_ms
    ) -> None: ...
    async def perform_group_join(self):  # -> tuple[Any, Any] | None:
        """Join the group and return the assignment for the next generation.

        This function handles both JoinGroup and SyncGroup, delegating to
        _perform_assignment() if elected as leader by the coordinator node.

        Returns encoded-bytes assignment returned from the group leader
        """
