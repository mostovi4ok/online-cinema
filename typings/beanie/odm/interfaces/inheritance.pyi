"""
This type stub file was generated by pyright.
"""

from typing import ClassVar

class InheritanceInterface:
    _children: ClassVar[dict[str, type]]
    _parent: ClassVar[type | None]
    _inheritance_inited: ClassVar[bool]
    _class_id: ClassVar[str | None] = ...
    @classmethod
    def add_child(cls, name: str, clas: type):  # -> None:
        ...
