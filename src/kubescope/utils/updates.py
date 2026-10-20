"""Look for a newer KubeScope on GitHub.

This is the one network call the app makes on its own. It asks the
public GitHub API for the latest release (or, when there is none, for
the tags) and sends nothing but a User-Agent with the app version. It
never raises: when the check cannot be done, there is simply nothing to
report. Settings can turn it off.
"""

import json
import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, replace
from typing import Any
from urllib.parse import quote

from kubescope import PROJECT_URL, __version__
from kubescope.utils.errors import first_line

logger = logging.getLogger(__name__)

API_URL = "https://api.github.com/repos/dcotecnologia/kubescope"
TIMEOUT = 10  # seconds
_VERSION = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
_DIGEST = re.compile(r"sha256:([0-9a-f]{64})")
MAX_NOTES = 20000  # characters of release notes kept


@dataclass(frozen=True, slots=True)
class Asset:
    name: str  # "kubescope_0.3.0_amd64.deb"
    url: str  # where GitHub serves the file, built here from the project
    sha256: str  # the digest GitHub published for the file


@dataclass(frozen=True, slots=True)
class Release:
    version: str  # "0.3.0"
    url: str  # the page of the release on GitHub
    notes: str = ""  # the changelog of the release, in Markdown
    assets: tuple[Asset, ...] = ()  # the files that carry a published digest


def parse_version(text: str) -> tuple[int, int, int] | None:
    """A "v1.2.3" or "1.2.3" tag as numbers; anything else (a pre-release such
    as "v1.2.3-rc1", or a tag that is not a version) is None."""
    found = _VERSION.fullmatch(text.strip())
    if found is None:
        return None
    major, minor, patch = (int(part) for part in found.groups())
    return major, minor, patch


def _get(path: str) -> Any:
    request = urllib.request.Request(
        f"{API_URL}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"KubeScope/{__version__}",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.load(response)


def _release(tag: str) -> Release | None:
    """A release for a tag name.

    The link is built here, not taken from the answer, so it always
    points at this project.
    """
    version = parse_version(tag)
    if version is None:
        return None
    return Release(
        ".".join(map(str, version)), f"{PROJECT_URL}/releases/tag/{quote(tag.strip())}"
    )


def _assets(tag: str, items: object) -> tuple[Asset, ...]:
    """The files of a release that GitHub gave a sha256 for.

    The download link is built here, so it always points at this
    project.
    """
    found = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        name, digest = item.get("name"), _DIGEST.fullmatch(str(item.get("digest")))
        if isinstance(name, str) and name and "/" not in name and digest:
            url = f"{PROJECT_URL}/releases/download/{quote(tag.strip())}/{quote(name)}"
            found.append(Asset(name, url, digest.group(1)))
    return tuple(found)


def _published(data: object) -> Release | None:
    """The release GitHub described, with its notes and files; None when the
    answer is not a release of a plain version."""
    if not isinstance(data, dict) or not isinstance(data.get("tag_name"), str):
        return None
    release = _release(data["tag_name"])
    if release is None:
        return None
    body = data.get("body")
    notes = body.strip()[:MAX_NOTES] if isinstance(body, str) else ""
    return replace(
        release, notes=notes, assets=_assets(data["tag_name"], data.get("assets"))
    )


def release_of(version: str) -> Release | None:
    """The published release of a version such as "0.9.1"; None when the
    project has none.

    Network errors are raised.
    """
    wanted = parse_version(version)
    if wanted is None:
        return None
    tag = ".".join(map(str, wanted))
    for name in (f"v{tag}", tag):
        try:
            found = _published(_get(f"/releases/tags/{quote(name)}"))
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            continue
        if found is not None:
            return found
    return None


def latest_release() -> Release | None:
    """The newest published release; when the project has none, the highest
    version among its tags."""
    latest = _get("/releases/latest")
    if isinstance(latest, dict) and isinstance(latest.get("tag_name"), str):
        return _published(latest)
    tags = [
        tag["name"]
        for tag in _get("/tags")
        if isinstance(tag, dict) and isinstance(tag.get("name"), str)
    ]
    versions = [tag for tag in tags if parse_version(tag)]
    if not versions:
        return None
    return _release(max(versions, key=lambda tag: parse_version(tag) or (0, 0, 0)))


@dataclass(frozen=True, slots=True)
class UpdateCheck:
    status: str  # "current", "available" or "failed"
    release: Release | None = None  # the newer release, when there is one


def check_for_update(current: str = __version__) -> UpdateCheck:
    """Whether a release newer than the running version exists.

    A source tree that was never installed has no version to compare, so
    it counts as current.
    """
    installed = parse_version(current)
    try:
        release = latest_release()
    except (OSError, ValueError) as error:  # offline, rate limited, bad answer
        logger.debug("Update check failed: %s", first_line(str(error)))
        return UpdateCheck("failed")
    newest = parse_version(release.version) if release else None
    if release is None or installed is None or newest is None or newest <= installed:
        logger.info("KubeScope is up to date")
        return UpdateCheck("current")
    logger.info("A newer KubeScope is available: %s", release.version)
    return UpdateCheck("available", release)
