"""
This type stub file was generated by pyright.
"""

from collections.abc import Sequence

class BatchBuilder:
    def __init__(
        self, magic, batch_size, compression_type, *, is_transactional, key_serializer=..., value_serializer=...
    ) -> None: ...
    def append(
        self, *, timestamp, key, value, headers: Sequence = ...
    ):  # -> DefaultRecordMetadataProtocol | LegacyRecordMetadataProtocol | None:
        """Add a message to the batch.

        Arguments:
            timestamp (float or None): epoch timestamp in seconds. If None,
                the timestamp will be set to the current time. If submitting to
                an 0.8.x or 0.9.x broker, the timestamp will be ignored.
            key (bytes or None): the message key. `key` and `value` may not
                both be None.
            value (bytes or None): the message value. `key` and `value` may not
                both be None.

        Returns:
            If the message was successfully added, returns a metadata object
            with crc, offset, size, and timestamp fields. If the batch is full
            or closed, returns None.

        """

    def close(self):  # -> None:
        """Close the batch to further updates.

        Closing the batch before submitting to the producer ensures that no
        messages are added via the ``producer.send()`` interface. To gracefully
        support both the batch and individual message interfaces, leave the
        batch open. For complete control over the batch's contents, close
        before submission. Closing a batch has no effect on when it's sent to
        the broker.

        A batch may not be reopened after it's closed.
        """

    def size(self):  # -> int:
        """Get the size of batch in bytes."""

    def record_count(self):  # -> int:
        """Get the number of records in the batch."""

class MessageBatch:
    """This class incapsulate operations with batch of produce messages"""

    def __init__(self, tp, builder, ttl) -> None: ...
    @property
    def tp(self):  # -> Any:
        ...
    @property
    def record_count(self): ...
    def append(self, key, value, timestamp_ms, _create_future=..., headers: Sequence = ...):  # -> None:
        """Append message (key and value) to batch

        Returns:
            None if batch is full
              or
            asyncio.Future that will resolved when message is delivered

        """

    def done(self, base_offset, timestamp=..., log_start_offset=..., _record_metadata_class=...):  # -> None:
        """Resolve all pending futures"""

    def done_noack(self):  # -> None:
        """Resolve all pending futures to None"""

    def failure(self, exception):  # -> None:
        ...
    async def wait_drain(self, timeout=...):  # -> None:
        """Wait until all message from this batch is processed"""

    def expired(self):  # -> bool:
        """Check that batch is expired or not"""

    def drain_ready(self):  # -> None:
        """Compress batch to be ready for send"""

    def reset_drain(self):  # -> None:
        """Reset drain waiter, until we will do another retry"""

    def set_producer_state(self, producer_id, producer_epoch, base_sequence):  # -> None:
        ...
    def get_data_buffer(self): ...
    def is_empty(self): ...
    @property
    def retry_count(self):  # -> int:
        ...

class MessageAccumulator:
    """Accumulator of messages batched by topic-partition

    Producer adds messages to this accumulator and a background send task
    gets batches per nodes to process it.
    """

    def __init__(self, cluster, batch_size, compression_type, batch_ttl, *, txn_manager=..., loop=...) -> None: ...
    def set_api_version(self, api_version):  # -> None:
        ...
    async def flush(self):  # -> None:
        ...
    async def flush_for_commit(self):  # -> None:
        ...
    def fail_all(self, exception):  # -> None:
        ...
    async def close(self):  # -> None:
        ...
    async def add_message(self, tp, key, value, timeout, timestamp_ms=..., headers: Sequence = ...):
        """Add message to batch by topic-partition
        If batch is already full this method waits (`timeout` seconds maximum)
        until batch is drained by send task
        """

    def data_waiter(self):  # -> Future[Any]:
        """Return waiter future that will be resolved when accumulator contain
        some data for drain
        """

    def reenqueue(self, batch):  # -> None:
        ...
    def drain_by_nodes(self, ignore_nodes, muted_partitions=...):  # -> tuple[defaultdict[Any, dict[Any, Any]], bool]:
        """Group batches by leader to partition nodes."""

    def create_builder(self, key_serializer=..., value_serializer=...):  # -> BatchBuilder:
        ...
    async def add_batch(self, builder, tp, timeout):  # -> Future[Any]:
        """Add BatchBuilder to queue by topic-partition.

        Arguments:
            builder (BatchBuilder): batch object to enqueue.
            tp (TopicPartition): topic and partition to enqueue this batch for.
            timeout (int): time in seconds to wait for a free slot in the batch
                queue.

        Returns:
            MessageBatch: delivery wrapper around the BatchBuilder object.

        Raises:
            aiokafka.errors.ProducerClosed: the accumulator has already been
                closed and flushed.
            aiokafka.errors.KafkaTimeoutError: the batch could not be added
                within the specified timeout.

        """
