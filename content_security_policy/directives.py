"""
Actual directives, I would have loved to generate these classes dynamically, but then autocompletion tools won't
properly pick up on them.
"""
from content_security_policy.base_classes import Directive, FetchDirective
from content_security_policy.values import SourceList, AncestorSourceList


# Fetch Directives
class ChildSrc(FetchDirective):
    name = "child-src"


class ConnectSrc(FetchDirective):
    name = "connect-src"


class DefaultSrc(FetchDirective):
    name = "default-src"


class FontSrc(FetchDirective):
    name = "font-src"


class FrameSrc(FetchDirective):
    name = "frame-src"


class ImgSrc(FetchDirective):
    name = "img-src"


class ManifestSrc(FetchDirective):
    name = "manifest-src"


class MediaSrc(FetchDirective):
    name = "media-src"


class ObjectSrc(FetchDirective):
    name = "object-src"


class ScriptSrc(FetchDirective):
    name = "script-src"


class ScriptSrcElem(FetchDirective):
    name = "script-src-elem"


class ScriptSrcAttr(FetchDirective):
    name = "script-src-attr"


class StyleSrc(FetchDirective):
    name = "style-src"


class StyleSrcElem(FetchDirective):
    name = "style-src-elem"


class StyleSrcAttr(FetchDirective):
    name = "style-src-attr"


# Other directives
# TODO: Allows only one value!
class Webrtc(Directive[SourceList]):
    name = "webrtc"


class WorkerSrc(Directive[SourceList]):
    name = "worker-src"


# Document directives
class BaseUri(Directive[SourceList]):
    name = "base-uri"


# TODO: Special value for sandbox tokens
class Sandbox(Directive):
    name = "sandbox"


# Navigation directives
class FormAction(Directive[SourceList]):
    name = "form-action"


class FrameAncestors(Directive[AncestorSourceList]):
    name = "frame-ancestors"


# Reporting directives


# TODO uri-reference value
class ReportUri(Directive):
    name = "report-uri"


# TODO "token" value
class ReportTo(Directive):
    name = "report-to"
