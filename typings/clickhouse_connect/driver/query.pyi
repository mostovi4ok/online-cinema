"""
This type stub file was generated by pyright.
"""

from collections.abc import Generator, Sequence
from datetime import tzinfo
from io import IOBase
from typing import Any

from clickhouse_connect.driver.common import StreamContext
from clickhouse_connect.driver.context import BaseQueryContext
from clickhouse_connect.driver.external import ExternalData
from clickhouse_connect.driver.types import Closable, Matrix

logger = ...
commands = ...
limit_re = ...
select_re = ...
insert_re = ...
command_re = ...
external_bind_re = ...

class QueryContext(BaseQueryContext):
    """
    Argument/parameter object for queries.  This context is used to set thread/query specific formats
    """

    def __init__(
        self,
        query: str | bytes = ...,
        parameters: dict[str, Any] | None = ...,
        settings: dict[str, Any] | None = ...,
        query_formats: dict[str, str] | None = ...,
        column_formats: dict[str, str | dict[str, str]] | None = ...,
        encoding: str | None = ...,
        server_tz: tzinfo = ...,
        use_none: bool | None = ...,
        column_oriented: bool | None = ...,
        use_numpy: bool | None = ...,
        max_str_len: int | None = ...,
        query_tz: str | tzinfo | None = ...,
        column_tzs: dict[str, str | tzinfo] | None = ...,
        use_extended_dtypes: bool | None = ...,
        as_pandas: bool = ...,
        streaming: bool = ...,
        apply_server_tz: bool = ...,
        external_data: ExternalData | None = ...,
    ) -> None:
        """
        Initializes various configuration settings for the query context

        :param query:  Query string with Python style format value replacements
        :param parameters: Optional dictionary of substitution values
        :param settings: Optional ClickHouse settings for the query
        :param query_formats: Optional dictionary of query formats with the key of a ClickHouse type name
          (with * wildcards) and a value of valid query formats for those types.
          The value 'encoding' can be sent to change the expected encoding for this query, with a value of
          the desired encoding such as `latin-1`
        :param column_formats: Optional dictionary of column specific formats.  The key is the column name,
          The value is either the format for the data column (such as 'string' for a UUID column) or a
          second level "format" dictionary of a ClickHouse type name and a value of query formats.  This
          secondary dictionary can be used for nested column types such as Tuples or Maps
        :param encoding: Optional string encoding for this query, such as 'latin-1'
        :param column_formats: Optional dictionary
        :param use_none: Use a Python None for ClickHouse NULL values in nullable columns.  Otherwise the default
          value of the column (such as 0 for numbers) will be returned in the result_set
        :param max_str_len Limit returned ClickHouse String values to this length, which allows a Numpy
          structured array even with ClickHouse variable length String columns.  If 0, Numpy arrays for
          String columns will always be object arrays
        :param query_tz  Either a string or a pytz tzinfo object.  (Strings will be converted to tzinfo objects).
          Values for any DateTime or DateTime64 column in the query will be converted to Python datetime.datetime
          objects with the selected timezone
        :param column_tzs A dictionary of column names to tzinfo objects (or strings that will be converted to
          tzinfo objects).  The timezone will be applied to datetime objects returned in the query
        """

    @property
    def is_select(self) -> bool: ...
    @property
    def has_limit(self) -> bool: ...
    @property
    def is_insert(self) -> bool: ...
    @property
    def is_command(self) -> bool: ...
    def set_parameters(self, parameters: dict[str, Any]):  # -> None:
        ...
    def set_parameter(self, key: str, value: Any):  # -> None:
        ...
    def set_response_tz(self, response_tz: tzinfo):  # -> None:
        ...
    def start_column(self, name: str):  # -> None:
        ...
    def active_tz(self, datatype_tz: tzinfo | None):  # -> str | tzinfo | _UTCclass | StaticTzInfo | DstTzInfo | None:
        ...
    def updated_copy(
        self,
        query: str | bytes | None = ...,
        parameters: dict[str, Any] | None = ...,
        settings: dict[str, Any] | None = ...,
        query_formats: dict[str, str] | None = ...,
        column_formats: dict[str, str | dict[str, str]] | None = ...,
        encoding: str | None = ...,
        server_tz: tzinfo | None = ...,
        use_none: bool | None = ...,
        column_oriented: bool | None = ...,
        use_numpy: bool | None = ...,
        max_str_len: int | None = ...,
        query_tz: str | tzinfo | None = ...,
        column_tzs: dict[str, str | tzinfo] | None = ...,
        use_extended_dtypes: bool | None = ...,
        as_pandas: bool = ...,
        streaming: bool = ...,
        external_data: ExternalData | None = ...,
    ) -> QueryContext:
        """
        Creates Query context copy with parameters overridden/updated as appropriate.
        """

