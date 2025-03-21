"""
This type stub file was generated by pyright.
"""

from abc import ABC

from beanie.odm.operators.find import BaseFindOperator

class BaseFindArrayOperator(BaseFindOperator, ABC): ...

class All(BaseFindArrayOperator):
    """
    `$all` array query operator

    Example:
    ```python
    class Sample(Document):
        results: List[int]

    All(Sample.results, [80, 85])
    ```

    Will return query object like

    ```python
    {"results": {"$all": [80, 85]}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/all>

    """

    def __init__(self, field, values: list) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, list[Any]]]:
        ...

class ElemMatch(BaseFindArrayOperator):
    """
    `$elemMatch` array query operator

    Example:
    ```python
    class Sample(Document):
        results: List[int]

    ElemMatch(Sample.results, {"$in": [80, 85]})
    ```

    Will return query object like

    ```python
    {"results": {"$elemMatch": {"$in": [80, 85]}}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/elemMatch/>

    """

    def __init__(self, field, expression: dict | None = ..., **kwargs) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, dict[str, Any] | dict[Any, Any]]]:
        ...

class Size(BaseFindArrayOperator):
    """
    `$size` array query operator

    Example:
    ```python
    class Sample(Document):
        results: List[int]

    Size(Sample.results, 2)
    ```

    Will return query object like

    ```python
    {"results": {"$size": 2}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/size/>

    """

    def __init__(self, field, num: int) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, int]]:
        ...
