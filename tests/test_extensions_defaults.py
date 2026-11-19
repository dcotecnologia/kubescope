import pytest

from kubescope.extensions import defaults
from kubescope.extensions.defaults import DefaultExtension, offered, verify
from kubescope.extensions.github import Repo
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Candidate, StoreError

PIN = "a" * 64

REAL = defaults.DEFAULTS  # the tests start with none, so that none reaches GitHub


def wanted(sha256: str = PIN, ref: str = "v1.0.0") -> DefaultExtension:
    return DefaultExtension(
        "kubescope.gabi", "Gabi", "The assistant", Repo("dco", "gabi", ref), sha256
    )


def candidate(extension: str = "kubescope.gabi", sha256: str = PIN) -> Candidate:
    manifest = Manifest(extension, "Gabi", "1.0.0", "x:go", frozenset())
    return Candidate(manifest, "github dco/gabi@v1.0.0", sha256, folder=None)  # type: ignore[arg-type]


def test_an_extension_is_pinned_when_it_has_a_tag_and_a_sha256() -> None:
    assert wanted().pinned
    assert not wanted(sha256="").pinned
    assert not wanted(sha256="abc").pinned
    assert not wanted(ref="").pinned


def test_what_the_app_recommends_is_offered(monkeypatch) -> None:
    monkeypatch.setattr(defaults, "DEFAULTS", (wanted(), wanted(sha256="")))

    assert offered() == (wanted(), wanted(sha256=""))


def test_the_recommended_extensions_are_the_latest_release_of_their_repositories() -> (
    None
):
    gabi, aws, search = REAL

    assert (gabi.id, gabi.repo.owner, gabi.repo.name) == (
        "kubescope.gabi",
        "dcotecnologia",
        "kubescope-ai-gabi",
    )
    assert (aws.id, aws.repo.owner, aws.repo.name) == (
        "kubescope.aws",
        "dcotecnologia",
        "kubescope-aws",
    )
    assert (search.id, search.repo.name) == ("kubescope.search", "kubescope-search")
    assert search.automatic  # it comes with the app, like Gabi
    for one in REAL:
        assert one.repo.ref == "" and one.sha256 == "" and not one.pinned  # the latest
    assert gabi.automatic and not aws.automatic  # Gabi comes with the app


def test_without_a_hash_any_files_of_that_extension_are_accepted() -> None:
    verify(candidate(sha256="b" * 64), wanted(sha256="", ref=""))
    with pytest.raises(StoreError, match="That is not Gabi"):
        verify(candidate(extension="dco.other"), wanted(sha256=""))


def test_what_was_pinned_is_accepted() -> None:
    verify(candidate(), wanted())


def test_another_extension_is_refused() -> None:
    with pytest.raises(StoreError, match="That is not Gabi: it is dco.other"):
        verify(candidate(extension="dco.other"), wanted())


def test_files_that_are_not_the_checked_ones_are_refused() -> None:
    with pytest.raises(StoreError, match="not the ones that were checked"):
        verify(candidate(sha256="b" * 64), wanted())


def test_the_names_shown_before_the_download_are_the_ones_of_the_manifests() -> None:
    assert [one.name for one in REAL] == [
        "Gabi - AI Assistant",
        "AWS Resources",
        "Global Search",
    ]
