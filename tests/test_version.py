import importlib
import importlib.metadata
import re

from kubescope import about


def test_the_version_comes_from_the_installed_package() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+.*", about.__version__)


def test_a_source_tree_that_was_never_installed_reports_an_unknown_version(
    monkeypatch,
) -> None:
    def missing(_name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", missing)
    try:
        reloaded = importlib.reload(about)
        assert reloaded.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(about)


def test_the_project_link_points_at_the_repository() -> None:
    assert about.PROJECT_URL == "https://github.com/dcotecnologia/kubescope"
