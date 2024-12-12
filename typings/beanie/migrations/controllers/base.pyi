"""
This type stub file was generated by pyright.
"""

from abc import ABC, abstractmethod

from beanie.odm.documents import Document

class BaseMigrationController(ABC):
    def __init__(self, function) -> None: ...
    @abstractmethod
    async def run(self, session):  # -> None:
        ...
    @property
    @abstractmethod
    def models(self) -> list[type[Document]]: ...
