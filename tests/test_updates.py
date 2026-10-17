import pytest

from kubescope.utils import updates
from kubescope.utils.updates import Release, UpdateCheck


@pytest.mark.parametrize(
    ("tag", "version"),
    [("v1.2.3", (1, 2, 3)), ("0.10.0", (0, 10, 0)), (" v2.0.1 ", (2, 0, 1))],
)
def test_parse_version_reads_release_tags(tag, version) -> None:
    assert updates.parse_version(tag) == version


@pytest.mark.parametrize("tag", ["v1.2.3-rc1", "v1.2", "latest", "", "v1.2.3.4"])
def test_parse_version_ignores_what_is_not_a_release(tag) -> None:
    assert updates.parse_version(tag) is None


def test_release_links_point_at_this_project_whatever_the_answer_says() -> None:
    release = updates._release("v0.3.0")

    assert release == Release(
        "0.3.0", "https://github.com/dcotecnologia/kubescope/releases/tag/v0.3.0"
    )
    assert updates._release("v0.3.0-beta") is None


def fake_api(monkeypatch, answers: dict) -> list[str]:
    asked = []

    def get(path: str):
        asked.append(path)
        answer = answers[path]
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(updates, "_get", get)
    return asked


def test_latest_release_uses_the_latest_published_release(monkeypatch) -> None:
    asked = fake_api(monkeypatch, {"/releases/latest": {"tag_name": "v0.3.0"}})

    assert updates.latest_release() == updates._release("v0.3.0")
    assert asked == ["/releases/latest"]


def test_latest_release_falls_back_to_the_highest_tag(monkeypatch) -> None:
    tags = [
        {"name": "v0.9.0"},
        {"name": "v0.10.0"},
        {"name": "nightly"},
        {"name": "v0.11.0-rc1"},
        {"name": 5},
        "junk",
    ]
    fake_api(monkeypatch, {"/releases/latest": {"message": "Not Found"}, "/tags": tags})

    assert updates.latest_release() == updates._release("v0.10.0")


def test_latest_release_is_none_without_releases_or_version_tags(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases/latest": [], "/tags": [{"name": "nightly"}]})

    assert updates.latest_release() is None


def test_get_asks_github_over_https_and_says_which_version_it_is(monkeypatch) -> None:
    seen = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

        def read(self, *_args):
            return b'{"tag_name": "v1.0.0"}'

    def urlopen(request, timeout):
        seen.update(url=request.full_url, headers=dict(request.header_items()))
        seen["timeout"] = timeout
        return Response()

    monkeypatch.undo()  # the tests' offline guard
    monkeypatch.setattr(updates.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(updates, "__version__", "0.2.0")

    assert updates._get("/releases/latest") == {"tag_name": "v1.0.0"}
    assert seen["url"] == (
        "https://api.github.com/repos/dcotecnologia/kubescope/releases/latest"
    )
    assert seen["headers"]["User-agent"] == "KubeScope/0.2.0"
    assert seen["timeout"] == updates.TIMEOUT


def test_check_for_update_reports_newer_equal_and_older_versions(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases/latest": {"tag_name": "v0.3.0"}})

    newer = updates.check_for_update("0.2.0")
    assert newer == UpdateCheck("available", updates._release("v0.3.0"))
    assert updates.check_for_update("0.3.0") == UpdateCheck("current")
    assert updates.check_for_update("1.0.0") == UpdateCheck("current")
    assert updates.check_for_update("unknown") == UpdateCheck("current")


def test_check_for_update_with_nothing_published_is_current(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases/latest": [], "/tags": []})

    assert updates.check_for_update("0.2.0") == UpdateCheck("current")


@pytest.mark.parametrize(
    "error", [OSError("offline"), ValueError("not json"), TimeoutError("slow")]
)
def test_check_for_update_never_raises(monkeypatch, error) -> None:
    fake_api(monkeypatch, {"/releases/latest": error})

    assert updates.check_for_update("0.2.0") == UpdateCheck("failed")


def test_latest_release_carries_the_notes_and_the_verified_files(monkeypatch) -> None:
    digest = "a" * 64
    fake_api(
        monkeypatch,
        {
            "/releases/latest": {
                "tag_name": "v0.3.0",
                "body": "  ## Fixed\n- a thing  ",
                "assets": [
                    {"name": "kubescope_0.3.0_amd64.deb", "digest": f"sha256:{digest}"},
                    {"name": "no-digest.AppImage", "digest": None},
                    {"name": "../escape", "digest": f"sha256:{digest}"},
                    "not an asset",
                ],
            }
        },
    )

    release = updates.latest_release()

    assert release.notes == "## Fixed\n- a thing"
    assert release.assets == (
        updates.Asset(
            "kubescope_0.3.0_amd64.deb",
            "https://github.com/dcotecnologia/kubescope/releases/download/v0.3.0/"
            "kubescope_0.3.0_amd64.deb",
            digest,
        ),
    )


def test_a_latest_release_with_an_odd_tag_or_body_is_tolerated(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases/latest": {"tag_name": "v0.3.0-rc1"}})
    assert updates.latest_release() is None

    fake_api(
        monkeypatch,
        {"/releases/latest": {"tag_name": "v0.3.0", "body": 5, "assets": "x"}},
    )
    assert updates.latest_release() == updates._release("v0.3.0")
