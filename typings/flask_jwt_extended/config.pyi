"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterable, Sequence
from json import JSONEncoder

from flask_jwt_extended.typing import ExpiresDelta

class _Config:
    """
    Helper object for accessing and verifying options in this extension. This
    is meant for internal use of the application; modifying config options
    should be done with flasks ```app.config```.

    Default values for the configuration options are set in the jwt_manager
    object. All of these values are read only. This is simply a loose wrapper
    with some helper functionality for flasks `app.config`.
    """

    @property
    def is_asymmetric(self) -> bool: ...
    @property
    def encode_key(self) -> str: ...
    @property
    def decode_key(self) -> str: ...
    @property
    def token_location(self) -> Sequence[str]: ...
    @property
    def jwt_in_cookies(self) -> bool: ...
    @property
    def jwt_in_headers(self) -> bool: ...
    @property
    def jwt_in_query_string(self) -> bool: ...
    @property
    def jwt_in_json(self) -> bool: ...
    @property
    def header_name(self) -> str: ...
    @property
    def header_type(self) -> str: ...
    @property
    def query_string_name(self) -> str: ...
    @property
    def query_string_value_prefix(self) -> str: ...
    @property
    def access_cookie_name(self) -> str: ...
    @property
    def refresh_cookie_name(self) -> str: ...
    @property
    def access_cookie_path(self) -> str: ...
    @property
    def refresh_cookie_path(self) -> str: ...
    @property
    def cookie_secure(self) -> bool: ...
    @property
    def cookie_domain(self) -> str: ...
    @property
    def session_cookie(self) -> bool: ...
    @property
    def cookie_samesite(self) -> str: ...
    @property
    def json_key(self) -> str: ...
    @property
    def refresh_json_key(self) -> str: ...
    @property
    def cookie_csrf_protect(self) -> bool: ...
    @property
    def csrf_request_methods(self) -> Iterable[str]: ...
    @property
    def csrf_in_cookies(self) -> bool: ...
    @property
    def access_csrf_cookie_name(self) -> str: ...
    @property
    def refresh_csrf_cookie_name(self) -> str: ...
    @property
    def access_csrf_cookie_path(self) -> str: ...
    @property
    def refresh_csrf_cookie_path(self) -> str: ...
    @property
    def access_csrf_header_name(self) -> str: ...
    @property
    def refresh_csrf_header_name(self) -> str: ...
    @property
    def csrf_check_form(self) -> bool: ...
    @property
    def access_csrf_field_name(self) -> str: ...
    @property
    def refresh_csrf_field_name(self) -> str: ...
    @property
    def access_expires(self) -> ExpiresDelta: ...
    @property
    def refresh_expires(self) -> ExpiresDelta: ...
    @property
    def algorithm(self) -> str: ...
    @property
    def decode_algorithms(self) -> list[str]: ...
    @property
    def cookie_max_age(self) -> int | None: ...
    @property
    def identity_claim_key(self) -> str: ...
    @property
    def exempt_methods(self) -> Iterable[str]: ...
    @property
    def error_msg_key(self) -> str: ...
    @property
    def json_encoder(self) -> type[JSONEncoder]: ...
    @property
    def decode_audience(self) -> str | Iterable[str]: ...
    @property
    def encode_audience(self) -> str | Iterable[str]: ...
    @property
    def encode_issuer(self) -> str: ...
    @property
    def decode_issuer(self) -> str: ...
    @property
    def leeway(self) -> int: ...
    @property
    def encode_nbf(self) -> bool: ...

config = ...
