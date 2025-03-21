"""
This type stub file was generated by pyright.
"""

import kafka.errors as Errors
from kafka.vendor import six

log = ...
READ_UNCOMMITTED = ...
READ_COMMITTED = ...
ConsumerRecord = ...
CompletedFetch = ...

class NoOffsetForPartitionError(Errors.KafkaError): ...
class RecordTooLargeError(Errors.KafkaError): ...

class Fetcher(six.Iterator):
    DEFAULT_CONFIG = ...
    def __init__(self, client, subscriptions, metrics, **configs) -> None:
        """Initialize a Kafka Message Fetcher.

        Keyword Arguments:
            key_deserializer (callable): Any callable that takes a
                raw message key and returns a deserialized key.
            value_deserializer (callable, optional): Any callable that takes a
                raw message value and returns a deserialized value.
            fetch_min_bytes (int): Minimum amount of data the server should
                return for a fetch request, otherwise wait up to
                fetch_max_wait_ms for more data to accumulate. Default: 1.
            fetch_max_wait_ms (int): The maximum amount of time in milliseconds
                the server will block before answering the fetch request if
                there isn't sufficient data to immediately satisfy the
                requirement given by fetch_min_bytes. Default: 500.
            fetch_max_bytes (int): The maximum amount of data the server should
                return for a fetch request. This is not an absolute maximum, if
                the first message in the first non-empty partition of the fetch
                is larger than this value, the message will still be returned
                to ensure that the consumer can make progress. NOTE: consumer
                performs fetches to multiple brokers in parallel so memory
                usage will depend on the number of brokers containing
                partitions for the topic.
                Supported Kafka version >= 0.10.1.0. Default: 52428800 (50 MB).
            max_partition_fetch_bytes (int): The maximum amount of data
                per-partition the server will return. The maximum total memory
                used for a request = #partitions * max_partition_fetch_bytes.
                This size must be at least as large as the maximum message size
                the server allows or else it is possible for the producer to
                send messages larger than the consumer can fetch. If that
                happens, the consumer can get stuck trying to fetch a large
                message on a certain partition. Default: 1048576.
            check_crcs (bool): Automatically check the CRC32 of the records
                consumed. This ensures no on-the-wire or on-disk corruption to
                the messages occurred. This check adds some overhead, so it may
                be disabled in cases seeking extreme performance. Default: True

        """

    def send_fetches(self):  # -> list[Any]:
        """Send FetchRequests for all assigned partitions that do not already have
        an in-flight fetch or pending fetch data.

        Returns:
            List of Futures: each future resolves to a FetchResponse

        """

    def reset_offsets_if_needed(self, partitions):  # -> None:
        """Lookup and set offsets for any partitions which are awaiting an
        explicit reset.

        Arguments:
            partitions (set of TopicPartitions): the partitions to reset

        """

    def in_flight_fetches(self):  # -> bool:
        """Return True if there are any unprocessed FetchRequests in flight."""

    def update_fetch_positions(self, partitions):  # -> None:
        """Update the fetch positions for the provided partitions.

        Arguments:
            partitions (list of TopicPartitions): partitions to update

        Raises:
            NoOffsetForPartitionError: if no offset is stored for a given
                partition and no reset policy is available

        """

    def get_offsets_by_times(self, timestamps, timeout_ms):  # -> dict[Any, Any] | None:
        ...
    def beginning_offsets(self, partitions, timeout_ms):  # -> dict[Any, Any] | None:
        ...
    def end_offsets(self, partitions, timeout_ms):  # -> dict[Any, Any] | None:
        ...
    def beginning_or_end_offset(self, partitions, timestamp, timeout_ms):  # -> dict[Any, Any] | None:
        ...
    def fetched_records(self, max_records=..., update_offsets=...):  # -> tuple[dict[Any, list[Any]], bool]:
        """Returns previously fetched records and updates consumed offsets.

        Arguments:
            max_records (int): Maximum number of records returned. Defaults
                to max_poll_records configuration.

        Raises:
            OffsetOutOfRangeError: if no subscription offset_reset_strategy
            CorruptRecordException: if message crc validation fails (check_crcs
                must be set to True)
            RecordTooLargeError: if a message is larger than the currently
                configured max_partition_fetch_bytes
            TopicAuthorizationError: if consumer is not authorized to fetch
                messages from the topic

        Returns: (records (dict), partial (bool))
            records: {TopicPartition: [messages]}
            partial: True if records returned did not fully drain any pending
                partition requests. This may be useful for choosing when to
                pipeline additional fetch requests.

        """

    def __iter__(self):  # -> Self:
        ...
    def __next__(self): ...

    class PartitionRecords:
        def __init__(self, fetch_offset, tp, messages) -> None: ...
        def __len__(self):  # -> int:
            ...
        def discard(self):  # -> None:
            ...
        def take(self, n=...):  # -> list[Any]:
            ...

class FetchResponseMetricAggregator:
    """
    Since we parse the message data for each partition from each fetch
    response lazily, fetch-level metrics need to be aggregated as the messages
    from each partition are parsed. This class is used to facilitate this
    incremental aggregation.
    """

    def __init__(self, sensors, partitions) -> None: ...
    def record(self, partition, num_bytes, num_records):  # -> None:
        """
        After each partition is parsed, we update the current metric totals
        with the total bytes and number of records parsed. After all partitions
        have reported, we write the metric.
        """

class FetchManagerMetrics:
    def __init__(self, metrics, prefix) -> None: ...
    def record_topic_fetch_metrics(self, topic, num_bytes, num_records):  # -> None:
        ...
