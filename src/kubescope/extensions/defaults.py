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
    automatic: bool = True  # installed on the first run; else only a card

    @property
    def pinned(self) -> bool:
        return bool(self.repo.ref) and len(self.sha256) == 64


DEFAULTS = (
    DefaultExtension(
        id="kubescope.gabi",
        name="Gabi - AI Assistant",
        description=(
            "Ask about your cluster in plain language: she reads workloads, events, "
            "logs and live CPU and memory, explains what is wrong and how to fix it, "
            "and takes you to the right list or tab. "
            "Changes (scale, edit) only in write mode, each one confirmed. "
            "Uses the coding assistant you already signed in to."
        ),
        repo=Repo("dcotecnologia", "kubescope-ai-gabi", "v1.0.1"),
        sha256="08910eda1092a1aa950b8ab49e3ddf8c7455680986e2a336c364b6b023b03ea5",
    ),
    DefaultExtension(
        id="kubescope.aws",
        name="AWS",
        description=(
            "Look at your AWS account from KubeScope: the RDS databases of the "
            "account of the selected cluster, in any region, with their details "
            "and logs, and a port forward to a database through Systems Manager "
            "in the write mode."
        ),
        repo=Repo("dcotecnologia", "kubescope-aws", "v1.0.1"),
        sha256="9762bac6076e467b5868ca4966726b7a2b3613ce28a1d65181788e41d3688e0a",
        automatic=False,
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
