"""The extensions that the app offers to install, and exactly which version.

An extension that the app offers is not part of it: it is a project of
its own that is downloaded from GitHub when the person agrees. What is
downloaded is pinned: a tag, and the sha256 of the files of that tag, so
that what is installed is what was checked and not whatever the tag
points at later. An entry that is not pinned yet is not offered. No Qt.
"""

from dataclasses import dataclass

from kubescope.extensions.github import Repo
from kubescope.extensions.store import Candidate, StoreError


@dataclass(frozen=True)
class DefaultExtension:
    id: str
    name: str  # shown before it is downloaded
    description: str
    repo: Repo  # with the tag of the version
    sha256: str  # of the files of that tag; see `tools/pin_default_extension.py`

    @property
    def pinned(self) -> bool:
        return bool(self.repo.ref) and len(self.sha256) == 64


DEFAULTS = (
    DefaultExtension(
        id="kubescope.gabi",
        name="Gabi - AI Assistant",
        description=(
            "The assistant of DCO Tecnologia: ask about your cluster from a coding "
            "assistant installed on this computer."
        ),
        repo=Repo("dcotecnologia", "kubescope-ai-gabi", "v1.0.0"),
        sha256="48008c8ce9ac8c1279208e699892faf9d70e8833bdccf55d595d11df30b62e6d",
    ),
)


def offered() -> tuple[DefaultExtension, ...]:
    """What the app can offer now: the pinned ones."""
    return tuple(one for one in DEFAULTS if one.pinned)


def verify(candidate: Candidate, wanted: DefaultExtension) -> None:
    """Refuse what was downloaded unless it is the extension and the files that
    were pinned."""
    if candidate.manifest.id != wanted.id:
        raise StoreError(f"That is not {wanted.name}: it is {candidate.manifest.id}")
    if candidate.sha256 != wanted.sha256:
        raise StoreError(
            f"That is not the version of {wanted.name} that this KubeScope "
            "expects: its files are not the ones that were checked"
        )
