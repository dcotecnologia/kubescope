from pathlib import Path

import pytest

from kubescope.extensions.defaults import DefaultExtension
from kubescope.extensions.github import GithubError, Repo
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Installed
from kubescope.extensions.updates import find, recommended_versions, version_key


def installed(
    version="1.0.0",
    source="github dco/tool@v1.0.0",
    extension="dco.tool",
    dev=False,
    bundled=False,
) -> Installed:
    return Installed(
        Manifest(extension, "Tool", version, "m:f", frozenset()),
        Path("x"),
        source,
        "",
        bundled,
        dev=dev,
    )


class Tags:
    """The tags of a repository, and which repositories were asked."""

    def __init__(self, *names: str) -> None:
        self.names = list(names)
        self.asked: list[Repo] = []

    def __call__(self, repo: Repo) -> list[str]:
        self.asked.append(repo)
        return self.names


def tags_of(*names: str) -> Tags:
    return Tags(*names)


@pytest.mark.parametrize(
    ("text", "key"),
    [("v1.2.3", (1, 2, 3)), ("1.2.3", (1, 2, 3)), (" v0.10.0 ", (0, 10, 0)),
     ("v1.2", None), ("v1.2.3-rc1", None), ("main", None), ("", None)],
)  # fmt: skip
def test_a_version_is_read_from_a_final_tag_only(text, key) -> None:
    assert version_key(text) == key


def test_a_higher_tag_is_an_update_and_the_highest_one_wins() -> None:
    tags = tags_of("v1.1.0", "v1.10.0", "v1.2.0", "v2.0.0-rc1", "nightly")

    [update] = find([installed()], [], tags)

    assert (update.extension, update.current, update.latest) == (
        "dco.tool",
        "1.0.0",
        "v1.10.0",
    )
    assert update.repo == Repo("dco", "tool", "v1.10.0") and update.version == "1.10.0"
    assert update.pin is None
    assert tags.asked == [Repo("dco", "tool")]  # the repository, not its old tag


def test_the_same_or_a_lower_version_is_not_an_update() -> None:
    assert find([installed("1.2.0")], [], tags_of("v1.2.0", "v1.1.0")) == []
    assert find([installed()], [], tags_of("beta", "v1.0.0-rc2")) == []
    assert find([installed()], [], tags_of()) == []


def test_without_the_network_only_what_is_pinned_is_looked_at() -> None:
    assert find([installed()], [], None) == []


def test_what_the_app_recommends_is_updated_to_what_it_pinned_without_the_network() -> (
    None
):
    pin = DefaultExtension(
        "dco.tool", "Tool", "d", Repo("dco", "tool", "v1.0.1"), "a" * 64
    )
    tags = tags_of("v9.9.9")  # never asked: the app decides

    [update] = find([installed()], [pin], tags)

    assert update.latest == "v1.0.1" and update.pin is pin
    assert tags.asked == []
    assert find([installed("1.0.1")], [pin], tags) == []
    assert find([installed("1.0.2")], [pin], tags) == []


def test_what_is_recommended_without_a_pin_is_updated_to_the_latest_release() -> None:
    latest = DefaultExtension("dco.tool", "Tool", "d", Repo("dco", "tool"))
    tags = tags_of("v1.0.0", "v2.0.0", "v2.1.0-rc1")

    [update] = find([installed()], [latest], tags)

    assert update.latest == "v2.0.0" and update.pin is latest  # still checked to be it
    assert tags.asked == [Repo("dco", "tool")]
    assert find([installed("2.0.0")], [latest], tags_of("v2.0.0")) == []


def test_what_is_recommended_without_a_pin_needs_the_network_to_be_updated() -> None:
    latest = DefaultExtension("dco.tool", "Tool", "d", Repo("dco", "tool"))

    assert find([installed()], [latest], None) == []


def test_the_latest_tag_is_the_highest_final_one() -> None:
    from kubescope.extensions.updates import latest_tag

    assert latest_tag(["v1.9.0", "v1.10.0", "main", "v2.0.0-rc1"]) == "v1.10.0"
    assert latest_tag(["main", "nightly"]) is None
    assert latest_tag([]) is None


def test_the_latest_version_of_an_uninstalled_recommendation_is_shown() -> None:
    latest = DefaultExtension("dco.tool", "Tool", "d", Repo("dco", "tool"))
    tags = tags_of("v1.9.0", "v1.10.0", "v2.0.0-rc1", "main")

    assert recommended_versions([latest], set(), tags) == {"dco.tool": "1.10.0"}
    assert tags.asked == [Repo("dco", "tool")]


def test_recommended_versions_skip_installed_pinned_and_unavailable_releases() -> None:
    latest = DefaultExtension("dco.latest", "Latest", "d", Repo("dco", "latest"))
    pinned = DefaultExtension(
        "dco.pinned", "Pinned", "d", Repo("dco", "pinned", "v1.0.0")
    )
    tags = tags_of("main")

    assert recommended_versions([latest, pinned], {"dco.latest"}, tags) == {}
    assert recommended_versions([latest], set(), None) == {}
    assert recommended_versions([latest], set(), tags) == {}
    assert tags.asked == [Repo("dco", "latest")]


def test_a_recommended_repository_that_cannot_be_reached_is_skipped() -> None:
    latest = DefaultExtension("dco.tool", "Tool", "d", Repo("dco", "tool"))

    def tags(_repo: Repo) -> list[str]:
        raise GithubError("rate limit")

    assert recommended_versions([latest], set(), tags) == {}


def test_a_recommended_id_from_another_repository_is_not_taken_for_it() -> None:
    pin = DefaultExtension(
        "dco.tool", "Tool", "d", Repo("dco", "other", "v5.0.0"), "a" * 64
    )

    [update] = find([installed()], [pin], tags_of("v1.1.0"))

    assert update.latest == "v1.1.0" and update.pin is None


@pytest.mark.parametrize(
    "one",
    [
        installed(dev=True),
        installed(bundled=True),
        installed(source="folder /x"),
        installed(source="dev /x"),
        installed(source="github not a repo"),
        installed("not.a.version"),
    ],
)
def test_what_did_not_come_from_a_repository_is_left_alone(one) -> None:
    assert find([one], [], tags_of("v9.0.0")) == []


def test_a_repository_that_cannot_be_reached_does_not_stop_the_others() -> None:
    def tags(repo: Repo) -> list[str]:
        if repo.name == "tool":
            raise GithubError("rate limit")
        return ["v3.0.0"]

    found = find(
        [installed(), installed("1.0.0", "github dco/two@v1.0.0", "dco.two")], [], tags
    )

    assert [one.extension for one in found] == ["dco.two"]
