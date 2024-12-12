"""
This type stub file was generated by pyright.
"""

LABELS_ADDED = ...
LABELS_REMOVED = ...
NODES_CREATED = ...
NODES_DELETED = ...
RELATIONSHIPS_DELETED = ...
PROPERTIES_SET = ...
PROPERTIES_REMOVED = ...
RELATIONSHIPS_CREATED = ...
INDICES_CREATED = ...
INDICES_DELETED = ...
CACHED_EXECUTION = ...
INTERNAL_EXECUTION_TIME = ...
STATS = ...

class ResultSetColumnTypes:
    COLUMN_UNKNOWN = ...
    COLUMN_SCALAR = ...
    COLUMN_NODE = ...
    COLUMN_RELATION = ...

class ResultSetScalarTypes:
    VALUE_UNKNOWN = ...
    VALUE_NULL = ...
    VALUE_STRING = ...
    VALUE_INTEGER = ...
    VALUE_BOOLEAN = ...
    VALUE_DOUBLE = ...
    VALUE_ARRAY = ...
    VALUE_EDGE = ...
    VALUE_NODE = ...
    VALUE_PATH = ...
    VALUE_MAP = ...
    VALUE_POINT = ...

class QueryResult:
    def __init__(self, graph, response, profile=...) -> None:
        """
        A class that represents a result of the query operation.

        Args:
        graph:
            The graph on which the query was executed.
        response:
            The response from the server.
        profile:
            A boolean indicating if the query command was "GRAPH.PROFILE"

        """

    def parse_results(self, raw_result_set):  # -> None:
        """
        Parse the query execution result returned from the server.
        """

    def parse_statistics(self, raw_statistics):  # -> None:
        """
        Parse the statistics returned in the response.
        """

    def parse_header(self, raw_result_set):
        """
        Parse the header of the result.
        """

    def parse_records(
        self, raw_result_set
    ):  # -> list[list[bool | Node | float | int | str | Edge | OrderedDict[Any, Any] | Path | dict[Any, Any] | list[Any] | None]]:
        """
        Parses the result set and returns a list of records.
        """

    def parse_entity_properties(self, props):  # -> dict[Any, Any]:
        """
        Parse node / edge properties.
        """

    def parse_string(self, cell):  # -> str:
        """
        Parse the cell as a string.
        """

    def parse_node(self, cell):  # -> Node:
        """
        Parse the cell to a node.
        """

    def parse_edge(self, cell):  # -> Edge:
        """
        Parse the cell to an edge.
        """

    def parse_path(self, cell):  # -> Path:
        """
        Parse the cell to a path.
        """

    def parse_map(self, cell):  # -> OrderedDict[Any, Any]:
        """
        Parse the cell as a map.
        """

    def parse_point(self, cell):  # -> dict[Any, Any]:
        """
        Parse the cell to point.
        """

    def parse_null(self, cell):  # -> None:
        """
        Parse a null value.
        """

    def parse_integer(self, cell):  # -> int:
        """
        Parse the integer value from the cell.
        """

    def parse_boolean(self, value):  # -> bool | None:
        """
        Parse the cell value as a boolean.
        """

    def parse_double(self, cell):  # -> float:
        """
        Parse the cell as a double.
        """

    def parse_array(self, value):  # -> list[Any]:
        """
        Parse an array of values.
        """

    def parse_unknown(self, cell):  # -> None:
        """
        Parse a cell of unknown type.
        """

    def parse_scalar(
        self, cell
    ):  # -> bool | Node | float | int | str | Edge | OrderedDict[Any, Any] | Path | dict[Any, Any] | list[Any] | None:
        """
        Parse a scalar value from a cell in the result set.
        """

    def parse_profile(self, response):  # -> None:
        ...
    def is_empty(self):  # -> bool:
        ...
    @property
    def labels_added(self):  # -> Literal[0]:
        """Returns the number of labels added in the query"""

    @property
    def labels_removed(self):  # -> Literal[0]:
        """Returns the number of labels removed in the query"""

    @property
    def nodes_created(self):  # -> Literal[0]:
        """Returns the number of nodes created in the query"""

    @property
    def nodes_deleted(self):  # -> Literal[0]:
        """Returns the number of nodes deleted in the query"""

    @property
    def properties_set(self):  # -> Literal[0]:
        """Returns the number of properties set in the query"""

    @property
    def properties_removed(self):  # -> Literal[0]:
        """Returns the number of properties removed in the query"""

    @property
    def relationships_created(self):  # -> Literal[0]:
        """Returns the number of relationships created in the query"""

    @property
    def relationships_deleted(self):  # -> Literal[0]:
        """Returns the number of relationships deleted in the query"""

    @property
    def indices_created(self):  # -> Literal[0]:
        """Returns the number of indices created in the query"""

    @property
    def indices_deleted(self):  # -> Literal[0]:
        """Returns the number of indices deleted in the query"""

    @property
    def cached_execution(self):  # -> bool:
        """Returns whether or not the query execution plan was cached"""

    @property
    def run_time_ms(self):  # -> Literal[0]:
        """Returns the server execution time of the query"""

    @property
    def parse_scalar_types(
        self,
    ):  # -> dict[int, Callable[..., None] | Callable[..., str] | Callable[..., int] | Callable[..., bool | None] | Callable[..., float] | Callable[..., list[Any]] | Callable[..., Node] | Callable[..., Edge] | Callable[..., Path] | Callable[..., OrderedDict[Any, Any]] | Callable[..., dict[Any, Any]]]:
        ...
    @property
    def parse_record_types(
        self,
    ):  # -> dict[int, Callable[..., bool | Node | float | int | str | Edge | OrderedDict[Any, Any] | Path | dict[Any, Any] | list[Any] | None] | Callable[..., Node] | Callable[..., Edge] | Callable[..., None]]:
        ...

class AsyncQueryResult(QueryResult):
    """
    Async version for the QueryResult class - a class that
    represents a result of the query operation.
    """

    def __init__(self) -> None:
        """
        To init the class you must call self.initialize()
        """

    async def initialize(self, graph, response, profile=...):  # -> Self:
        """
        Initializes the class.

        Args:
        graph:
            The graph on which the query was executed.
        response:
            The response from the server.
        profile:
            A boolean indicating if the query command was "GRAPH.PROFILE"

        """

    async def parse_node(self, cell):  # -> Node:
        """
        Parses a node from the cell.
        """

    async def parse_scalar(
        self, cell
    ):  # -> bool | Node | float | int | str | Edge | OrderedDict[Any, Any] | Path | dict[Any, Any] | list[Any] | None:
        """
        Parses a scalar value from the server response.
        """

    async def parse_records(self, raw_result_set):  # -> list[Any]:
        """
        Parses the result set and returns a list of records.
        """

    async def parse_results(self, raw_result_set):  # -> None:
        """
        Parse the query execution result returned from the server.
        """

    async def parse_entity_properties(self, props):  # -> dict[Any, Any]:
        """
        Parse node / edge properties.
        """

    async def parse_edge(self, cell):  # -> Edge:
        """
        Parse the cell to an edge.
        """

    async def parse_path(self, cell):  # -> Path:
        """
        Parse the cell to a path.
        """

    async def parse_map(self, cell):  # -> OrderedDict[Any, Any]:
        """
        Parse the cell to a map.
        """

    async def parse_array(
        self, value
    ):  # -> list[Any | bool | Node | float | int | str | Edge | OrderedDict[Any, Any] | Path | dict[Any, Any] | list[Any] | None]:
        """
        Parse array value.
        """
