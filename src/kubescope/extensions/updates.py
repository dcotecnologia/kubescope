"""Find out which installed extensions have a newer version.

No Qt. An extension that the app recommends is updated to the version
the app pins, which needs no network. One that came from another
repository on GitHub is compared with the highest tag of that
repository; only a final tag (`v1.2.3`) counts, never a pre-release.
Whatever is found is only offered: it is downloaded and reviewed like
any install.
"""

import logging
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from kubescope.extensions.defaults import DefaultExtension
from kubescope.extensions.github import GithubError, Repo, repo_of
from kubescope.extensions.store import Installed

logger = logging.getLogger(__name__)

_VERSION = re.compile(r"v?(\d{1,6})\.(\d{1,6})\.(\d{1,6})")


def version_key(text: str) -> tuple[int, int, int] | None:
    """`(1, 2, 3)` for `v1.2.3` or `1.2.3`; None for anything else, such as a
    pre-release."""
    found = _VERSION.fullmatch(text.strip())
    return (int(found[1]), int(found[2]), int(found[3])) if found else None


def latest_tag(names: Sequence[str]) -> str | None:
    """The highest final tag of a list of tags, None when there is none."""
    finals = [name for name in names if version_key(name) is not None]
    return max(finals, key=lambda name: version_key(name) or (0, 0, 0), default=None)


def recommended_versions(
    defaults: Sequence[DefaultExtension],
    present: set[str],
    tags: Callable[[Repo], list[str]] | None,
) -> dict[str, str]:
    """The latest versions of recommended extensions that are not installed."""
    if tags is None:
        return {}
    found = {}
    for one in defaults:
        if one.id in present:
            continue
        if one.repo.ref:
            continue
        try:
            newest = latest_tag(tags(one.repo))
        except GithubError as error:
            logger.info(
                "Could not look for the recommended version of %s: %s",
                one.id,
                error,
            )
            continue
        if newest is not None:
            found[one.id] = newest.removeprefix("v")
    return found


@dataclass(frozen=True)
class Update:
    extension: str
    name: str
    current: str  # the version that is installed
    latest: str  # the tag that is offered, such as v1.2.0
    repo: Repo  # with `latest` as its ref
    pin: DefaultExtension | None = None  # what the app pinned, to check it against

    @property
    def version(self) -> str:
        return self.latest.removeprefix("v")


def find(
    installed: Sequence[Installed],
    defaults: Sequence[DefaultExtension],
    tags: Callable[[Repo], list[str]] | None,
) -> list[Update]:
    """The updates there are.

    `tags` lists the tags of a repository; None means the network is not
    to be used, and only the pinned ones are looked at.
    """
    found = []
    for one in installed:
        if one.bundled or one.dev:
            continue
        try:
            repo = repo_of(one.source)
        except GithubError:
            continue
        current = version_key(one.manifest.version)
        if repo is None or current is None:
            continue
        pinned = next(
            (
                wanted
                for wanted in defaults
                if wanted.id == one.manifest.id
                and (wanted.repo.owner, wanted.repo.name) == (repo.owner, repo.name)
            ),
            None,
        )
        if pinned is not None and pinned.pinned:
            wanted_key = version_key(pinned.repo.ref)
            if wanted_key is not None and wanted_key > current:
                found.append(
                    Update(
                        one.manifest.id,
                        one.manifest.name,
                        one.manifest.version,
                        pinned.repo.ref,
                        pinned.repo,
                        pinned,
                    )
                )
            continue  # what is pinned never goes past what was checked
        if tags is None:
            continue
        try:
            names = tags(Repo(repo.owner, repo.name))
        except GithubError as error:
            logger.info("Could not look for updates of %s: %s", one.manifest.id, error)
            continue
        newest = latest_tag(names)
        if newest is not None and (version_key(newest) or (0, 0, 0)) > current:
            found.append(
                Update(
                    one.manifest.id,
                    one.manifest.name,
                    one.manifest.version,
                    newest,
                    Repo(repo.owner, repo.name, newest),
                    pinned,  # a recommended one is still checked to be itself
                )
            )
    return found
