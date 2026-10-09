import importlib
import re

import kubescope


def test_the_version_comes_from_the_installed_package() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+.*", kubescope.__version__)


def test_a_source_tree_that_was_never_installed_reports_an_unknown_version(
    monkeypatch,
) -> None:
    def missing(_name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", missing)
    try:
        reloaded = importlib.reload(kubescope)
        assert reloaded.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(kubescope)


def test_the_project_link_points_at_the_repository() -> None:
    assert kubescope.PROJECT_URL == "https://github.com/dcotecnologia/kubescope"
