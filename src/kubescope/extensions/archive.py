"""Unpack the zip of an extension without trusting it.

No Qt. The archive comes from a file the person picked or from a
repository, so nothing in it is believed: a name that leaves the folder,
a link, a repeated name, or more data than the limits allow is refused
before it is written.
"""

import hashlib
import io
import os
import shutil
import stat
import zipfile
from pathlib import Path

MAX_ARCHIVE = 20 * 1024 * 1024  # bytes of the zip
MAX_FILES = 2000
MAX_UNPACKED = 50 * 1024 * 1024  # bytes once unpacked
_CHUNK = 64 * 1024
# what a repository carries that an extension does not need
IGNORED = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "__MACOSX",
    }
)


class ArchiveError(Exception):
    """The archive cannot be unpacked; the message says why."""


def _unsafe(name: str) -> bool:
    parts = name.split("/")
    return (
        not name
        or "\\" in name
        or name.startswith("/")
        or name[1:2] == ":"  # a drive, as in C:/
        or ".." in parts
    )


def extract(data: bytes, destination: Path) -> None:
    """Unpack the zip in `data` into the existing folder `destination`."""
    if len(data) > MAX_ARCHIVE:
        raise ArchiveError("The file is too big to be an extension")
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as error:
        raise ArchiveError("It is not a zip file") from error
    with archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES:
            raise ArchiveError("It has too many files")
        root = destination.resolve()
        seen: set[str] = set()
        written = 0
        for info in infos:
            name = info.filename
            if _unsafe(name):
                raise ArchiveError(f"It has a file with an unsafe name: {name!r}")
            if name in seen:
                raise ArchiveError(f"It has {name!r} twice")
            seen.add(name)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ArchiveError(f"It has a link: {name!r}")
            target = (root / name).resolve()
            if not target.is_relative_to(root):
                raise ArchiveError(f"It has a file that leaves the folder: {name!r}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("wb") as out:
                while chunk := source.read(_CHUNK):
                    written += len(chunk)
                    if written > MAX_UNPACKED:  # the sizes it declares can lie
                        raise ArchiveError("It is too big once unpacked")
                    out.write(chunk)


def copy_tree(source: Path, destination: Path) -> None:
    """Copy the folder `source` into the existing folder `destination`, under the
    same limits as an archive: no links, and not more files or bytes than an
    extension may have. What a repository carries besides the code (`.git`, a
    virtual environment, caches) is left out."""
    root = source.resolve()
    if not root.is_dir():
        raise ArchiveError("It is not a folder")
    count = written = 0
    for folder, names, files in os.walk(root, followlinks=False):
        names[:] = sorted(name for name in names if name not in IGNORED)
        here = Path(folder)
        for name in names:
            if (here / name).is_symlink():
                raise ArchiveError(f"It has a link: {name!r}")
        target = destination / here.relative_to(root)
        target.mkdir(parents=True, exist_ok=True)
        for name in sorted(files):
            path = here / name
            if path.is_symlink():
                raise ArchiveError(f"It has a link: {name!r}")
            count += 1
            written += path.stat().st_size
            if count > MAX_FILES:
                raise ArchiveError("It has too many files")
            if written > MAX_UNPACKED:
                raise ArchiveError("It is too big")
            shutil.copyfile(path, target / name)


# What a repository has for the people who work on it and an installed extension does
# not need: its tests, its pipeline, its documents of the project and its tooling.
# The manifest, the code, the translations, the README and the LICENSE stay.
DEVELOPMENT = frozenset(
    {
        "tests",
        "test",
        "tools",
        "docs",
        ".github",
        ".git",
        ".gitignore",
        ".gitattributes",
        ".pre-commit-config.yaml",
        ".markdownlint.json",
        ".python-version",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".coverage",
        "coverage.xml",
        "dist",
        "build",
        "Makefile",
        "uv.lock",
        "pyproject.toml",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "noxfile.py",
        "tox.ini",
    }
)


def prune(folder: Path) -> list[str]:
    """Delete from an installed extension what is only for developing it (see
    `DEVELOPMENT`), at the top of its folder; the names removed."""
    removed = []
    for path in sorted(folder.iterdir()):
        if path.name not in DEVELOPMENT:
            continue
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
        removed.append(path.name)
    return removed


def tree_digest(root: Path) -> str:
    """The sha256 of the files under `root`: their paths and their content."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()
