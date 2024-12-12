"""
This type stub file was generated by pyright.
"""

class TSInfo:
    """
    Hold information and statistics on the time-series.
    Can be created using ``tsinfo`` command
    https://redis.io/docs/latest/commands/ts.info/
    """

    rules = ...
    labels = ...
    sourceKey = ...
    chunk_count = ...
    memory_usage = ...
    total_samples = ...
    retention_msecs = ...
    last_time_stamp = ...
    first_time_stamp = ...
    max_samples_per_chunk = ...
    chunk_size = ...
    duplicate_policy = ...
    def __init__(self, args) -> None:
        """
        Hold information and statistics on the time-series.

        The supported params that can be passed as args:

        rules:
            A list of compaction rules of the time series.
        sourceKey:
            Key name for source time series in case the current series
            is a target of a rule.
        chunkCount:
            Number of Memory Chunks used for the time series.
        memoryUsage:
            Total number of bytes allocated for the time series.
        totalSamples:
            Total number of samples in the time series.
        labels:
            A list of label-value pairs that represent the metadata
            labels of the time series.
        retentionTime:
            Retention time, in milliseconds, for the time series.
        lastTimestamp:
            Last timestamp present in the time series.
        firstTimestamp:
            First timestamp present in the time series.
        maxSamplesPerChunk:
            Deprecated.
        chunkSize:
            Amount of memory, in bytes, allocated for data.
        duplicatePolicy:
            Policy that will define handling of duplicate samples.

        Can read more about on
        https://redis.io/docs/latest/develop/data-types/timeseries/configuration/#duplicate_policy
        """

    def get(self, item):  # -> Any | None:
        ...
    def __getitem__(self, item):  # -> Any:
        ...
