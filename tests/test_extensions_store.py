import io
import json
import shutil
import zipfile
from pathlib import Path

import pytest

from kubescope.extensions.archive import tree_digest
from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.extensions.store import (
    REGISTRY,
    Candidate,
    ExtensionStore,
    StoreError,
)

REQUIRED_FILES = {"LICENSE": b"MIT", "README.md": b"x", "src/__init__.py": b""}


def add_required(folder: Path) -> None:
    for name, data in REQUIRED_FILES.items():
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_bytes(data)


def manifest(extension: str = "dco.tool", version: str = "1.0.0") -> bytes:
    return (
        f'id = "{extension}"\nname = "Tool"\nversion = "{version}"\n'
        'api = "0"\nentry = "tool:activate"\n'
    ).encode()


def make_zip(files: dict[str, bytes]) -> bytes:
    """A zip; next to each manifest it has what an extension must have."""
    files = dict(files)
    for name in [one for one in files if one.endswith(MANIFEST_NAME)]:
        top = name.removesuffix(MANIFEST_NAME)
        for required, data in REQUIRED_FILES.items():
            files.setdefault(f"{top}{required}", data)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, content in files.items():
            zipped.writestr(name, content)
    return buffer.getvalue()


def tool_zip(version: str = "1.0.0", top: str = "", extra: bytes = b"") -> bytes:
    return make_zip(
        {
            f"{top}{MANIFEST_NAME}": manifest(version=version),
            f"{top}src/tool.py": b"def activate(ctx): pass\n" + extra,
        }
    )


def make_bundled(root: Path, extension: str = "kubescope.gabi") -> Path:
    folder = root / "gabi"
    folder.mkdir(parents=True)
    (folder / MANIFEST_NAME).write_bytes(manifest(extension))
    (root / "no_manifest").mkdir()
    (root / "a_file.txt").write_text("x")
    return root


def store_in(tmp_path, bundled: Path | None = None) -> ExtensionStore:
    return ExtensionStore(tmp_path / "ext", bundled)


def install(store: ExtensionStore, data: bytes, source: str = "file tool.zip"):
    return store.install(store.prepare(data, source))


def test_an_archive_is_prepared_and_nothing_is_installed(tmp_path) -> None:
    store = store_in(tmp_path)
    data = tool_zip()

    candidate = store.prepare(data, "file tool.zip")

    assert candidate.manifest.id == "dco.tool"
    assert candidate.source == "file tool.zip"
    assert candidate.sha256 == tree_digest(candidate.folder)  # of the files
    assert candidate.replaces is None and not candidate.content_changed
    assert (candidate.folder / "src" / "tool.py").is_file()
    assert store.installed() == []


def test_the_folder_a_repository_zip_has_on_top_is_looked_into(tmp_path) -> None:
    store = store_in(tmp_path)
    data = make_zip(
        {
            f"dco-tool-abc123/{MANIFEST_NAME}": manifest(),
            "dco-tool-abc123/tool.py": b"",
            "__MACOSX/x": b"",
        }
    )

    candidate = store.prepare(data, "github dco/tool")

    assert candidate.folder.name == "dco-tool-abc123"


@pytest.mark.parametrize(
    "files",
    [
        {"tool.py": b""},
        {"a/tool.py": b"", "b/tool.py": b""},
        {f"a/b/c/d/{MANIFEST_NAME}": manifest()},  # deeper than it is looked for
        {f".git/{MANIFEST_NAME}": manifest()},  # in what a repository carries
    ],
)
def test_an_archive_without_a_manifest_in_reach_is_refused(tmp_path, files) -> None:
    store = store_in(tmp_path)

    with pytest.raises(StoreError, match=f"There is no {MANIFEST_NAME}"):
        store.prepare(make_zip(files), "file x.zip")

    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_the_manifest_is_looked_for_down_the_folders(tmp_path) -> None:
    store = store_in(tmp_path)
    data = make_zip({f"repo-abc/extensions/tool/{MANIFEST_NAME}": manifest()})

    assert store.prepare(data, "github dco/tool").folder.name == "tool"


