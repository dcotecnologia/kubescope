import pytest

from kubescope.extensions import defaults
from kubescope.extensions.defaults import DefaultExtension, offered, verify
from kubescope.extensions.github import Repo
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Candidate, StoreError

PIN = "a" * 64


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


def test_only_what_is_pinned_is_offered(monkeypatch) -> None:
    monkeypatch.setattr(defaults, "DEFAULTS", (wanted(), wanted(sha256="")))

    assert offered() == (wanted(),)


def test_gabi_is_offered_by_a_tag_and_only_once_it_is_pinned() -> None:
    [gabi] = defaults.DEFAULTS

    assert (gabi.id, gabi.repo.owner, gabi.repo.name) == (
        "kubescope.gabi",
        "dcotecnologia",
        "kubescope-gabi",
    )
    assert gabi.repo.ref  # a tag, never the default branch
    assert gabi.pinned == bool(gabi.sha256)  # nothing is offered without a hash


def test_what_was_pinned_is_accepted() -> None:
    verify(candidate(), wanted())


def test_another_extension_is_refused() -> None:
    with pytest.raises(StoreError, match="That is not Gabi: it is dco.other"):
        verify(candidate(extension="dco.other"), wanted())


def test_files_that_are_not_the_checked_ones_are_refused() -> None:
    with pytest.raises(StoreError, match="not the ones that were checked"):
        verify(candidate(sha256="b" * 64), wanted())
