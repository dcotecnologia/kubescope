import hashlib
import io
import json
import zipfile
from pathlib import Path

import pytest

from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.extensions.store import (
    REGISTRY,
    Candidate,
    ExtensionStore,
    StoreError,
)


def manifest(extension: str = "dco.tool", version: str = "1.0.0") -> bytes:
    return (
        f'id = "{extension}"\nname = "Tool"\nversion = "{version}"\n'
        'api = "0"\nentry = "tool:activate"\n'
    ).encode()


def make_zip(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, content in files.items():
            zipped.writestr(name, content)
    return buffer.getvalue()


def tool_zip(version: str = "1.0.0", top: str = "", extra: bytes = b"") -> bytes:
    return make_zip(
        {
            f"{top}{MANIFEST_NAME}": manifest(version=version),
            f"{top}tool.py": b"def activate(ctx): pass\n" + extra,
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
    assert candidate.sha256 == hashlib.sha256(data).hexdigest()
    assert candidate.replaces is None and not candidate.content_changed
    assert (candidate.folder / "tool.py").is_file()
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
    assert (installed.folder / "tool.py").is_file()
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


def test_the_gabi_that_ships_with_the_app_is_a_bundled_extension() -> None:
    from kubescope.extensions import bundled

    store = ExtensionStore(Path("unused"), Path(bundled.__file__).parent)

    [gabi] = store.installed()
    assert gabi.manifest.id == "kubescope.gabi" and gabi.bundled
    assert {"ui.dock", "cli"} <= gabi.manifest.permissions


def make_folder(root: Path, version: str = "1.0.0", extra: str = "") -> Path:
    """An extension as its author has it: code in src, and what a repository
    carries."""
    (root / "src" / "tool").mkdir(parents=True)
    (root / MANIFEST_NAME).write_bytes(manifest(version=version))
    (root / "src" / "tool" / "__init__.py").write_text(
        "def activate(ctx): pass\n" + extra
    )
    (root / ".git").mkdir()
    (root / ".git" / "HEAD").write_text("ref")
    (root / "src" / "tool" / "__pycache__").mkdir()
    (root / "src" / "tool" / "__pycache__" / "x.pyc").write_bytes(b"x")
    return root


def test_a_folder_is_copied_without_what_a_repository_carries(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")

    candidate = store.prepare_folder(source)

    assert candidate.manifest.id == "dco.tool"
    assert candidate.source == f"folder {source}"
    assert (candidate.folder / "src" / "tool" / "__init__.py").is_file()
    assert not (candidate.folder / ".git").exists()
    assert not (candidate.folder / "src" / "tool" / "__pycache__").exists()
    assert store.installed() == []  # nothing is installed yet
    assert source.joinpath(".git", "HEAD").is_file()  # and the author's folder stays


def test_a_folder_is_installed_and_its_content_hash_tells_a_change(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")
    first = store.install(store.prepare_folder(source))
    unchanged = store.prepare_folder(source)
    (source / "src" / "tool" / "__init__.py").write_text("def activate(ctx): 1\n")
    changed = store.prepare_folder(source)

    assert first.source == f"folder {source}"
    assert not unchanged.content_changed
    assert changed.content_changed and changed.replaces is not None


def test_the_manifest_is_found_in_a_subfolder_of_the_folder(tmp_path) -> None:
    store = store_in(tmp_path)
    repository = tmp_path / "repo"
    make_folder(repository / "extensions" / "tool")

    assert store.prepare_folder(repository).manifest.id == "dco.tool"


def test_a_folder_that_is_not_one_or_has_no_manifest_is_refused(tmp_path) -> None:
    store = store_in(tmp_path)
    (tmp_path / "empty").mkdir()

    with pytest.raises(StoreError, match="It is not a folder"):
        store.prepare_folder(tmp_path / "missing")
    with pytest.raises(StoreError, match=f"There is no {MANIFEST_NAME}"):
        store.prepare_folder(tmp_path / "empty")
    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_a_folder_with_a_link_is_refused(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")
    (source / "src" / "link.py").symlink_to(source / "src" / "tool" / "__init__.py")

    with pytest.raises(StoreError, match="It has a link"):
        store.prepare_folder(source)


def test_a_folder_can_be_linked_and_runs_from_where_it_is(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")

    candidate = store.prepare_link(source)
    installed = store.install(candidate)

    assert candidate.dev and candidate.sha256 == ""
    assert candidate.source == f"dev {source.resolve()}"
    assert installed.dev and installed.folder == source.resolve()
    assert [one.dev for one in store.installed()] == [True]
    assert not (tmp_path / "ext" / "installed").exists()  # nothing was copied
    # the registry remembers it, and the manifest is read from the folder again
    (source / MANIFEST_NAME).write_bytes(manifest(version="2.0.0"))
    assert [one.manifest.version for one in store_in(tmp_path).installed()] == ["2.0.0"]


def test_discarding_a_link_never_touches_the_folder_of_the_author(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")

    store.discard(store.prepare_link(source))

    assert (source / MANIFEST_NAME).is_file()


def test_uninstalling_a_link_keeps_the_folder_of_the_author(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")
    store.install(store.prepare_link(source))

    store.uninstall("dco.tool")

    assert store.installed() == []
    assert (source / MANIFEST_NAME).is_file() and (source / "src").is_dir()


def test_linking_replaces_a_copy_and_a_copy_replaces_a_link(tmp_path) -> None:
    store = store_in(tmp_path)
    source = make_folder(tmp_path / "tool")
    copied = install(store, tool_zip())
    store.install(store.prepare_link(source))

    assert not copied.folder.exists()  # the copy is gone
    assert [one.dev for one in store.installed()] == [True]

    store.install(store.prepare_folder(source))  # now a copy again

    [one] = store.installed()
    assert not one.dev and one.folder != source.resolve()
    assert source.is_dir()  # still the author's


def test_a_folder_that_cannot_be_linked_is_refused(tmp_path) -> None:
    store = store_in(tmp_path)
    (tmp_path / "empty").mkdir()

    with pytest.raises(StoreError, match=f"There is no {MANIFEST_NAME}"):
        store.prepare_link(tmp_path / "empty")
    with pytest.raises(StoreError):
        store.prepare_link(tmp_path / "missing")


def test_the_path_of_a_link_is_kept_and_trimmed_in_the_registry(tmp_path) -> None:
    directory = tmp_path / "ext"
    directory.mkdir()
    (directory / REGISTRY).write_text(
        json.dumps(
            {
                "installed": {
                    "dco.a": {"source": "dev x", "sha256": "", "path": "p" * 900},
                    "dco.b": {"source": "dev y", "sha256": "", "path": 5},
                }
            }
        )
    )

    store = ExtensionStore(directory)

    assert len(store._installed["dco.a"]["path"]) == 500
    assert "path" not in store._installed["dco.b"]
