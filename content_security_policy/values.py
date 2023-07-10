__all__ = [
    "NonceSrc",
    "HashAlgorithm",
    "HashSrc",
    "SchemeSrc",
    "HostSrc",
    "KeywordSource",
    "SourceExpression",
    "SourceList",
    "WebrtcValue",
    "AncestorSource",
    "AncestorSourceList",
    "SandboxValue",
    "ReportToValue",
    "UriReference",
    "ReportUriValue",
]

from enum import StrEnum
from typing import Optional, Tuple, Union, cast, Literal

from content_security_policy.constants import (
    NONCE_PREFIX,
    KEYWORD_SOURCES,
    WEBRTC_VALUES,
    NONE,
    SELF,
    SANDBOX_VALUES,
)
from content_security_policy.exceptions import BadDirectiveValue, BadSourceExpression
from content_security_policy.patterns import (
    TOKEN,
    BASE64_VALUE,
    SCHEME,
    HOST_SOURCE,
    URI_REFERENCE,
    KEYWORD_SOURCE as KEYWORD_SOURCE_RE,
    WEBRTC_VALUE as WEBRTC_VALUE_RE,
    SANDBOX_VALUE as SANDBOX_VALUE_RE,
)
from content_security_policy.utils import SingleValueClass, AutoInstanceMixin


class SourceExpression:
    ...


# https://w3c.github.io/webappsec-csp/#grammardef-nonce-source
class NonceSrc(SourceExpression):
    def __init__(self, nonce: str):
        nonce = nonce.strip("'").lstrip(NONCE_PREFIX)
        if not BASE64_VALUE.fullmatch(nonce):
            raise BadSourceExpression(
                f"Nonce value '{nonce}' does not match {BASE64_VALUE.pattern}"
            )

        self._nonce_value: str = nonce

    def __str__(self):
        return f"'{NONCE_PREFIX}{self._nonce_value}'"


# https://w3c.github.io/webappsec-csp/#grammardef-hash-algorithm
class HashAlgorithm(StrEnum):
    sha256 = "sha256"
    sha384 = "sha384"
    sha512 = "sha512"


# https://w3c.github.io/webappsec-csp/#grammardef-nonce-source
class HashSrc(SourceExpression):
    def __init__(self, value: str, algo: Optional[HashAlgorithm | str] = None):
        value = value.strip("'")

        if algo is not None:
            hash_value = value
        else:
            algo, hash_value = value.split("-")

        if not algo in HashAlgorithm:
            raise BadSourceExpression(f"Unknown hash algorithm: '{algo}'")

        if not BASE64_VALUE.fullmatch(hash_value):
            raise BadSourceExpression(
                f"Hash value '{hash_value}' does not match {BASE64_VALUE.pattern}"
            )

        self._algo: HashAlgorithm = algo
        self._hash_value: str = hash_value

    def __str__(self):
        return f"'{self._algo}-{self._hash_value}'"


# https://w3c.github.io/webappsec-csp/#grammardef-scheme-source
class SchemeSrc(SourceExpression):
    def __init__(self, scheme: str):
        scheme = scheme.rstrip(":")
        if not SCHEME.fullmatch(scheme):
            raise BadSourceExpression(
                f"Scheme '{scheme}' does not match {SCHEME.pattern}"
            )

        self._scheme: str = scheme

    def __str__(self):
        return f"{self._scheme}:"


# https://w3c.github.io/webappsec-csp/#grammardef-host-source
class HostSrc(SourceExpression):
    def __init__(self, host: str):
        if not HOST_SOURCE.fullmatch(host):
            raise BadSourceExpression(f"{host} does not match {HOST_SOURCE.pattern}")
        self._host = host

    def __str__(self):
        return self._host


# https://w3c.github.io/webappsec-csp/#grammardef-keyword-source
class KeywordSource(AutoInstanceMixin, SourceExpression):
    # You can later get an instance of any value source by accessing these as class attributes
    # They are spelled out explicitly here so type hints work
    self = cast("KeywordSource", "'self'")
    unsafe_inline = cast("KeywordSource", "'unsafe-inline'")
    unsafe_eval = cast("KeywordSource", "'unsafe-eval'")
    strict_dynamic = cast("KeywordSource", "'strict-dynamic'")
    unsafe_hashes = cast("KeywordSource", "'unsafe-hashes'")
    report_sample = cast("KeywordSource", "'report-sample'")
    unsafe_allow_redirects = cast("KeywordSource", "'unsafe-allow-redirects'")
    wasm_unsafe_eval = cast("KeywordSource", "'wasm-unsafe-eval'")
    _auto_instance_prop = KEYWORD_SOURCES

    def __init__(self, keyword: str):
        keyword = str(keyword)
        no_ticks_keyword = keyword.strip("'")
        keyword = f"'{no_ticks_keyword}'"
        if not KEYWORD_SOURCE_RE.fullmatch(keyword):
            raise BadSourceExpression(
                f"{keyword} does not match {KEYWORD_SOURCE_RE.pattern}"
            )

        self._keyword = no_ticks_keyword

    def __str__(self):
        return f"'{self._keyword}'"


