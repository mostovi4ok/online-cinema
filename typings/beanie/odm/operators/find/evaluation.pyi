"""
This type stub file was generated by pyright.
"""

from abc import ABC

from beanie.odm.operators.find import BaseFindOperator

class BaseFindEvaluationOperator(BaseFindOperator, ABC): ...

class Expr(BaseFindEvaluationOperator):
    """
    `$type` query operator

    Example:
    ```python
    class Sample(Document):
        one: int
        two: int

    Expr({"$gt": ["$one", "$two"]})
    ```

    Will return query object like

    ```python
    {"$expr": {"$gt": ["$one", "$two"]}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/expr/>

    """

    def __init__(self, expression: dict) -> None: ...
    @property
    def query(self):  # -> dict[str, dict[Any, Any]]:
        ...

class JsonSchema(BaseFindEvaluationOperator):
    """
    `$jsonSchema` query operator

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/jsonSchema/>
    """

    def __init__(self, expression: dict) -> None: ...
    @property
    def query(self):  # -> dict[str, dict[Any, Any]]:
        ...

class Mod(BaseFindEvaluationOperator):
    """
    `$mod` query operator

    Example:
    ```python
    class Sample(Document):
        one: int

    Mod(Sample.one, 4, 0)
    ```

    Will return query object like

    ```python
    {"one": {"$mod": [4, 0]}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/mod/>

    """

    def __init__(self, field, divisor: int, remainder: int) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, list[int]]]:
        ...

class RegEx(BaseFindEvaluationOperator):
    """
    `$regex` query operator

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/regex/>
    """

    def __init__(self, field, pattern: str, options: str | None = ...) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, str]]:
        ...

class Text(BaseFindEvaluationOperator):
    """
    `$text` query operator

    Example:
    ```python
    class Sample(Document):
        description: Indexed(str, pymongo.TEXT)

    Text("coffee")
    ```

    Will return query object like

    ```python
    {"$text": {"$search": "coffee", "$caseSensitive": False, "$diacriticSensitive": False}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/text/>

    """

    def __init__(
        self, search: str, language: str | None = ..., case_sensitive: bool = ..., diacritic_sensitive: bool = ...
    ) -> None:
        """

        :param search: str
        :param language: Optional[str] = None
        :param case_sensitive: bool = False
        :param diacritic_sensitive: bool = False
        """

    @property
    def query(self):  # -> dict[str, dict[str, str | bool]]:
        ...

class Where(BaseFindEvaluationOperator):
    """
    `$where` query operator

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/where/>
    """

    def __init__(self, expression: str) -> None: ...
    @property
    def query(self):  # -> dict[str, str]:
        ...
