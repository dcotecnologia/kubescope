"""Unpack the zip of an extension without trusting it.

No Qt. The archive comes from a file the person picked or from a
repository, so nothing in it is believed: a name that leaves the folder,
a link, a repeated name, or more data than the limits allow is refused
before it is written.
"""

import io
import stat
import zipfile
from pathlib import Path

MAX_ARCHIVE = 20 * 1024 * 1024  # bytes of the zip
MAX_FILES = 2000
MAX_UNPACKED = 50 * 1024 * 1024  # bytes once unpacked
_CHUNK = 64 * 1024


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
