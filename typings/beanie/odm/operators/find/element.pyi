"""
This type stub file was generated by pyright.
"""

from abc import ABC

from beanie.odm.operators.find import BaseFindOperator

class BaseFindElementOperator(BaseFindOperator, ABC): ...

class Exists(BaseFindElementOperator):
    """
    `$exists` query operator

    Example:
    ```python
    class Product(Document):
        price: float

    Exists(Product.price, True)
    ```

    Will return query object like

    ```python
    {"price": {"$exists": True}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/exists/>

    """

    def __init__(self, field, value: bool = ...) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, bool]]:
        ...

class Type(BaseFindElementOperator):
    """
    `$type` query operator

    Example:
    ```python
    class Product(Document):
        price: float

    Type(Product.price, "decimal")
    ```

    Will return query object like

    ```python
    {"price": {"$type": "decimal"}}
    ```

    MongoDB doc:
    <https://docs.mongodb.com/manual/reference/operator/query/type/>

    """

    def __init__(self, field, types: list[str] | str) -> None: ...
    @property
    def query(self):  # -> dict[Any, dict[str, List[str] | str]]:
        ...
