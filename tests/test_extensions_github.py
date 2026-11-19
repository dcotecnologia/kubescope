import io
import urllib.error
from email.message import Message

import pytest

from kubescope.extensions import github
from kubescope.extensions.github import (
    GithubError,
    Repo,
    download,
    parse_repo,
    repo_of,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("dco/gabi", Repo("dco", "gabi")),
        ("https://github.com/dco/gabi", Repo("dco", "gabi")),
        ("https://github.com/dco/gabi.git", Repo("dco", "gabi")),
        ("https://github.com/dco/gabi/", Repo("dco", "gabi")),
        (" dco/gabi ", Repo("dco", "gabi")),
        ("https://github.com/dco/gabi/tree/v1.2", Repo("dco", "gabi", "v1.2")),
        (
            "https://github.com/dco/gabi/tree/feature/x",
            Repo("dco", "gabi", "feature/x"),
        ),
    ],
)
def test_a_repository_is_read_from_its_name_or_address(text, expected) -> None:
    assert parse_repo(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "gabi",
        "https://evil.example/dco/gabi",
        "http://github.com/dco/gabi",
        "dco/gabi/tree/../x",
        "a b/c",
    ],
)
def test_what_is_not_a_repository_is_refused(text) -> None:
    with pytest.raises(GithubError, match="owner/name"):
        parse_repo(text)


def test_the_label_and_the_url_follow_the_ref() -> None:
    assert Repo("dco", "gabi").label == "dco/gabi"
    assert (
        Repo("dco", "gabi").zip_url == "https://codeload.github.com/dco/gabi/zip/HEAD"
    )
    assert Repo("dco", "gabi", "feature/x").label == "dco/gabi@feature/x"
    assert Repo("dco", "gabi", "feature/x").zip_url.endswith("/zip/feature/x")


class Response:
    def __init__(self, data: bytes, url: str) -> None:
        self._data, self._url = data, url

    def __enter__(self):
        return self

    def __exit__(self, *_exc) -> None:
        return None

    def geturl(self) -> str:
        return self._url

    def read(self, limit: int) -> bytes:
        return self._data[:limit]


def fake(monkeypatch, outcome) -> list:
    sent: list = []

    def urlopen(request, timeout):
        sent.append((request, timeout))
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    monkeypatch.setattr(github.urllib.request, "urlopen", urlopen)
    return sent


def test_the_zip_is_downloaded_with_only_a_user_agent(monkeypatch) -> None:
    sent = fake(monkeypatch, Response(b"zip", "https://codeload.github.com/x"))

    assert download(Repo("dco", "gabi")) == b"zip"
    request, timeout = sent[0]
    assert request.full_url == "https://codeload.github.com/dco/gabi/zip/HEAD"
    assert request.get_header("User-agent").startswith("KubeScope/")
    assert set(request.headers) == {"User-agent", "Accept"}
    assert timeout == github.TIMEOUT


def test_a_file_sent_from_another_host_is_refused(monkeypatch) -> None:
    fake(monkeypatch, Response(b"zip", "https://evil.example/x.zip"))

    with pytest.raises(GithubError, match="somewhere else"):
        download(Repo("dco", "gabi"))


def test_an_http_error_says_the_code(monkeypatch) -> None:
    error = urllib.error.HTTPError("u", 404, "Not Found", Message(), io.BytesIO(b""))
    fake(monkeypatch, error)

    with error, pytest.raises(GithubError, match="answered 404 for dco/gabi"):
        download(Repo("dco", "gabi"))


def test_a_network_failure_says_why(monkeypatch) -> None:
    fake(monkeypatch, urllib.error.URLError("no route"))

    with pytest.raises(GithubError, match="could not be reached: .*no route"):
        download(Repo("dco", "gabi"))


def test_a_repository_too_big_is_refused(monkeypatch) -> None:
    monkeypatch.setattr(github, "MAX_ARCHIVE", 3)
    fake(monkeypatch, Response(b"abcdef", "https://codeload.github.com/x"))

    with pytest.raises(GithubError, match="too big"):
        download(Repo("dco", "gabi"))


def test_a_repository_is_remembered_by_its_source_and_found_again() -> None:
    for repo in (Repo("dco", "gabi"), Repo("dco", "gabi", "feature/x")):
        assert repo.source == f"github {repo.label}"
        assert repo_of(repo.source) == repo


def test_a_source_that_is_not_a_repository_is_none_or_refused() -> None:
    assert repo_of("file gabi.zip") is None
    assert repo_of("bundled") is None
    with pytest.raises(GithubError, match="owner/name"):
        repo_of("github ../x")


FEED = (
    b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'
    b"<entry><title>v1.1.0</title></entry><entry><title>v1.0.0</title></entry>"
    b"<entry><link/></entry><entry><title>" + b"x" * 101 + b"</title></entry></feed>"
)


def test_the_tags_are_listed_from_the_website_with_only_a_user_agent(
    monkeypatch,
) -> None:
    sent = fake(monkeypatch, Response(FEED, "https://github.com/dco/gabi/tags.atom"))

    assert github.list_tags(Repo("dco", "gabi")) == ["v1.1.0", "v1.0.0"]
    request, timeout = sent[0]
    assert request.full_url == "https://github.com/dco/gabi/tags.atom"  # not the API
    assert set(request.headers) == {"User-agent"} and timeout == github.TIMEOUT


@pytest.mark.parametrize(
    ("outcome", "message"),
    [
        (Response(FEED, "https://evil.example/tags"), "somewhere else"),
        (
            Response(b"x" * (github.MAX_TAGS_BYTES + 1), "https://github.com/x"),
            "too much",
        ),
        (Response(b"not xml", "https://github.com/x"), "unexpected"),
        (urllib.error.URLError("no route"), "could not be reached"),
        (urllib.error.HTTPError("u", 404, "no", {}, None), "answered 404"),  # type: ignore[arg-type]
    ],
)
def test_tags_that_cannot_be_read_say_why(monkeypatch, outcome, message) -> None:
    fake(monkeypatch, outcome)

    with pytest.raises(GithubError, match=message):
        github.list_tags(Repo("dco", "gabi"))
