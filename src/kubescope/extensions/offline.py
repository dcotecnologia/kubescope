"""The extensions that come installed, taken from a copy that ships with the
app, so that a first run needs no network.

No Qt. The build of the app downloads the latest release of each
extension that is installed by default (`tools/bundle_extensions.py`)
and keeps its zip and the repository and tag it came from; this reads
them back. They are installed like any other zip, so the same checks
run, and the source they record lets the app look for newer versions
later.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from kubescope.extensions.archive import MAX_ARCHIVE
from kubescope.extensions.github import GithubError, Repo, parse_repo

logger = logging.getLogger(__name__)

DIRECTORY = Path(__file__).resolve().parent.parent / "assets" / "extensions"


@dataclass(frozen=True)
class Snapshot:
    data: bytes  # the zip of the extension
    repo: Repo  # where it came from, with the tag of that release


def snapshot(extension: str, directory: Path | None = None) -> Snapshot | None:
    """The copy of an extension that ships with the app, None when there is
    none (a run from the sources, or a build made without a network)."""
    folder = directory or DIRECTORY
    try:
        zipped = folder / f"{extension}.zip"
        if zipped.stat().st_size > MAX_ARCHIVE:
            return None
        recorded = json.loads((folder / f"{extension}.json").read_text("utf-8"))
        repo = parse_repo(f"{recorded['repo']}/tree/{recorded['tag']}")
        return Snapshot(zipped.read_bytes(), repo)
    except (OSError, ValueError, KeyError, TypeError, GithubError) as error:
        logger.debug("No copy of %s ships with the app: %s", extension, error)
        return None
