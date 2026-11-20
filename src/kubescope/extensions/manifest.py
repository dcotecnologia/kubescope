"""The manifest of an extension: `kubescope-extension.toml`.

No Qt. It is the only thing read from an extension before the person
agrees to install it, so it is checked strictly: a manifest that does
not fit is refused with a message that says which field is wrong.
"""

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from kubescope.sdk import API_VERSION, PERMISSIONS

MANIFEST_NAME = "kubescope-extension.toml"
MAX_MANIFEST_BYTES = 16 * 1024
# what every extension has, and what its manifest does not need to list
REQUIRED = (MANIFEST_NAME, "LICENSE", "README.md", "src")
# what is for production when it is there, so the manifest does not list it
OPTIONAL = ("languages",)
_PRODUCTION = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_. -]{0,99}")
_MAX_PRODUCTION = 20

_ID = re.compile(r"[a-z0-9][a-z0-9_-]*(\.[a-z0-9][a-z0-9_-]*)+")
_VERSION = re.compile(r"\d{1,6}\.\d{1,6}\.\d{1,6}")
_ENTRY = re.compile(r"([A-Za-z_]\w*)(\.[A-Za-z_]\w*)*:[A-Za-z_]\w*")
_MAX_TEXT = 300
_COMMAND = re.compile(r"[a-z][a-z0-9-]{0,29}")
_MAX_COMMANDS = 8


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
    # the commands it adds to `kubescope`, so that the app knows them without
    # running the extension
    commands: tuple[str, ...] = ()
    # what else, at the top of its folder, is for production and stays when it is
    # installed; REQUIRED is always there, and OPTIONAL when it exists
    production: tuple[str, ...] = ()

    @property
    def kept(self) -> frozenset[str]:
        """The names at the top of the folder that stay once installed."""
        return frozenset((*REQUIRED, *OPTIONAL, *self.production))


def _text(document: dict[str, object], key: str, required: bool = True) -> str:
    value = document.get(key, "" if not required else None)
    if not isinstance(value, str) or (required and not value.strip()):
        raise ManifestError(f"{key} must be a text")
    if len(value) > _MAX_TEXT:
        raise ManifestError(f"{key} is too long")
    return value.strip()


def _production(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > _MAX_PRODUCTION:
        raise ManifestError("production must be a list of at most 20 names")
    names: list[str] = []
    for one in value:
        name = one.rstrip("/") if isinstance(one, str) else ""
        if not _PRODUCTION.fullmatch(name) or name in {".", ".."}:
            raise ManifestError(
                "production must list names at the top of the extension, like assets"
            )
        if name not in (*REQUIRED, *OPTIONAL) and name not in names:
            names.append(name)
    return tuple(names)


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
    commands = document.get("commands", [])
    if (
        not isinstance(commands, list)
        or not all(isinstance(one, str) and _COMMAND.fullmatch(one) for one in commands)
        or len(commands) > _MAX_COMMANDS
        or len(set(commands)) != len(commands)
    ):
        raise ManifestError(
            "commands must be a list of at most 8 different names, like chat"
        )
    if commands and "cli" not in permissions:
        raise ManifestError("commands need the permission cli")
    production = _production(document.get("production", []))
    return Manifest(
        id=extension,
        name=_text(document, "name"),
        version=version,
        entry=entry,
        permissions=frozenset(permissions),
        description=_text(document, "description", required=False),
        author=_text(document, "author", required=False),
        commands=tuple(commands),
        production=production,
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


def missing_required(folder: Path) -> list[str]:
    """What every extension must have and `folder` does not."""
    return [name for name in REQUIRED if not (folder / name).exists()]
