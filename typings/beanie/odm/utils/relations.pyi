"""
This type stub file was generated by pyright.
"""

from collections.abc import Mapping as MappingType
from typing import TYPE_CHECKING, Any

from beanie import Document

if TYPE_CHECKING: ...

def convert_ids(query: MappingType[str, Any], doc: Document, fetch_links: bool) -> dict[str, Any]: ...
