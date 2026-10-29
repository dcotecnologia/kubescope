import email.message
import urllib.error
from typing import Any, cast

import pytest

from kubescope.utils import updates
from kubescope.utils.updates import Release, UpdateCheck


def _http_error(code: int, message: str) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("u", code, message, email.message.Message(), None)


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
    assert updates._release("not a version") is None
    # a pre-release is a release too, named as the package names its files
    assert updates._release("v0.3.0-beta2") == Release(
        "0.3.0b2",
        "https://github.com/dcotecnologia/kubescope/releases/tag/v0.3.0-beta2",
    )


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

    assert release is not None
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
    fake_api(
        monkeypatch,
        {"/releases/latest": {"tag_name": "v0.3.0-rc1"}, "/releases?per_page=30": []},
    )
    assert updates.latest_release() is None

    fake_api(
        monkeypatch,
        {"/releases/latest": {"tag_name": "v0.3.0", "body": 5, "assets": "x"}},
    )
    assert updates.latest_release() == updates._release("v0.3.0")


def test_release_of_asks_for_the_tag_of_the_version(monkeypatch) -> None:
    asked = fake_api(
        monkeypatch,
        {
            "/releases/tags/v0.3.0": _http_error(404, "no"),
            "/releases/tags/0.3.0": {"tag_name": "0.3.0", "body": "notes"},
        },
    )

    release = updates.release_of("v0.3.0")

    assert release is not None
    assert (release.version, release.notes) == ("0.3.0", "notes")
    assert asked == ["/releases/tags/v0.3.0", "/releases/tags/0.3.0"]


def test_release_of_is_none_for_what_is_not_a_published_version(monkeypatch) -> None:
    missing = _http_error(404, "no")
    fake_api(
        monkeypatch,
        {"/releases/tags/v1.0.0": missing, "/releases/tags/1.0.0": {"tag_name": "x"}},
    )

    assert updates.release_of("latest") is None
    assert updates.release_of("1.0.0") is None


def test_release_of_raises_what_is_not_a_missing_release(monkeypatch) -> None:
    limited = _http_error(403, "limit")
    fake_api(monkeypatch, {"/releases/tags/v1.0.0": limited})

    with pytest.raises(urllib.error.HTTPError):
        updates.release_of("1.0.0")


