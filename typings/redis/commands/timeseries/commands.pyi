"""
This type stub file was generated by pyright.
"""

from redis.typing import KeyT, Number

ADD_CMD = ...
ALTER_CMD = ...
CREATERULE_CMD = ...
CREATE_CMD = ...
DECRBY_CMD = ...
DELETERULE_CMD = ...
DEL_CMD = ...
GET_CMD = ...
INCRBY_CMD = ...
INFO_CMD = ...
MADD_CMD = ...
MGET_CMD = ...
MRANGE_CMD = ...
MREVRANGE_CMD = ...
QUERYINDEX_CMD = ...
RANGE_CMD = ...
REVRANGE_CMD = ...

class TimeSeriesCommands:
    """RedisTimeSeries Commands."""

    def create(
        self,
        key: KeyT,
        retention_msecs: int | None = ...,
        uncompressed: bool | None = ...,
        labels: dict[str, str] | None = ...,
        chunk_size: int | None = ...,
        duplicate_policy: str | None = ...,
        ignore_max_time_diff: int | None = ...,
        ignore_max_val_diff: Number | None = ...,
    ):
        """
        Create a new time-series.

        For more information see https://redis.io/commands/ts.create/

        Args:
            key:
                The time-series key.
            retention_msecs:
                Maximum age for samples, compared to the highest reported timestamp in
                milliseconds. If `None` or `0` is passed, the series is not trimmed at
                all.
            uncompressed:
                Changes data storage from compressed (default) to uncompressed.
            labels:
                A dictionary of label-value pairs that represent metadata labels of the
                key.
            chunk_size:
                Memory size, in bytes, allocated for each data chunk. Must be a multiple
                of 8 in the range `[48..1048576]`. In earlier versions of the module the
                minimum value was different.
            duplicate_policy:
                Policy for handling multiple samples with identical timestamps. Can be
                one of:
                    - 'block': An error will occur and the new value will be ignored.
                    - 'first': Ignore the new value.
                    - 'last': Override with the latest value.
                    - 'min': Only override if the value is lower than the existing
                      value.
                    - 'max': Only override if the value is higher than the existing
                      value.
                    - 'sum': If a previous sample exists, add the new sample to it so
                      that the updated value is equal to (previous + new). If no
                      previous sample exists, set the updated value equal to the new
                      value.
            ignore_max_time_diff:
                A non-negative integer value, in milliseconds, that sets an ignore
                threshold for added timestamps. If the difference between the last
                timestamp and the new timestamp is lower than this threshold, the new
                entry is ignored. Only applicable if `duplicate_policy` is set to
                `last`, and if `ignore_max_val_diff` is also set. Available since
                RedisTimeSeries version 1.12.0.
            ignore_max_val_diff:
                A non-negative floating point value, that sets an ignore threshold for
                added values. If the difference between the last value and the new value
                is lower than this threshold, the new entry is ignored. Only applicable
                if `duplicate_policy` is set to `last`, and if `ignore_max_time_diff` is
                also set. Available since RedisTimeSeries version 1.12.0.

        """

    def alter(
        self,
        key: KeyT,
        retention_msecs: int | None = ...,
        labels: dict[str, str] | None = ...,
        chunk_size: int | None = ...,
        duplicate_policy: str | None = ...,
        ignore_max_time_diff: int | None = ...,
        ignore_max_val_diff: Number | None = ...,
    ):
        """
        Update an existing time series.

        For more information see https://redis.io/commands/ts.alter/

        Args:
            key:
                The time-series key.
            retention_msecs:
                Maximum age for samples, compared to the highest reported timestamp in
                milliseconds. If `None` or `0` is passed, the series is not trimmed at
                all.
            labels:
                A dictionary of label-value pairs that represent metadata labels of the
                key.
            chunk_size:
                Memory size, in bytes, allocated for each data chunk. Must be a multiple
                of 8 in the range `[48..1048576]`. In earlier versions of the module the
                minimum value was different. Changing this value does not affect
                existing chunks.
            duplicate_policy:
                Policy for handling multiple samples with identical timestamps. Can be
                one of:
                    - 'block': An error will occur and the new value will be ignored.
                    - 'first': Ignore the new value.
                    - 'last': Override with the latest value.
                    - 'min': Only override if the value is lower than the existing
                      value.
                    - 'max': Only override if the value is higher than the existing
                      value.
                    - 'sum': If a previous sample exists, add the new sample to it so
                      that the updated value is equal to (previous + new). If no
                      previous sample exists, set the updated value equal to the new
                      value.
            ignore_max_time_diff:
                A non-negative integer value, in milliseconds, that sets an ignore
                threshold for added timestamps. If the difference between the last
                timestamp and the new timestamp is lower than this threshold, the new
                entry is ignored. Only applicable if `duplicate_policy` is set to
                `last`, and if `ignore_max_val_diff` is also set. Available since
                RedisTimeSeries version 1.12.0.
            ignore_max_val_diff:
                A non-negative floating point value, that sets an ignore threshold for
                added values. If the difference between the last value and the new value
                is lower than this threshold, the new entry is ignored. Only applicable
                if `duplicate_policy` is set to `last`, and if `ignore_max_time_diff` is
                also set. Available since RedisTimeSeries version 1.12.0.

        """

    def add(
        self,
        key: KeyT,
        timestamp: int | str,
        value: Number,
        retention_msecs: int | None = ...,
        uncompressed: bool | None = ...,
        labels: dict[str, str] | None = ...,
        chunk_size: int | None = ...,
        duplicate_policy: str | None = ...,
        ignore_max_time_diff: int | None = ...,
        ignore_max_val_diff: Number | None = ...,
        on_duplicate: str | None = ...,
    ):
        """
        Append a sample to a time series. When the specified key does not exist, a new
        time series is created.

        For more information see https://redis.io/commands/ts.add/

        Args:
            key:
                The time-series key.
            timestamp:
                Timestamp of the sample. `*` can be used for automatic timestamp (using
                the system clock).
            value:
                Numeric data value of the sample.
            retention_msecs:
                Maximum age for samples, compared to the highest reported timestamp in
                milliseconds. If `None` or `0` is passed, the series is not trimmed at
                all.
            uncompressed:
                Changes data storage from compressed (default) to uncompressed.
            labels:
                A dictionary of label-value pairs that represent metadata labels of the
                key.
            chunk_size:
                Memory size, in bytes, allocated for each data chunk. Must be a multiple
                of 8 in the range `[48..1048576]`. In earlier versions of the module the
                minimum value was different.
            duplicate_policy:
                Policy for handling multiple samples with identical timestamps. Can be
                one of:
                    - 'block': An error will occur and the new value will be ignored.
                    - 'first': Ignore the new value.
                    - 'last': Override with the latest value.
                    - 'min': Only override if the value is lower than the existing
                      value.
                    - 'max': Only override if the value is higher than the existing
                      value.
                    - 'sum': If a previous sample exists, add the new sample to it so
                      that the updated value is equal to (previous + new). If no
                      previous sample exists, set the updated value equal to the new
                      value.
            ignore_max_time_diff:
                A non-negative integer value, in milliseconds, that sets an ignore
                threshold for added timestamps. If the difference between the last
                timestamp and the new timestamp is lower than this threshold, the new
                entry is ignored. Only applicable if `duplicate_policy` is set to
                `last`, and if `ignore_max_val_diff` is also set. Available since
                RedisTimeSeries version 1.12.0.
            ignore_max_val_diff:
                A non-negative floating point value, that sets an ignore threshold for
                added values. If the difference between the last value and the new value
                is lower than this threshold, the new entry is ignored. Only applicable
                if `duplicate_policy` is set to `last`, and if `ignore_max_time_diff` is
                also set. Available since RedisTimeSeries version 1.12.0.
            on_duplicate:
                Use a specific duplicate policy for the specified timestamp. Overrides
                the duplicate policy set by `duplicate_policy`.

        """

    def madd(self, ktv_tuples: list[tuple[KeyT, int | str, Number]]):
        """
        Append new samples to one or more time series.

        Each time series must already exist.

        The method expects a list of tuples. Each tuple should contain three elements:
        (`key`, `timestamp`, `value`). The `value` will be appended to the time series
        identified by 'key', at the given 'timestamp'.

        For more information see https://redis.io/commands/ts.madd/

        Args:
            ktv_tuples:
                A list of tuples, where each tuple contains:
                    - `key`: The key of the time series.
                    - `timestamp`: The timestamp at which the value should be appended.
                    - `value`: The value to append to the time series.

        Returns:
            A list that contains, for each sample, either the timestamp that was used,
            or an error, if the sample could not be added.

        """

    def incrby(
        self,
        key: KeyT,
        value: Number,
        timestamp: int | str | None = ...,
        retention_msecs: int | None = ...,
        uncompressed: bool | None = ...,
        labels: dict[str, str] | None = ...,
        chunk_size: int | None = ...,
        duplicate_policy: str | None = ...,
        ignore_max_time_diff: int | None = ...,
        ignore_max_val_diff: Number | None = ...,
    ):
        """
        Increment the latest sample's of a series. When the specified key does not
        exist, a new time series is created.

        This command can be used as a counter or gauge that automatically gets history
        as a time series.

        For more information see https://redis.io/commands/ts.incrby/

        Args:
            key:
                The time-series key.
            value:
                Numeric value to be added (addend).
            timestamp:
                Timestamp of the sample. `*` can be used for automatic timestamp (using
                the system clock). `timestamp` must be equal to or higher than the
                maximum existing timestamp in the series. When equal, the value of the
                sample with the maximum existing timestamp is increased. If it is
                higher, a new sample with a timestamp set to `timestamp` is created, and
                its value is set to the value of the sample with the maximum existing
                timestamp plus the addend.
            retention_msecs:
                Maximum age for samples, compared to the highest reported timestamp in
                milliseconds. If `None` or `0` is passed, the series is not trimmed at
                all.
            uncompressed:
                Changes data storage from compressed (default) to uncompressed.
            labels:
                A dictionary of label-value pairs that represent metadata labels of the
                key.
            chunk_size:
                Memory size, in bytes, allocated for each data chunk. Must be a multiple
                of 8 in the range `[48..1048576]`. In earlier versions of the module the
                minimum value was different.
            duplicate_policy:
                Policy for handling multiple samples with identical timestamps. Can be
                one of:
                    - 'block': An error will occur and the new value will be ignored.
                    - 'first': Ignore the new value.
                    - 'last': Override with the latest value.
                    - 'min': Only override if the value is lower than the existing
                      value.
                    - 'max': Only override if the value is higher than the existing
                      value.
                    - 'sum': If a previous sample exists, add the new sample to it so
                      that the updated value is equal to (previous + new). If no
                      previous sample exists, set the updated value equal to the new
                      value.
            ignore_max_time_diff:
                A non-negative integer value, in milliseconds, that sets an ignore
                threshold for added timestamps. If the difference between the last
                timestamp and the new timestamp is lower than this threshold, the new
                entry is ignored. Only applicable if `duplicate_policy` is set to
                `last`, and if `ignore_max_val_diff` is also set. Available since
                RedisTimeSeries version 1.12.0.
            ignore_max_val_diff:
                A non-negative floating point value, that sets an ignore threshold for
                added values. If the difference between the last value and the new value
                is lower than this threshold, the new entry is ignored. Only applicable
                if `duplicate_policy` is set to `last`, and if `ignore_max_time_diff` is
                also set. Available since RedisTimeSeries version 1.12.0.

        Returns:
            The timestamp of the sample that was modified or added.

        """

    def decrby(
        self,
        key: KeyT,
        value: Number,
        timestamp: int | str | None = ...,
        retention_msecs: int | None = ...,
        uncompressed: bool | None = ...,
        labels: dict[str, str] | None = ...,
        chunk_size: int | None = ...,
        duplicate_policy: str | None = ...,
        ignore_max_time_diff: int | None = ...,
        ignore_max_val_diff: Number | None = ...,
    ):
        """
        Decrement the latest sample's of a series. When the specified key does not
        exist, a new time series is created.

        This command can be used as a counter or gauge that automatically gets history
        as a time series.

        For more information see https://redis.io/commands/ts.decrby/

        Args:
            key:
                The time-series key.
            value:
                Numeric value to subtract (subtrahend).
            timestamp:
                Timestamp of the sample. `*` can be used for automatic timestamp (using
                the system clock). `timestamp` must be equal to or higher than the
                maximum existing timestamp in the series. When equal, the value of the
                sample with the maximum existing timestamp is decreased. If it is
                higher, a new sample with a timestamp set to `timestamp` is created, and
                its value is set to the value of the sample with the maximum existing
                timestamp minus subtrahend.
            retention_msecs:
                Maximum age for samples, compared to the highest reported timestamp in
                milliseconds. If `None` or `0` is passed, the series is not trimmed at
                all.
            uncompressed:
                Changes data storage from compressed (default) to uncompressed.
            labels:
                A dictionary of label-value pairs that represent metadata labels of the
                key.
            chunk_size:
                Memory size, in bytes, allocated for each data chunk. Must be a multiple
                of 8 in the range `[48..1048576]`. In earlier versions of the module the
                minimum value was different.
            duplicate_policy:
                Policy for handling multiple samples with identical timestamps. Can be
                one of:
                    - 'block': An error will occur and the new value will be ignored.
                    - 'first': Ignore the new value.
                    - 'last': Override with the latest value.
                    - 'min': Only override if the value is lower than the existing
                      value.
                    - 'max': Only override if the value is higher than the existing
                      value.
                    - 'sum': If a previous sample exists, add the new sample to it so
                      that the updated value is equal to (previous + new). If no
                      previous sample exists, set the updated value equal to the new
                      value.
            ignore_max_time_diff:
                A non-negative integer value, in milliseconds, that sets an ignore
                threshold for added timestamps. If the difference between the last
                timestamp and the new timestamp is lower than this threshold, the new
                entry is ignored. Only applicable if `duplicate_policy` is set to
                `last`, and if `ignore_max_val_diff` is also set. Available since
                RedisTimeSeries version 1.12.0.
            ignore_max_val_diff:
                A non-negative floating point value, that sets an ignore threshold for
                added values. If the difference between the last value and the new value
                is lower than this threshold, the new entry is ignored. Only applicable
                if `duplicate_policy` is set to `last`, and if `ignore_max_time_diff` is
                also set. Available since RedisTimeSeries version 1.12.0.

        Returns:
            The timestamp of the sample that was modified or added.

        """

    def delete(self, key: KeyT, from_time: int, to_time: int):
        """
        Delete all samples between two timestamps for a given time series.

        The given timestamp interval is closed (inclusive), meaning that samples whose
        timestamp equals `from_time` or `to_time` are also deleted.

        For more information see https://redis.io/commands/ts.del/

        Args:
            key:
                The time-series key.
            from_time:
                Start timestamp for the range deletion.
            to_time:
                End timestamp for the range deletion.

        Returns:
            The number of samples deleted.

        """

    def createrule(
        self,
        source_key: KeyT,
        dest_key: KeyT,
        aggregation_type: str,
        bucket_size_msec: int,
        align_timestamp: int | None = ...,
    ):
        """
        Create a compaction rule from values added to `source_key` into `dest_key`.

        For more information see https://redis.io/commands/ts.createrule/

        Args:
            source_key:
                Key name for source time series.
            dest_key:
                Key name for destination (compacted) time series.
            aggregation_type:
                Aggregation type: One of the following:
                [`avg`, `sum`, `min`, `max`, `range`, `count`, `first`, `last`, `std.p`,
                `std.s`, `var.p`, `var.s`, `twa`]
            bucket_size_msec:
                Duration of each bucket, in milliseconds.
            align_timestamp:
                Assure that there is a bucket that starts at exactly align_timestamp and
                align all other buckets accordingly.

        """

    def deleterule(self, source_key: KeyT, dest_key: KeyT):
        """
        Delete a compaction rule from `source_key` to `dest_key`.

        For more information see https://redis.io/commands/ts.deleterule/
        """

    def range(
        self,
        key: KeyT,
        from_time: int | str,
        to_time: int | str,
        count: int | None = ...,
        aggregation_type: str | None = ...,
        bucket_size_msec: int | None = ...,
        filter_by_ts: list[int] | None = ...,
        filter_by_min_value: int | None = ...,
        filter_by_max_value: int | None = ...,
        align: int | str | None = ...,
        latest: bool | None = ...,
        bucket_timestamp: str | None = ...,
        empty: bool | None = ...,
    ):
        """
        Query a range in forward direction for a specific time-series.

        For more information see https://redis.io/commands/ts.range/

        Args:
            key:
                Key name for timeseries.
            from_time:
                Start timestamp for the range query. `-` can be used to express the
                minimum possible timestamp (0).
            to_time:
                End timestamp for range query, `+` can be used to express the maximum
                possible timestamp.
            count:
                Limits the number of returned samples.
            aggregation_type:
                Optional aggregation type. Can be one of [`avg`, `sum`, `min`, `max`,
                `range`, `count`, `first`, `last`, `std.p`, `std.s`, `var.p`, `var.s`,
                `twa`]
            bucket_size_msec:
                Time bucket for aggregation in milliseconds.
            filter_by_ts:
                List of timestamps to filter the result by specific timestamps.
            filter_by_min_value:
                Filter result by minimum value (must mention also
                `filter by_max_value`).
            filter_by_max_value:
                Filter result by maximum value (must mention also
                `filter by_min_value`).
            align:
                Timestamp for alignment control for aggregation.
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest possibly partial bucket.
            bucket_timestamp:
                Controls how bucket timestamps are reported. Can be one of [`-`, `low`,
                `+`, `high`, `~`, `mid`].
            empty:
                Reports aggregations for empty buckets.

        """

    def revrange(
        self,
        key: KeyT,
        from_time: int | str,
        to_time: int | str,
        count: int | None = ...,
        aggregation_type: str | None = ...,
        bucket_size_msec: int | None = ...,
        filter_by_ts: list[int] | None = ...,
        filter_by_min_value: int | None = ...,
        filter_by_max_value: int | None = ...,
        align: int | str | None = ...,
        latest: bool | None = ...,
        bucket_timestamp: str | None = ...,
        empty: bool | None = ...,
    ):
        """
        Query a range in reverse direction for a specific time-series.

        **Note**: This command is only available since RedisTimeSeries >= v1.4

        For more information see https://redis.io/commands/ts.revrange/

        Args:
            key:
                Key name for timeseries.
            from_time:
                Start timestamp for the range query. `-` can be used to express the
                minimum possible timestamp (0).
            to_time:
                End timestamp for range query, `+` can be used to express the maximum
                possible timestamp.
            count:
                Limits the number of returned samples.
            aggregation_type:
                Optional aggregation type. Can be one of [`avg`, `sum`, `min`, `max`,
                `range`, `count`, `first`, `last`, `std.p`, `std.s`, `var.p`, `var.s`,
                `twa`]
            bucket_size_msec:
                Time bucket for aggregation in milliseconds.
            filter_by_ts:
                List of timestamps to filter the result by specific timestamps.
            filter_by_min_value:
                Filter result by minimum value (must mention also
                `filter_by_max_value`).
            filter_by_max_value:
                Filter result by maximum value (must mention also
                `filter_by_min_value`).
            align:
                Timestamp for alignment control for aggregation.
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest possibly partial bucket.
            bucket_timestamp:
                Controls how bucket timestamps are reported. Can be one of [`-`, `low`,
                `+`, `high`, `~`, `mid`].
            empty:
                Reports aggregations for empty buckets.

        """

    def mrange(
        self,
        from_time: int | str,
        to_time: int | str,
        filters: list[str],
        count: int | None = ...,
        aggregation_type: str | None = ...,
        bucket_size_msec: int | None = ...,
        with_labels: bool | None = ...,
        filter_by_ts: list[int] | None = ...,
        filter_by_min_value: int | None = ...,
        filter_by_max_value: int | None = ...,
        groupby: str | None = ...,
        reduce: str | None = ...,
        select_labels: list[str] | None = ...,
        align: int | str | None = ...,
        latest: bool | None = ...,
        bucket_timestamp: str | None = ...,
        empty: bool | None = ...,
    ):
        """
        Query a range across multiple time-series by filters in forward direction.

        For more information see https://redis.io/commands/ts.mrange/

        Args:
            from_time:
                Start timestamp for the range query. `-` can be used to express the
                minimum possible timestamp (0).
            to_time:
                End timestamp for range query, `+` can be used to express the maximum
                possible timestamp.
            filters:
                Filter to match the time-series labels.
            count:
                Limits the number of returned samples.
            aggregation_type:
                Optional aggregation type. Can be one of [`avg`, `sum`, `min`, `max`,
                `range`, `count`, `first`, `last`, `std.p`, `std.s`, `var.p`, `var.s`,
                `twa`]
            bucket_size_msec:
                Time bucket for aggregation in milliseconds.
            with_labels:
                Include in the reply all label-value pairs representing metadata labels
                of the time series.
            filter_by_ts:
                List of timestamps to filter the result by specific timestamps.
            filter_by_min_value:
                Filter result by minimum value (must mention also
                `filter_by_max_value`).
            filter_by_max_value:
                Filter result by maximum value (must mention also
                `filter_by_min_value`).
            groupby:
                Grouping by fields the results (must mention also `reduce`).
            reduce:
                Applying reducer functions on each group. Can be one of [`avg` `sum`,
                `min`, `max`, `range`, `count`, `std.p`, `std.s`, `var.p`, `var.s`].
            select_labels:
                Include in the reply only a subset of the key-value pair labels of a
                series.
            align:
                Timestamp for alignment control for aggregation.
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest possibly partial bucket.
            bucket_timestamp:
                Controls how bucket timestamps are reported. Can be one of [`-`, `low`,
                `+`, `high`, `~`, `mid`].
            empty:
                Reports aggregations for empty buckets.

        """

    def mrevrange(
        self,
        from_time: int | str,
        to_time: int | str,
        filters: list[str],
        count: int | None = ...,
        aggregation_type: str | None = ...,
        bucket_size_msec: int | None = ...,
        with_labels: bool | None = ...,
        filter_by_ts: list[int] | None = ...,
        filter_by_min_value: int | None = ...,
        filter_by_max_value: int | None = ...,
        groupby: str | None = ...,
        reduce: str | None = ...,
        select_labels: list[str] | None = ...,
        align: int | str | None = ...,
        latest: bool | None = ...,
        bucket_timestamp: str | None = ...,
        empty: bool | None = ...,
    ):
        """
        Query a range across multiple time-series by filters in reverse direction.

        For more information see https://redis.io/commands/ts.mrevrange/

        Args:
            from_time:
                Start timestamp for the range query. '-' can be used to express the
                minimum possible timestamp (0).
            to_time:
                End timestamp for range query, '+' can be used to express the maximum
                possible timestamp.
            filters:
                Filter to match the time-series labels.
            count:
                Limits the number of returned samples.
            aggregation_type:
                Optional aggregation type. Can be one of [`avg`, `sum`, `min`, `max`,
                `range`, `count`, `first`, `last`, `std.p`, `std.s`, `var.p`, `var.s`,
                `twa`].
            bucket_size_msec:
                Time bucket for aggregation in milliseconds.
            with_labels:
                Include in the reply all label-value pairs representing metadata labels
                of the time series.
            filter_by_ts:
                List of timestamps to filter the result by specific timestamps.
            filter_by_min_value:
                Filter result by minimum value (must mention also
                `filter_by_max_value`).
            filter_by_max_value:
                Filter result by maximum value (must mention also
                `filter_by_min_value`).
            groupby:
                Grouping by fields the results (must mention also `reduce`).
            reduce:
                Applying reducer functions on each group. Can be one of [`avg` `sum`,
                `min`, `max`, `range`, `count`, `std.p`, `std.s`, `var.p`, `var.s`].
            select_labels:
                Include in the reply only a subset of the key-value pair labels of a
                series.
            align:
                Timestamp for alignment control for aggregation.
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest possibly partial bucket.
            bucket_timestamp:
                Controls how bucket timestamps are reported. Can be one of [`-`, `low`,
                `+`, `high`, `~`, `mid`].
            empty:
                Reports aggregations for empty buckets.

        """

    def get(self, key: KeyT, latest: bool | None = ...):
        """
        Get the last sample of `key`.

        For more information see https://redis.io/commands/ts.get/

        Args:
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest (possibly partial) bucket.

        """

    def mget(
        self,
        filters: list[str],
        with_labels: bool | None = ...,
        select_labels: list[str] | None = ...,
        latest: bool | None = ...,
    ):
        """
        Get the last samples matching the specific `filter`.

        For more information see https://redis.io/commands/ts.mget/

        Args:
            filters:
                Filter to match the time-series labels.
            with_labels:
                Include in the reply all label-value pairs representing metadata labels
                of the time series.
            select_labels:
                Include in the reply only a subset of the key-value pair labels o the
                time series.
            latest:
                Used when a time series is a compaction, reports the compacted value of
                the latest possibly partial bucket.

        """

    def info(self, key: KeyT):
        """
        Get information of `key`.

        For more information see https://redis.io/commands/ts.info/
        """

    def queryindex(self, filters: list[str]):
        """
        Get all time series keys matching the `filter` list.

        For more information see https://redis.io/commands/ts.queryindex/
        """