def test_the_shallowest_manifest_wins_and_two_at_one_depth_are_refused(
    tmp_path,
) -> None:
    store = store_in(tmp_path)
    shallow = make_zip(
        {
            f"{MANIFEST_NAME}": manifest("dco.top"),
            f"examples/one/{MANIFEST_NAME}": manifest("dco.example"),
        }
    )
    twins = make_zip(
        {
            f"a/{MANIFEST_NAME}": manifest("dco.a"),
            f"b/{MANIFEST_NAME}": manifest("dco.b"),
        }
    )

    assert store.prepare(shallow, "file x.zip").manifest.id == "dco.top"
    with pytest.raises(StoreError, match="more than one"):
        store.prepare(twins, "file x.zip")


def test_a_bad_archive_or_manifest_is_refused_and_cleaned_up(tmp_path) -> None:
    store = store_in(tmp_path)

    with pytest.raises(StoreError, match="not a zip"):
        store.prepare(b"nope", "file x.zip")
    with pytest.raises(StoreError, match="id must"):
        store.prepare(make_zip({MANIFEST_NAME: manifest("Bad")}), "file x.zip")

    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_installing_puts_it_in_place_and_remembers_it(tmp_path) -> None:
    store = store_in(tmp_path)

    installed = install(store, tool_zip(), "github dco/tool@v1")

    assert installed.manifest.id == "dco.tool" and not installed.bundled
    assert installed.source == "github dco/tool@v1"
    assert (installed.folder / "src" / "tool.py").is_file()
    assert [one.manifest.id for one in store.installed()] == ["dco.tool"]
    assert store.source_of("dco.tool") == "github dco/tool@v1"
    assert list((tmp_path / "ext" / "staging").iterdir()) == []
    # a new store reads the same from the disk
    again = store_in(tmp_path)
    assert [one.source for one in again.installed()] == ["github dco/tool@v1"]


def test_installing_over_an_extension_replaces_it_and_tells_what_changed(
    tmp_path,
) -> None:
    store = store_in(tmp_path)
    install(store, tool_zip("1.0.0"))

    same = store.prepare(tool_zip("1.0.0"), "file again.zip")
    newer = store.prepare(tool_zip("1.1.0", extra=b"# new\n"), "file new.zip")

    assert same.replaces is not None and same.replaces.version == "1.0.0"
    assert not same.content_changed
    assert newer.content_changed
    store.discard(same)
    store.install(newer)
    assert [one.manifest.version for one in store.installed()] == ["1.1.0"]
    assert not (tmp_path / "ext" / "installed" / "dco.tool.old").exists()


def test_a_folder_that_was_not_prepared_is_refused(tmp_path) -> None:
    store = store_in(tmp_path)
    install(store, tool_zip())
    outside = Candidate(
        manifest=store.installed()[0].manifest,
        source="x",
        sha256="",
        folder=tmp_path,
    )
    inside_not_staged = Candidate(
        manifest=outside.manifest,
        source="x",
        sha256="",
        folder=tmp_path / "ext" / "staging",
    )

    with pytest.raises(StoreError, match="not a prepared extension"):
        store.install(outside)
    with pytest.raises(StoreError, match="not a prepared extension"):
        store.discard(inside_not_staged)


def test_discarding_removes_the_staged_files(tmp_path) -> None:
    store = store_in(tmp_path)
    candidate = store.prepare(tool_zip(top="top/"), "file tool.zip")

    store.discard(candidate)

    assert not candidate.folder.exists()
    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_uninstalling_removes_the_folder_and_the_record(tmp_path) -> None:
    store = store_in(tmp_path)
    installed = install(store, tool_zip())

    store.uninstall("dco.tool")

    assert not installed.folder.exists()
    assert store.installed() == []
    assert store_in(tmp_path).installed() == []
    with pytest.raises(StoreError, match="was not installed from an archive"):
        store.source_of("dco.tool")


def test_uninstalling_what_is_not_there_is_refused(tmp_path) -> None:
    with pytest.raises(StoreError, match="is not installed"):
        store_in(tmp_path).uninstall("dco.nope")