def test_release_of_ignores_an_answer_that_is_not_a_release(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases/tags/v1.0.0": [], "/releases/tags/1.0.0": 5})

    assert updates.release_of("1.0.0") is None


def _limited(code: int, remaining: str | None, reset: str | None):
    headers = email.message.Message()
    if remaining is not None:
        headers["X-RateLimit-Remaining"] = remaining
    if reset is not None:
        headers["X-RateLimit-Reset"] = reset
    return urllib.error.HTTPError("u", code, "limit", headers, None)


def test_a_check_refused_for_asking_too_often_says_when_it_may_try_again(
    monkeypatch,
) -> None:
    for code in (403, 429):
        fake_api(monkeypatch, {"/releases/latest": _limited(code, "0", "1793302518")})
        assert updates.check_for_update("0.2.0") == UpdateCheck(
            "failed", limited_until=1793302518.0
        )


@pytest.mark.parametrize(
    "error",
    [
        _limited(403, "5", "1793302518"),  # forbidden for another reason
        _limited(403, "0", None),  # no time given
        _limited(429, "0", "soon"),  # a time that is not a number
        _limited(500, "0", "1793302518"),  # not a refusal for asking too often
        urllib.error.HTTPError("u", 403, "limit", cast(Any, None), None),  # no headers
    ],
)
def test_any_other_failure_has_no_time_to_try_again(monkeypatch, error) -> None:
    fake_api(monkeypatch, {"/releases/latest": error})

    assert updates.check_for_update("0.2.0") == UpdateCheck("failed")


@pytest.mark.parametrize(
    ("text", "key"),
    [
        ("1.3.0", (1, 3, 0, 3, 0)),
        ("v1.3.0", (1, 3, 0, 3, 0)),
        ("1.3.0rc1", (1, 3, 0, 2, 1)),
        ("1.3.0-rc.2", (1, 3, 0, 2, 2)),
        ("v1.3.0-rc1", (1, 3, 0, 2, 1)),
        ("v1.3.2a2", (1, 3, 2, 0, 2)),
        ("1.3.0-beta1", (1, 3, 0, 1, 1)),
        ("1.3.0-alpha", (1, 3, 0, 0, 0)),
        ("1.3.0.dev3", (1, 3, 0, -1, 3)),
        ("unknown", None),
        ("1.3", None),
    ],
)
def test_a_version_is_read_as_numbers_that_order_it(text, key) -> None:
    assert updates.release_key(text) == key


def test_the_stages_of_a_version_come_in_order() -> None:
    ordered = [
        "1.3.0.dev1",
        "1.3.0a1",
        "1.3.0a2",
        "1.3.0b1",
        "1.3.0rc1",
        "1.3.0rc2",
        "1.3.0",
        "1.3.1a1",
        "1.4.0",
    ]
    keys = [updates.release_key(text) for text in ordered]

    assert None not in keys and keys == sorted(keys)  # type: ignore[type-var]
    assert len(set(keys)) == len(keys)


@pytest.mark.parametrize(
    ("text", "package", "pre_release"),
    [
        ("v1.3.0", "1.3.0", False),
        ("v1.3.0-rc1", "1.3.0rc1", True),
        ("1.3.0-beta.4", "1.3.0b4", True),
        ("1.3.0-alpha", "1.3.0a0", True),
    ],
)
def test_a_version_is_named_as_the_package_names_its_files(
    text, package, pre_release
) -> None:
    key = updates.release_key(text)

    assert key is not None
    assert updates.package_version(key) == package
    assert updates.is_pre_release(key) is pre_release


def _release_data(tag: str, **flags) -> dict:
    return {"tag_name": tag, **flags}


def test_the_app_is_never_offered_a_pre_release(monkeypatch) -> None:
    for tag, flags in (
        ("v1.3.0-rc1", {"prerelease": True}),
        ("v1.3.0-rc1", {}),  # tagged as one, though GitHub does not say it is
        ("v1.3.0-beta2", {"prerelease": False}),
    ):
        fake_api(
            monkeypatch,
            {
                "/releases/latest": _release_data(tag, **flags),
                "/releases?per_page=30": [],
            },
        )

        assert updates.check_for_update("1.2.0") == UpdateCheck("current")


def test_when_the_newest_release_is_a_pre_release_the_newest_stable_one_is_found(
    monkeypatch,
) -> None:
    listing = [
        _release_data("v1.3.0-rc2", prerelease=True),
        _release_data("v1.3.0-rc1"),
        _release_data("v1.2.1", draft=True),  # not published yet
        _release_data("v1.2.0"),
        _release_data("v1.1.1"),
        "not a release",
    ]
    asked = fake_api(
        monkeypatch,
        {
            "/releases/latest": _release_data("v1.3.0-rc2", prerelease=False),
            "/releases?per_page=30": listing,
        },
    )

    found = updates.check_for_update("1.1.0")

    assert found == UpdateCheck("available", updates._release("v1.2.0"))
    assert asked == ["/releases/latest", "/releases?per_page=30"]
    assert updates.check_for_update("1.2.0") == UpdateCheck("current")


def test_a_stable_latest_release_needs_no_second_question(monkeypatch) -> None:
    asked = fake_api(monkeypatch, {"/releases/latest": _release_data("v1.2.0")})

    updates.check_for_update("1.1.0")

    assert asked == ["/releases/latest"]


def test_a_listing_that_is_not_a_list_leaves_nothing_to_offer(monkeypatch) -> None:
    fake_api(
        monkeypatch,
        {
            "/releases/latest": _release_data("v1.3.0-rc1", prerelease=True),
            "/releases?per_page=30": {"message": "nope"},
        },
    )

    assert updates.check_for_update("1.2.0") == UpdateCheck("current")


def _listing(*tags: str) -> list[dict]:
    return [
        {"tag_name": tag, "prerelease": "-" in tag, "draft": tag.endswith("draft")}
        for tag in tags
    ]


def test_a_release_candidate_is_offered_the_next_pre_release_and_the_stable_one(
    monkeypatch,
) -> None:
    fake_api(
        monkeypatch,
        {
            "/releases?per_page=30": _listing(
                "v1.3.0-rc2", "v1.3.0-rc1", "v1.2.0", "v1.1.0"
            )
        },
    )

    found = updates.check_for_update("1.3.0rc1")

    assert found == UpdateCheck("available", updates._release("v1.3.0-rc2"))
    assert found.release is not None and found.release.version == "1.3.0rc2"
    assert updates.check_for_update("1.3.0rc2") == UpdateCheck("current")  # the newest
    assert updates.check_for_update("1.3.0b9") == UpdateCheck(
        "available", updates._release("v1.3.0-rc2")
    )


def test_a_pre_release_is_offered_the_stable_release_that_follows_it(
    monkeypatch,
) -> None:
    fake_api(
        monkeypatch,
        {"/releases?per_page=30": _listing("v1.3.0", "v1.3.0-rc2", "v1.2.0")},
    )

    assert updates.check_for_update("1.3.0rc2") == UpdateCheck(
        "available", updates._release("v1.3.0")
    )
    assert updates.check_for_update("1.2.5a1") == UpdateCheck(
        "available", updates._release("v1.3.0")
    )


def test_a_pre_release_is_never_offered_an_older_release(monkeypatch) -> None:
    fake_api(
        monkeypatch,
        {"/releases?per_page=30": _listing("v1.2.5", "v1.2.0", "v1.3.0-alpha1")},
    )

    assert updates.check_for_update("1.3.0b1") == UpdateCheck("current")
    assert updates.check_for_update("1.3.0a1") == UpdateCheck("current")  # the same


def test_a_pre_release_looks_among_all_the_releases_and_ignores_drafts(
    monkeypatch,
) -> None:
    asked = fake_api(
        monkeypatch,
        {"/releases?per_page=30": _listing("v1.4.0-rc1draft", "v1.3.0-rc2", "junk")},
    )

    found = updates.latest_release(pre_releases=True)

    assert found == updates._release("v1.3.0-rc2")
    assert asked == ["/releases?per_page=30"]  # it did not ask for the latest one


def test_a_pre_release_with_no_release_to_offer_is_up_to_date(monkeypatch) -> None:
    fake_api(monkeypatch, {"/releases?per_page=30": []})
    assert updates.check_for_update("1.3.0rc1") == UpdateCheck("current")

    fake_api(monkeypatch, {"/releases?per_page=30": {"message": "nope"}})
    assert updates.check_for_update("1.3.0rc1") == UpdateCheck("current")


def test_a_stable_installation_still_hears_of_stable_releases_only(monkeypatch) -> None:
    fake_api(
        monkeypatch,
        {
            "/releases/latest": _release_data("v1.3.0-rc2", prerelease=True),
            "/releases?per_page=30": _listing("v1.3.0-rc2", "v1.2.1", "v1.2.0"),
        },
    )

    assert updates.check_for_update("1.2.0") == UpdateCheck(
        "available", updates._release("v1.2.1")
    )
    assert updates.latest_release_for("1.2.0") == updates._release("v1.2.1")
    assert updates.latest_release_for("1.3.0rc1") == updates._release("v1.3.0-rc2")


def test_the_release_of_a_pre_release_is_looked_up_by_its_tag(monkeypatch) -> None:
    asked = fake_api(
        monkeypatch,
        {
            "/releases/tags/v1.3.0-rc1": _http_error(404, "no"),
            "/releases/tags/1.3.0-rc1": {"tag_name": "1.3.0-rc1", "body": "notes"},
        },
    )

    release = updates.release_of("1.3.0rc1")

    assert release is not None and release.version == "1.3.0rc1"
    assert release.notes == "notes"
    assert asked == ["/releases/tags/v1.3.0-rc1", "/releases/tags/1.3.0-rc1"]