# According to spec, 'none'  is not a `source-expression`, but a special case of `serialized-source-list`
# https://w3c.github.io/webappsec-csp/#grammardef-serialized-source-list
class NoneSource(SingleValueClass):
    _value = NONE


# https://w3c.github.io/webappsec-csp/#grammardef-serialized-source-list
SourceList = Union[Tuple[SourceExpression] | NoneSource]


class WebrtcValue(AutoInstanceMixin):
    # You can later get an instance of any value by accessing these as class attributes
    # They are spelled out explicitly here so type hints work
    allow = cast("WebrtcValue", "'allow'")
    block = cast("WebrtcValue", "'block'")
    _auto_instance_prop = WEBRTC_VALUES

    def __init__(self, value: str):
        value = str(value)
        no_ticks_keyword = value.strip("'")
        value = f"'{no_ticks_keyword}'"
        if not WEBRTC_VALUE_RE.fullmatch(value):
            raise BadSourceExpression(
                f"{value} does not match {KEYWORD_SOURCE_RE.pattern}"
            )
        self._keyword = no_ticks_keyword

    def __str__(self):
        return f"'{self._keyword}'"


# 'self' is a keyword source expression, but it is also a possible value for frame-ancestors
# Other KeywordSources are not valid values for frame-ancestors.
class Self(SingleValueClass):
    _value = SELF


# https://w3c.github.io/webappsec-csp/#grammardef-ancestor-source-list
AncestorSource = Union[SchemeSrc, HostSrc, Self]
AncestorSourceList = Union[Tuple[AncestorSource] | NoneSource]


# https://html.spec.whatwg.org/multipage/iframe-embed-object.html#the-iframe-elemet
class SandboxToken(AutoInstanceMixin):
    # You can later get an instance of any value by accessing these as class attributes
    # They are spelled out explicitly here so type hints work
    allow_downloads = cast("SandboxToken", "allow-downloads")
    allow_forms = cast("SandboxToken", "allow-forms")
    allow_modals = cast("SandboxToken", "allow-modals")
    allow_orientation_lock = cast("SandboxToken", "allow-orientation-lock")
    allow_pointer_lock = cast("SandboxToken", "allow-pointer-lock")
    allow_popups = cast("SandboxToken", "allow-popups")
    allow_popups_to_escape_sandbox = cast(
        "SandboxToken", "allow-popups-to-escape-sandbox"
    )
    allow_presentation = cast("SandboxToken", "allow-presentation")
    allow_same_origin = cast("SandboxToken", "allow-same-origin")
    allow_scripts = cast("SandboxToken", "allow-scripts")
    allow_top_navigation = cast("SandboxToken", "allow-top-navigation")
    allow_top_navigation_by_user_activation = cast(
        "SandboxToken", "allow-top-navigation-by-user-activation"
    )
    allow_top_navigation_to_custom_protocols = cast(
        "SandboxToken", "allow-top-navigation-to-custom-protocols"
    )
    _auto_instance_prop = SANDBOX_VALUES

    def __init__(self, value: str):
        value = str(value)
        if not SANDBOX_VALUE_RE.fullmatch(value):
            raise BadDirectiveValue(
                f"{value} does not match {SANDBOX_VALUE_RE.pattern}"
            )
        self._token = value.lower()

    def __str__(self):
        # Unlike other "keywords" in CSP, sandbox values are not wrapped in single ticks
        return self._token


SandboxValue = Union[Tuple[SandboxToken], Literal[""]]


# https://w3c.github.io/webappsec-csp/#directive-report-to
class ReportToValue:
    def __init__(self, value: str):
        value = str(value)
        if not TOKEN.fullmatch(value):
            raise BadDirectiveValue(f"{value} does not match {TOKEN.pattern}")
        self._token = value.lower()

    def __str__(self):
        return self._token


# https://w3c.github.io/webappsec-csp/#directive-report-uri
class UriReference:
    def __init__(self, value: str):
        value = str(value)
        if not URI_REFERENCE.fullmatch(value):
            raise BadDirectiveValue(f"{value} does not match {URI_REFERENCE.pattern}")
        self._uri_reference = value.lower()

    def __str__(self):
        return self._uri_reference


ReportUriValue = Tuple[UriReference]