def test_a_bundled_extension_runs_until_it_is_uninstalled(tmp_path) -> None:
    bundled = make_bundled(tmp_path / "bundled")
    store = store_in(tmp_path, bundled)

    [one] = store.installed()
    assert one.bundled and one.source == "bundled"
    assert one.folder == bundled / "gabi"
    assert store.removed_bundled() == []

    store.uninstall("kubescope.gabi")

    assert store.installed() == []
    assert [m.id for m in store.removed_bundled()] == ["kubescope.gabi"]
    assert (bundled / "gabi" / MANIFEST_NAME).is_file()  # the app's files stay
    # the choice survives a restart
    assert store_in(tmp_path, bundled).installed() == []


def test_a_bundled_extension_is_reinstalled_with_a_click(tmp_path) -> None:
    bundled = make_bundled(tmp_path / "bundled")
    store = store_in(tmp_path, bundled)
    store.uninstall("kubescope.gabi")

    store.restore_bundled("kubescope.gabi")

    assert [one.manifest.id for one in store.installed()] == ["kubescope.gabi"]
    assert store.removed_bundled() == []
    with pytest.raises(StoreError, match="was not uninstalled"):
        store.restore_bundled("kubescope.gabi")


def test_an_installed_extension_takes_the_place_of_the_bundled_one(tmp_path) -> None:
    bundled = make_bundled(tmp_path / "bundled")
    store = store_in(tmp_path, bundled)

    candidate = store.prepare(
        make_zip({MANIFEST_NAME: manifest("kubescope.gabi", "2.0.0")}), "file gabi.zip"
    )
    store.install(candidate)

    [one] = store.installed()
    assert not one.bundled and one.manifest.version == "2.0.0"
    store.uninstall(
        "kubescope.gabi"
    )  # the installed copy goes, and the bundled returns
    assert [x.bundled for x in store.installed()] == [True]


def test_a_bundled_uninstalled_and_replaced_is_not_offered_again(tmp_path) -> None:
    bundled = make_bundled(tmp_path / "bundled")
    store = store_in(tmp_path, bundled)
    store.uninstall("kubescope.gabi")
    store.install(
        store.prepare(
            make_zip({MANIFEST_NAME: manifest("kubescope.gabi")}), "file g.zip"
        )
    )

    assert store.removed_bundled() == []


def test_a_missing_bundled_folder_means_none(tmp_path) -> None:
    assert store_in(tmp_path, tmp_path / "nowhere").installed() == []
    assert store_in(tmp_path, None).installed() == []


def test_a_damaged_installed_extension_is_skipped(tmp_path) -> None:
    store = store_in(tmp_path)
    installed = install(store, tool_zip())
    (installed.folder / MANIFEST_NAME).unlink()

    assert store.installed() == []


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        "[1]",
        json.dumps({"installed": [], "removed": {}}),
        json.dumps({"installed": {"Bad Id": {"source": "s", "sha256": "h"}}}),
        json.dumps({"installed": {"dco.a": {"source": 1, "sha256": "h"}}}),
        json.dumps({"installed": {"dco.a": "x"}, "removed": [1, "Bad Id"]}),
    ],
)
def test_a_damaged_registry_is_read_as_far_as_it_makes_sense(tmp_path, content) -> None:
    directory = tmp_path / "ext"
    directory.mkdir()
    (directory / REGISTRY).write_text(content)

    store = ExtensionStore(directory)

    assert store.installed() == []
    assert store.removed_bundled() == []


def test_the_registry_is_trimmed_to_what_it_may_hold(tmp_path) -> None:
    directory = tmp_path / "ext"
    directory.mkdir()
    (directory / REGISTRY).write_text(
        json.dumps(
            {
                "installed": {"dco.a": {"source": "s" * 900, "sha256": "h" * 90}},
                "removed": ["dco.b"],
            }
        )
    )

    store = ExtensionStore(directory)

    assert len(store.source_of("dco.a")) == 500
    assert len(store._installed["dco.a"]["sha256"]) == 64
    assert store._removed == {"dco.b"}


