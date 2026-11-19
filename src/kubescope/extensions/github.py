"""Download the zip of an extension from a repository on GitHub.

No Qt. This runs only when the person asks to install from a repository.
It reaches `api.github.com` (which sends the zip from
`codeload.github.com`) over HTTPS and sends nothing but a User-Agent
with the app version.
"""

import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import quote, urlparse

from kubescope.sdk.errors import first_line

from kubescope.about import __version__
from kubescope.extensions.archive import MAX_ARCHIVE

TIMEOUT = 30  # seconds
_HOSTS = ("api.github.com", "codeload.github.com")
_NAME = r"[A-Za-z0-9_.-]{1,100}"
_REPO = re.compile(
    rf"(?:https://github\.com/)?({_NAME})/({_NAME}?)(?:\.git)?"
    r"(?:/tree/([A-Za-z0-9_./-]{1,200}))?/?"
)


class GithubError(Exception):
    """The repository cannot be fetched; the message says why."""


@dataclass(frozen=True)
class Repo:
    owner: str
    name: str
    ref: str = ""  # a branch, a tag or a commit; empty is the default branch

    @property
    def label(self) -> str:
        return f"{self.owner}/{self.name}" + (f"@{self.ref}" if self.ref else "")

    @property
    def source(self) -> str:
        """How an installed extension remembers where it came from."""
        return f"github {self.label}"

    @property
    def zip_url(self) -> str:
        url = f"https://api.github.com/repos/{self.owner}/{self.name}/zipball"
        return f"{url}/{quote(self.ref, safe='/')}" if self.ref else url


def parse_repo(text: str) -> Repo:
    """A repository from `owner/name` or its GitHub address (a branch or a tag
    may follow `/tree/`)."""
    found = _REPO.fullmatch(text.strip())
    if found is None or ".." in text:
        raise GithubError("Give the repository as owner/name or its GitHub address")
    return Repo(found.group(1), found.group(2), found.group(3) or "")


def repo_of(source: str) -> Repo | None:
    """The repository a `Repo.source` names; None for any other source."""
    if not source.startswith("github "):
        return None
    name, _, ref = source.removeprefix("github ").partition("@")
    return parse_repo(f"{name}/tree/{ref}" if ref else name)


def download(repo: Repo) -> bytes:
    """The zip of the repository."""
    request = urllib.request.Request(
        repo.zip_url,
        headers={
            "User-Agent": f"KubeScope/{__version__}",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if urlparse(response.geturl()).hostname not in _HOSTS:
                raise GithubError("GitHub sent the file from somewhere else")
            data = response.read(MAX_ARCHIVE + 1)
    except urllib.error.HTTPError as error:
        raise GithubError(f"GitHub answered {error.code} for {repo.label}") from error
    except (urllib.error.URLError, OSError) as error:
        raise GithubError(
            f"GitHub could not be reached: {first_line(str(error))}"
        ) from error
    if len(data) > MAX_ARCHIVE:
        raise GithubError("The repository is too big to be an extension")
    return data