class QueryResult(Closable):
    """
    Wrapper class for query return values and metadata
    """

    def __init__(
        self,
        result_set: Matrix = ...,
        block_gen: Generator[Matrix, None, None] = ...,
        column_names: tuple = ...,
        column_types: tuple = ...,
        column_oriented: bool = ...,
        source: Closable = ...,
        query_id: str = ...,
        summary: dict[str, Any] = ...,
    ) -> None: ...
    @property
    def result_set(self) -> Matrix: ...
    @property
    def result_columns(self) -> Matrix: ...
    @property
    def result_rows(self) -> Matrix: ...
    @property
    def query_id(self) -> str: ...
    @property
    def column_block_stream(self) -> StreamContext: ...
    @property
    def row_block_stream(self):  # -> StreamContext:
        ...
    @property
    def rows_stream(self) -> StreamContext: ...
    def named_results(self) -> Generator[dict, None, None]: ...
    @property
    def row_count(self) -> int: ...
    @property
    def first_item(self):  # -> dict[Any, Any]:
        ...
    @property
    def first_row(self):  # -> list[Any] | Sequence[Any]:
        ...
    def close(self):  # -> None:
        ...

BS = ...
must_escape = ...

def quote_identifier(identifier: str):  # -> str:
    ...
def finalize_query(query: str, parameters: Sequence | dict[str, Any] | None, server_tz: tzinfo | None = ...) -> str: ...
def bind_query(
    query: str, parameters: Sequence | dict[str, Any] | None, server_tz: tzinfo | None = ...
) -> tuple[str, dict[str, str]]: ...
def format_str(value: str):  # -> str:
    ...
def escape_str(value: str):  # -> str:
    ...
def format_query_value(value: Any, server_tz: tzinfo = ...):  # -> str | Any:
    """
    Format Python values in a ClickHouse query
    :param value: Python object
    :param server_tz: Server timezone for adjusting datetime values
    :return: Literal string for python value
    """

def str_query_value(value: Any, server_tz: tzinfo = ...):  # -> str:
    ...
def format_bind_value(value: Any, server_tz: tzinfo = ..., top_level: bool = ...):  # -> str | Any | LiteralString:
    """
    Format Python values in a ClickHouse query
    :param value: Python object
    :param server_tz: Server timezone for adjusting datetime values
    :param top_level: Flag for top level for nested structures
    :return: Literal string for python value
    """

comment_re = ...

def remove_sql_comments(sql: str) -> str:
    """
    Remove SQL comments.  This is useful to determine the type of SQL query, such as SELECT or INSERT, but we
    don't fully trust it to correctly ignore weird quoted strings, and other edge cases, so we always pass the
    original SQL to ClickHouse (which uses a full-fledged AST/ token parser)
    :param sql:  SQL query
    :return: SQL Query without SQL comments
    """

def to_arrow(content: bytes): ...
def to_arrow_batches(buffer: IOBase) -> StreamContext: ...
def arrow_buffer(table) -> tuple[Sequence[str], bytes]: ...