def test_the_same_version_has_the_same_hash_from_a_repository_and_from_a_folder(
    tmp_path,
) -> None:
    store = store_in(tmp_path)
    files = {
        MANIFEST_NAME: manifest(),
        "pkg/__init__.py": b"x = 1\n",
        "README.md": b"hi",
    }
    from_github = store.prepare(
        make_zip({f"dco-tool-abc1234/{name}": data for name, data in files.items()}),
        "github dco/tool@v1",
    )
    source = tmp_path / "checkout"
    (source / "pkg").mkdir(parents=True)
    for name, data in files.items():
        (source / name).write_bytes(data)
    (source / "LICENSE").write_bytes(b"MIT")  # what the zip above gets by itself
    (source / "src").mkdir()
    (source / "src" / "__init__.py").write_bytes(b"")
    (source / ".git").mkdir()
    (source / ".git" / "HEAD").write_text("ref")  # what a checkout carries
    from_folder = store.prepare_folder(source)

    assert from_github.sha256 == from_folder.sha256
    (source / "README.md").write_bytes(b"changed")
    assert store.prepare_folder(source).sha256 != from_github.sha256


def test_the_day_of_the_installation_and_of_the_last_update_are_kept(
    tmp_path, monkeypatch
) -> None:
    from kubescope.extensions import store as store_module

    moments = iter(["2026-01-05T10:00:00+00:00", "2026-03-20T08:30:00+00:00"])
    monkeypatch.setattr(store_module, "_now", lambda: next(moments))
    store = store_in(tmp_path)

    first = install(store, tool_zip("1.0.0"))
    second = install(store, tool_zip("1.1.0", extra=b"# new\n"))

    assert (first.installed_at, first.updated_at) == (
        "2026-01-05T10:00:00+00:00",
        "2026-01-05T10:00:00+00:00",
    )
    assert second.installed_at == "2026-01-05T10:00:00+00:00"  # first time, kept
    assert second.updated_at == "2026-03-20T08:30:00+00:00"
    [read] = store_in(tmp_path).installed()  # and they are on the disk
    assert (read.installed_at, read.updated_at) == (
        second.installed_at,
        second.updated_at,
    )


def test_an_extension_installed_before_the_dates_were_kept_has_those_of_its_folder(
    tmp_path,
) -> None:
    store = store_in(tmp_path)
    install(store, tool_zip())
    registry = tmp_path / "ext" / "registry.json"
    document = json.loads(registry.read_text())
    for entry in document["installed"].values():
        entry.pop("installed_at")
        entry.pop("updated_at")
    registry.write_text(json.dumps(document))

    [read] = store_in(tmp_path).installed()

    assert read.installed_at.startswith("20") and read.updated_at == read.installed_at


def test_a_folder_run_in_place_keeps_its_dates_too(tmp_path) -> None:
    store = store_in(tmp_path)
    folder = tmp_path / "author"
    folder.mkdir()
    add_required(folder)
    (folder / MANIFEST_NAME).write_bytes(manifest())

    linked = store.install(store.prepare_link(folder))

    assert linked.installed_at and linked.updated_at


def test_a_folder_that_cannot_be_read_has_no_date(tmp_path) -> None:
    from kubescope.extensions.store import _modified

    assert _modified(tmp_path / "gone") == ""
    assert _modified(tmp_path).startswith("20")


def test_what_has_an_id_that_is_not_one_is_not_installed(tmp_path) -> None:
    from dataclasses import replace

    store = store_in(tmp_path)
    candidate = store.prepare(tool_zip(), "github dco/tool@v1")
    bad = replace(candidate, manifest=replace(candidate.manifest, id="../x"))

    with pytest.raises(StoreError, match="not a valid id"):
        store.install(bad)


DEVELOPMENT_FILES = {
    "tests/test_x.py": b"x",
    ".github/workflows/ci.yml": b"x",
    "tools/i18n.py": b"x",
    "docs/guide.md": b"x",
    "Makefile": b"x",
    "uv.lock": b"x",
    "pyproject.toml": b"x",
    ".pre-commit-config.yaml": b"x",
    "CHANGELOG.md": b"x",
    "CONTRIBUTING.md": b"x",
    "SECURITY.md": b"x",
    ".gitignore": b"x",
}
KEPT_FILES = {
    "src/dco_tool/__init__.py": b"def go(ctx): ...\n",
    "languages/pt_BR.json": b"{}",
    "README.md": b"readme",
    "LICENSE": b"MIT",
}


