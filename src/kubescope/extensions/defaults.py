"""The extensions that the app recommends.

An extension that the app recommends is not part of it: it is a project
of its own that is downloaded from GitHub. By default it is the latest
release of the repository (its highest final tag), which is also what an
update looks for. An entry may pin a tag and the sha256 of the files of
that tag instead, and then only those files are accepted. No Qt.
"""

from dataclasses import dataclass

from kubescope.extensions.github import Repo
from kubescope.extensions.store import Candidate, StoreError


@dataclass(frozen=True)
class DefaultExtension:
    id: str
    name: str  # shown before it is downloaded
    description: str
    repo: Repo  # without a ref: the latest release; with one, that tag
    sha256: str = ""  # of the files of that tag; empty: whatever the release has
    automatic: bool = True  # installed on the first run; else only a card
    author: str = ""

    @property
    def pinned(self) -> bool:
        """Whether it is fixed to a tag and to the hash of its files."""
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
        repo=Repo("dcotecnologia", "kubescope-ai-gabi"),
        author="DCO Tecnologia",
    ),
    DefaultExtension(
        id="kubescope.aws",
        name="AWS Resources",
        description=(
            "Look at your AWS account from KubeScope: the RDS databases of the "
            "account of the selected cluster, in any region, with their details "
            "and logs, and a port forward to a database through Systems Manager "
            "in the write mode."
        ),
        repo=Repo("dcotecnologia", "kubescope-aws"),
        automatic=False,
        author="DCO Tecnologia",
    ),
    DefaultExtension(
        id="kubescope.search",
        name="Global Search",
        description=(
            "Press / or Ctrl+K to find a screen, a list or a resource of any "
            "namespace by its name, and open it."
        ),
        repo=Repo("dcotecnologia", "kubescope-search"),
        author="DCO Tecnologia",
    ),
    DefaultExtension(
        id="kubescope.themes",
        name="Themes",
        description=(
            "Thirteen color themes, light and dark: Abyss, Dark Modern, High "
            "Contrast, Light Modern, macOS Dark and Light, Midnight, Monokai, "
            "Quiet Light, Sepia, Solarized Dark and Light, and Tomorrow Night Blue."
        ),
        repo=Repo("dcotecnologia", "kubescope-themes"),
        author="DCO Tecnologia",
    ),
    DefaultExtension(
        id="kubescope.notifications",
        name="Notifications",
        description=(
            "A bell in the top bar that keeps the Warning and Error events of every "
            "context, and the errors and new versions KubeScope itself reports, and "
            "lists them in a panel that slides in from the right. A new one also "
            "shows a notice of the operating system that opens the app when clicked."
        ),
        repo=Repo("dcotecnologia", "kubescope-notifications"),
        automatic=False,
        author="DCO Tecnologia",
    ),
)


def offered() -> tuple[DefaultExtension, ...]:
    """What the app recommends."""
    return DEFAULTS


def verify(candidate: Candidate, wanted: DefaultExtension) -> None:
    """Refuse what was downloaded unless it is the extension, and, when the
    entry pins its files, the files that were pinned."""
    if candidate.manifest.id != wanted.id:
        raise StoreError(f"That is not {wanted.name}: it is {candidate.manifest.id}")
    if wanted.sha256 and candidate.sha256 != wanted.sha256:
        raise StoreError(
            f"That is not the version of {wanted.name} that this KubeScope "
            "expects: its files are not the ones that were checked"
        )
