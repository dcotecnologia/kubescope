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
from typing import Any, cast
from urllib.parse import quote

from kubescope import PROJECT_URL, __version__
from kubescope.utils.errors import first_line

logger = logging.getLogger(__name__)

API_URL = "https://api.github.com/repos/dcotecnologia/kubescope"
TIMEOUT = 10  # seconds
_VERSION = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
# a version, final or not: 1.3.0, v1.3.0-rc1, 1.3.0rc1, 1.3.0-rc.1, 1.3.0a2, 1.3.0-beta1
_RELEASE = re.compile(
    r"v?(\d+)\.(\d+)\.(\d+)(?:[-.]?(dev|alpha|a|beta|b|rc|c)[-.]?(\d*))?"
)
FINAL = 3  # the stage of a release that is not a pre-release
# how far along a version is: a dev build, an alpha, a beta, a candidate, the release
_STAGES = {"dev": -1, "a": 0, "alpha": 0, "b": 1, "beta": 1, "c": 2, "rc": 2}
_SPELLED = {-1: "dev", 0: "a", 1: "b", 2: "rc"}  # as the package writes them
_TAGGED = {-1: "dev", 0: "alpha", 1: "beta", 2: "rc"}  # as the tag writes them
Key = tuple[int, int, int, int, int]  # major, minor, patch, stage, number
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


def release_key(text: str) -> Key | None:
    """A version, final or not, as numbers that order it: 1.3.0rc1 comes after
    1.3.0b2 and before 1.3.0; None when it is not a version."""
    found = _RELEASE.fullmatch(text.strip())
    if found is None:
        return None
    major, minor, patch = (int(part) for part in found.groups()[:3])
    word, number = found.group(4), found.group(5)
    if word is None:
        return major, minor, patch, FINAL, 0
    return major, minor, patch, _STAGES[word], int(number or 0)


def is_pre_release(key: Key) -> bool:
    return key[3] != FINAL


def package_version(key: Key) -> str:
    """The version as the package spells it, such as 1.3.0rc2: what the names
    of the files of a release carry."""
    base = ".".join(str(part) for part in key[:3])
    return base if key[3] == FINAL else f"{base}{_SPELLED[key[3]]}{key[4]}"


def _tags_of(key: Key) -> list[str]:
    """The names a release of this version may have been tagged with."""
    base = ".".join(str(part) for part in key[:3])
    tag = base if key[3] == FINAL else f"{base}-{_TAGGED[key[3]]}{key[4]}"
    return [f"v{tag}", tag]


def _published_release(release: object) -> bool:
    """Whether GitHub describes a release that is out and has a version in its
    tag."""
    return (
        isinstance(release, dict)
        and not release.get("draft")
        and isinstance(release.get("tag_name"), str)
        and release_key(release["tag_name"]) is not None
    )


def _stable(release: object) -> bool:
    """Whether GitHub describes a release of a plain version: not a draft, not
    marked as a pre-release and not tagged as one (v1.3.0-rc1)."""
    return (
        _published_release(release)
        and not cast(dict[str, Any], release).get("prerelease")
        and parse_version(cast(dict[str, Any], release)["tag_name"]) is not None
    )


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
    points at this project; the version is the one of the package, which
    names the files.
    """
    key = release_key(tag)
    if key is None:
        return None
    return Release(
        package_version(key), f"{PROJECT_URL}/releases/tag/{quote(tag.strip())}"
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
    """The published release of a version such as "0.9.1" or "1.3.0rc1"; None
    when the project has none.

    Network errors are raised.
    """
    wanted = release_key(version)
    if wanted is None:
        return None
    for name in _tags_of(wanted):
        try:
            found = _published(_get(f"/releases/tags/{quote(name)}"))
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            continue
        if found is not None:
            return found
    return None


def latest_release(pre_releases: bool = False) -> Release | None:
    """The newest stable release; when the project has none, the highest
    version among its tags.

    With `pre_releases`, the newest release of any kind: an alpha, a
    beta or a release candidate counts, for whoever runs one.
    """
    if pre_releases:
        listed = _get("/releases?per_page=30")
        usable = (
            [item for item in listed if _published_release(item)]
            if isinstance(listed, list)
            else []
        )
        best = max(
            usable,
            key=lambda item: release_key(item["tag_name"]) or (0, 0, 0, 0, 0),
            default=None,
        )
        return _published(best) if best is not None else None
    latest = _get("/releases/latest")
    if isinstance(latest, dict) and isinstance(latest.get("tag_name"), str):
        if _stable(latest):
            return _published(latest)
        # the newest release is an alpha, a beta or a release candidate, which a
        # stable installation never updates to: look for the newest stable one
        listed = _get("/releases?per_page=30")
        stable = (
            [item for item in listed if _stable(item)]
            if isinstance(listed, list)
            else []
        )
        newest = max(
            stable,
            key=lambda item: parse_version(item["tag_name"]) or (0, 0, 0),
            default=None,
        )
        return _published(newest) if newest is not None else None
    tags = [
        tag["name"]
        for tag in _get("/tags")
        if isinstance(tag, dict) and isinstance(tag.get("name"), str)
    ]
    versions = [tag for tag in tags if parse_version(tag)]
    if not versions:
        return None
    return _release(max(versions, key=lambda tag: parse_version(tag) or (0, 0, 0)))


def latest_release_for(current: str = __version__) -> Release | None:
    """The newest release that the running version may update to: a pre-release
    is offered the newest of any kind, a stable one only a stable one."""
    installed = release_key(current)
    return latest_release(
        pre_releases=installed is not None and is_pre_release(installed)
    )


@dataclass(frozen=True, slots=True)
class UpdateCheck:
    status: str  # "current", "available" or "failed"
    release: Release | None = None  # the newer release, when there is one
    limited_until: float | None = None  # when GitHub lets this address ask again


def _limited_until(error: Exception) -> float | None:
    """When GitHub lets the address ask again, if it refused for asking too
    often (the time it gives, in seconds since the epoch)."""
    if not isinstance(error, urllib.error.HTTPError) or error.code not in (403, 429):
        return None
    headers = error.headers
    if headers is None or headers.get("X-RateLimit-Remaining", "0") != "0":
        return None
    try:
        return float(headers["X-RateLimit-Reset"])
    except (KeyError, TypeError, ValueError):
        return None


def check_for_update(current: str = __version__) -> UpdateCheck:
    """Whether a release newer than the running version exists.

    A stable installation is offered only stable releases. An alpha, a
    beta or a release candidate is offered the next pre-release as well
    as the stable release. A source tree that was never installed has no
    version to compare, so it counts as current.
    """
    installed = release_key(current)
    try:
        release = latest_release_for(current)
    except (OSError, ValueError) as error:  # offline, rate limited, bad answer
        logger.debug("Update check failed: %s", first_line(str(error)))
        return UpdateCheck("failed", limited_until=_limited_until(error))
    newest = release_key(release.version) if release else None
    if release is None or installed is None or newest is None or newest <= installed:
        logger.info("KubeScope is up to date")
        return UpdateCheck("current")
    logger.info("A newer KubeScope is available: %s", release.version)
    return UpdateCheck("available", release)
