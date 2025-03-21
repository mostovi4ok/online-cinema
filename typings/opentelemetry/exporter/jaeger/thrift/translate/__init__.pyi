"""
This type stub file was generated by pyright.
"""

import abc

OTLP_JAEGER_SPAN_KIND = ...
NAME_KEY = ...
VERSION_KEY = ...
_SCOPE_NAME_KEY = ...
_SCOPE_VERSION_KEY = ...

class Translator(abc.ABC):
    def __init__(self, max_tag_value_length: int | None = ...) -> None: ...

class Translate:
    def __init__(self, spans) -> None: ...

class ThriftTranslator(Translator): ...
