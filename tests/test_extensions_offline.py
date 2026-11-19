import importlib.util
import json
from pathlib import Path

import pytest

from kubescope.extensions import offline
from kubescope.extensions.github import Repo
from kubescope.extensions.offline import snapshot


def keep(folder: Path, extension: str, data: bytes, recorded: object) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{extension}.zip").write_bytes(data)
    (folder / f"{extension}.json").write_text(json.dumps(recorded))


def test_the_copy_that_ships_with_the_app_is_read_with_where_it_came_from(
    tmp_path,
) -> None:
    keep(tmp_path, "dco.tool", b"zip", {"repo": "dco/tool", "tag": "v1.2.0"})

    found = snapshot("dco.tool", tmp_path)

    assert found is not None
    assert found.data == b"zip" and found.repo == Repo("dco", "tool", "v1.2.0")
    assert found.repo.source == "github dco/tool@v1.2.0"  # updates can follow it


def test_without_a_copy_there_is_none(tmp_path) -> None:
    assert snapshot("dco.tool", tmp_path) is None
    assert snapshot("dco.tool") is None  # the folder of the app, when run from sources


@pytest.mark.parametrize(
    "recorded",
    [
        "not an object",
        {"repo": "dco/tool"},
        {"tag": "v1"},
        {"repo": "not a repo", "tag": "v1"},
        {"repo": "dco/tool", "tag": "../x"},
        {"repo": 5, "tag": "v1"},
    ],
)
def test_a_record_that_does_not_fit_is_ignored(tmp_path, recorded) -> None:
    keep(tmp_path, "dco.tool", b"zip", recorded)

    assert snapshot("dco.tool", tmp_path) is None


def test_a_copy_that_is_too_big_is_ignored(tmp_path, monkeypatch) -> None:
    keep(tmp_path, "dco.tool", b"zip", {"repo": "dco/tool", "tag": "v1"})
    monkeypatch.setattr(offline, "MAX_ARCHIVE", 2)

    assert snapshot("dco.tool", tmp_path) is None


def test_a_record_that_is_not_json_is_ignored(tmp_path) -> None:
    keep(tmp_path, "dco.tool", b"zip", {})
    (tmp_path / "dco.tool.json").write_text("{")

    assert snapshot("dco.tool", tmp_path) is None


def load_tool():
    path = Path(__file__).resolve().parent.parent / "tools" / "bundle_extensions.py"
    spec = importlib.util.spec_from_file_location("bundle_extensions", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_build_keeps_the_latest_release_of_each_extension_installed_by_default(
    tmp_path, monkeypatch, capsys
) -> None:
    from kubescope.extensions import defaults, github
    from kubescope.extensions.defaults import DefaultExtension

    monkeypatch.setattr(
        defaults,
        "DEFAULTS",
        (
            DefaultExtension("dco.tool", "Tool", "d", Repo("dco", "tool")),
            DefaultExtension("dco.pinned", "P", "d", Repo("dco", "pinned", "v3.0.0")),
            DefaultExtension(
                "dco.card", "C", "d", Repo("dco", "card"), automatic=False
            ),
            DefaultExtension("dco.none", "N", "d", Repo("dco", "none")),
            DefaultExtension("dco.down", "D", "d", Repo("dco", "down")),
        ),
    )
    tags = {
        "tool": ["v1.0.0", "v1.1.0", "main"],
        "none": ["main"],
        "down": ["v1.0.0"],
    }
    monkeypatch.setattr(github, "list_tags", lambda repo: tags[repo.name])

    def fetch(repo):
        if repo.name == "down":
            raise github.GithubError("GitHub answered 403")
        return f"zip of {repo.label}".encode()

    monkeypatch.setattr(github, "download", fetch)

    done = load_tool().bundle(tmp_path)

    assert done == 2  # tool and pinned; the card is not installed by default
    assert (tmp_path / "dco.tool.zip").read_bytes() == b"zip of dco/tool@v1.1.0"
    assert json.loads((tmp_path / "dco.tool.json").read_text()) == {
        "repo": "dco/tool",
        "tag": "v1.1.0",
    }
    assert json.loads((tmp_path / "dco.pinned.json").read_text())["tag"] == "v3.0.0"
    assert not (tmp_path / "dco.card.zip").exists()
    errors = capsys.readouterr().err
    assert "no copy of dco.none: dco/none has no release yet" in errors
    assert "no copy of dco.down" in errors and "403" in errors