def test_an_installed_extension_keeps_only_what_runs(tmp_path) -> None:
    store = store_in(tmp_path)
    files = {**KEPT_FILES, **DEVELOPMENT_FILES, MANIFEST_NAME: manifest()}
    candidate = store.prepare(make_zip(files), "github dco/tool@v1")
    whole = tree_digest(candidate.folder)

    installed = store.install(candidate)

    kept = sorted(
        str(path.relative_to(installed.folder))
        for path in installed.folder.rglob("*")
        if path.is_file()
    )
    assert kept == sorted([*KEPT_FILES, MANIFEST_NAME, "src/__init__.py"])
    # what was checked and what is shown is the whole of what was downloaded
    assert candidate.sha256 == whole and tree_digest(installed.folder) != whole
    assert installed.sha256 == candidate.sha256
    assert [one.sha256 for one in store_in(tmp_path).installed()] == [candidate.sha256]


def test_a_folder_run_in_place_is_never_pruned(tmp_path) -> None:
    store = store_in(tmp_path)
    folder = tmp_path / "author"
    add_required(folder)
    for name, data in {**DEVELOPMENT_FILES, MANIFEST_NAME: manifest()}.items():
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_bytes(data)

    store.install(store.prepare_link(folder))

    assert (folder / "tests" / "test_x.py").is_file() and (
        folder / "Makefile"
    ).is_file()


def test_pruning_keeps_the_top_level_names_it_is_told_to_only(tmp_path) -> None:
    from kubescope.extensions.archive import prune

    (tmp_path / "src" / "tests").mkdir(parents=True)  # inside a kept folder, it stays
    (tmp_path / "src" / "tests" / "data.json").write_text("{}")
    (tmp_path / "tests").mkdir()
    (tmp_path / "Makefile").write_text("x")
    (tmp_path / "keep.py").write_text("x")

    removed = prune(tmp_path, {"src", "keep.py"})

    assert removed == ["Makefile", "tests"]
    assert (tmp_path / "src" / "tests" / "data.json").is_file()
    assert (tmp_path / "keep.py").is_file()


def test_the_manifest_says_what_else_is_for_production(tmp_path) -> None:
    store = store_in(tmp_path)
    text = manifest().decode() + 'production = ["assets/"]\n'
    data = make_zip(
        {
            MANIFEST_NAME: text.encode(),
            "languages/pt_BR.json": b"{}",
            "assets/a.png": b"x",
            "notes.txt": b"x",
        }
    )

    installed = store.install(store.prepare(data, "file tool.zip"))

    assert installed.manifest.production == ("assets",)  # languages is known
    assert sorted(path.name for path in installed.folder.iterdir()) == sorted(
        ["assets", "languages", "src", "LICENSE", "README.md", MANIFEST_NAME]
    )


@pytest.mark.parametrize("missing", ["LICENSE", "README.md", "src/__init__.py"])
def test_an_extension_without_what_is_required_is_refused(tmp_path, missing) -> None:
    store = store_in(tmp_path)
    files = {MANIFEST_NAME: manifest(), **REQUIRED_FILES}
    del files[missing]
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, content in files.items():
            zipped.writestr(name, content)

    with pytest.raises(StoreError, match=f"It lacks {missing.split('/')[0]}"):
        store.prepare(buffer.getvalue(), "file tool.zip")
    folder = tmp_path / "author"
    add_required(folder)
    (folder / MANIFEST_NAME).write_bytes(manifest())
    top = folder / missing.split("/")[0]
    shutil.rmtree(top) if top.is_dir() else top.unlink()
    with pytest.raises(StoreError, match="It lacks"):
        store.prepare_link(folder)


def test_what_was_installed_with_its_whole_repository_is_pruned_later(tmp_path) -> None:
    store = store_in(tmp_path)
    installed = install(store, tool_zip(), "github dco/tool@v1")
    (installed.folder / "tests").mkdir()
    (installed.folder / "tests" / "t.py").write_text("x")
    (installed.folder / "Makefile").write_text("x")
    author = tmp_path / "author"
    author.mkdir()
    add_required(author)
    (author / MANIFEST_NAME).write_bytes(manifest("dco.dev"))
    (author / "tests").mkdir()
    store.install(store.prepare_link(author))

    removed = store.prune_installed()

    assert removed == {"dco.tool": ["Makefile", "tests"]}
    assert (author / "tests").is_dir()  # the folder of an author is never touched
    assert store.prune_installed() == {}  # nothing more
