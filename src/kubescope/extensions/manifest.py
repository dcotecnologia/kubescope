"""The manifest of an extension: `kubescope-extension.toml`.

No Qt. It is the only thing read from an extension before the person
agrees to install it, so it is checked strictly: a manifest that does
not fit is refused with a message that says which field is wrong.
"""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from kubescope_sdk import API_VERSION, PERMISSIONS

MANIFEST_NAME = "kubescope-extension.toml"
MAX_MANIFEST_BYTES = 16 * 1024

_ID = re.compile(r"[a-z0-9][a-z0-9_-]*(\.[a-z0-9][a-z0-9_-]*)+")
_VERSION = re.compile(r"\d{1,6}\.\d{1,6}\.\d{1,6}")
_ENTRY = re.compile(r"([A-Za-z_]\w*)(\.[A-Za-z_]\w*)*:[A-Za-z_]\w*")
_MAX_TEXT = 300


class ManifestError(Exception):
    """The manifest cannot be used; the message says why."""


@dataclass(frozen=True)
class Manifest:
    id: str
    name: str
    version: str
    entry: str  # "package.module:function", looked up in the extension folder
    permissions: frozenset[str]
    description: str = ""
    author: str = ""


def _text(document: dict[str, object], key: str, required: bool = True) -> str:
    value = document.get(key, "" if not required else None)
    if not isinstance(value, str) or (required and not value.strip()):
        raise ManifestError(f"{key} must be a text")
    if len(value) > _MAX_TEXT:
        raise ManifestError(f"{key} is too long")
    return value.strip()


def parse_manifest(content: bytes) -> Manifest:
    """The manifest in `content`, or a `ManifestError`."""
    if len(content) > MAX_MANIFEST_BYTES:
        raise ManifestError("the manifest is too big")
    try:
        document = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise ManifestError(f"it is not a valid TOML file: {error}") from error
    extension = _text(document, "id")
    if not _ID.fullmatch(extension):
        raise ManifestError("id must look like author.name, in lowercase")
    version = _text(document, "version")
    if not _VERSION.fullmatch(version):
        raise ManifestError("version must look like 1.2.3")
    api = _text(document, "api")
    if api != API_VERSION:
        raise ManifestError(
            f"it needs the API {api} and this app offers the API {API_VERSION}"
        )
    entry = _text(document, "entry")
    if not _ENTRY.fullmatch(entry):
        raise ManifestError("entry must look like package.module:function")
    permissions = document.get("permissions", [])
    if not isinstance(permissions, list) or not all(
        isinstance(one, str) for one in permissions
    ):
        raise ManifestError("permissions must be a list of texts")
    unknown = sorted(set(permissions) - set(PERMISSIONS))
    if unknown:
        raise ManifestError(f"unknown permissions: {', '.join(unknown)}")
    return Manifest(
        id=extension,
        name=_text(document, "name"),
        version=version,
        entry=entry,
        permissions=frozenset(permissions),
        description=_text(document, "description", required=False),
        author=_text(document, "author", required=False),
    )


def read_manifest(folder: Path) -> Manifest:
    """The manifest of the extension in `folder`."""
    path = folder / MANIFEST_NAME
    try:
        if path.stat().st_size > MAX_MANIFEST_BYTES:
            raise ManifestError("the manifest is too big")
        return parse_manifest(path.read_bytes())
    except OSError as error:
        raise ManifestError(f"{MANIFEST_NAME} could not be read") from error
