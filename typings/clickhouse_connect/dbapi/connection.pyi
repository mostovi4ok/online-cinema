"""
This type stub file was generated by pyright.
"""

from clickhouse_connect.driver.query import QueryResult

class Connection:
    """
    See :ref:`https://peps.python.org/pep-0249/`
    """

    def __init__(
        self,
        dsn: str = ...,
        username: str = ...,
        password: str = ...,
        host: str = ...,
        database: str = ...,
        interface: str = ...,
        port: int = ...,
        secure: bool | str = ...,
        **kwargs,
    ) -> None: ...
    def close(self):  # -> None:
        ...
    def commit(self):  # -> None:
        ...
    def rollback(self):  # -> None:
        ...
    def command(self, cmd: str):  # -> str | int | Sequence[str] | QuerySummary:
        ...
    def raw_query(self, query: str) -> QueryResult: ...
    def cursor(self):  # -> Cursor:
        ...
