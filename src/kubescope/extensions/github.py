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
from xml.etree import ElementTree

from kubescope.sdk.errors import first_line

from kubescope.about import __version__
from kubescope.extensions.archive import MAX_ARCHIVE
from kubescope.extensions.manifest import MANIFEST_NAME, MAX_MANIFEST_BYTES

TIMEOUT = 30  # seconds
_HOSTS = ("github.com", "codeload.github.com")  # the website, never the API,
# whose limit of anonymous requests (60 an hour for an address) a first run can use up
_RAW_HOSTS = ("github.com", "raw.githubusercontent.com")  # the manifest of a tag
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
        ref = quote(self.ref, safe="/") if self.ref else "HEAD"
        return f"https://codeload.github.com/{self.owner}/{self.name}/zip/{ref}"


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


def fetch_manifest(repo: Repo) -> bytes:
    """The manifest of the repository at its ref, which is small: what tells
    whether a version works with this app, without downloading it.

    GitHub sends it from `raw.githubusercontent.com`, and nothing but a
    User-Agent with the app version leaves the app.
    """
    ref = quote(repo.ref, safe="/") if repo.ref else "HEAD"
    request = urllib.request.Request(
        f"https://github.com/{repo.owner}/{repo.name}/raw/{ref}/{MANIFEST_NAME}",
        headers={"User-Agent": f"KubeScope/{__version__}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if urlparse(response.geturl()).hostname not in _RAW_HOSTS:
                raise GithubError("GitHub sent the file from somewhere else")
            data = response.read(MAX_MANIFEST_BYTES + 1)
    except urllib.error.HTTPError as error:
        raise GithubError(f"GitHub answered {error.code} for {repo.label}") from error
    except (urllib.error.URLError, OSError) as error:
        raise GithubError(
            f"GitHub could not be reached: {first_line(str(error))}"
        ) from error
    if len(data) > MAX_MANIFEST_BYTES:
        raise GithubError("The manifest is too big")
    return data


MAX_TAGS_BYTES = 1024 * 1024
_ATOM = "{http://www.w3.org/2005/Atom}"


def list_tags(repo: Repo) -> list[str]:
    """The names of the tags of the repository, the newest first as GitHub
    lists them, read from the feed of its tags on the website."""
    request = urllib.request.Request(
        f"https://github.com/{repo.owner}/{repo.name}/tags.atom",
        headers={"User-Agent": f"KubeScope/{__version__}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if urlparse(response.geturl()).hostname != "github.com":
                raise GithubError("GitHub answered from somewhere else")
            data = response.read(MAX_TAGS_BYTES + 1)
    except urllib.error.HTTPError as error:
        raise GithubError(f"GitHub answered {error.code} for {repo.label}") from error
    except (urllib.error.URLError, OSError) as error:
        raise GithubError(
            f"GitHub could not be reached: {first_line(str(error))}"
        ) from error
    if len(data) > MAX_TAGS_BYTES:
        raise GithubError("GitHub sent too much")
    try:
        feed = ElementTree.fromstring(data)
    except ElementTree.ParseError as error:
        raise GithubError("GitHub answered with something unexpected") from error
    names = [
        entry.findtext(f"{_ATOM}title") or "" for entry in feed.iter(f"{_ATOM}entry")
    ]
    return [name for name in names if name and len(name) <= 100]
