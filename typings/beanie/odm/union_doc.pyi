"""
This type stub file was generated by pyright.
"""

from typing import ClassVar, TypeVar

from beanie.odm.interfaces.aggregate import AggregateInterface
from beanie.odm.interfaces.detector import DetectionInterface, ModelType
from beanie.odm.interfaces.find import FindInterface
from beanie.odm.interfaces.getters import OtherGettersInterface
from beanie.odm.settings.union_doc import UnionDocSettings

UnionDocType = TypeVar("UnionDocType", bound=UnionDoc)

class UnionDoc(FindInterface, AggregateInterface, OtherGettersInterface, DetectionInterface):
    _document_models: ClassVar[dict[str, type] | None] = ...
    _is_inited: ClassVar[bool] = ...
    _settings: ClassVar[UnionDocSettings]
    @classmethod
    def get_settings(cls) -> UnionDocSettings: ...
    @classmethod
    def register_doc(cls, name: str, doc_model: type):  # -> str | None:
        ...
    @classmethod
    def get_model_type(cls) -> ModelType: ...
