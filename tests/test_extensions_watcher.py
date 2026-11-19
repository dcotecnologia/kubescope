import os

from kubescope.extensions import watcher
from kubescope.extensions.watcher import FolderWatcher


def test_nothing_changed_until_a_file_does(tmp_path) -> None:
    (tmp_path / "a.py").write_text("a")
    folder = FolderWatcher(tmp_path)

    assert not folder.changed()
    (tmp_path / "a.py").write_text("a longer one")
    assert folder.changed()
    assert not folder.changed()  # the change was told once


def test_a_file_added_or_removed_is_a_change(tmp_path) -> None:
    folder = FolderWatcher(tmp_path)

    (tmp_path / "new.py").write_text("x")
    assert folder.changed()
    (tmp_path / "new.py").unlink()
    assert folder.changed()


def test_an_edit_that_keeps_the_size_is_seen_by_its_time(tmp_path) -> None:
    path = tmp_path / "a.py"
    path.write_text("aa")
    folder = FolderWatcher(tmp_path)

    path.write_text("bb")
    os.utime(path, ns=(1, 1))

    assert folder.changed()


def test_what_is_not_code_does_not_count(tmp_path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "__pycache__").mkdir()
    folder = FolderWatcher(tmp_path)

    (tmp_path / ".git" / "HEAD").write_text("x")
    (tmp_path / "__pycache__" / "a.pyc").write_bytes(b"x")
    (tmp_path / "b.pyc").write_bytes(b"x")

    assert not folder.changed()


def test_a_file_that_goes_away_while_scanning_is_skipped(tmp_path, monkeypatch) -> None:
    (tmp_path / "a.py").write_text("a")
    (tmp_path / "b.py").write_text("b")
    real = os.stat

    def stat(path, *args, **kwargs):
        if str(path).endswith("b.py"):
            raise FileNotFoundError(path)
        return real(path, *args, **kwargs)

    monkeypatch.setattr(watcher.os, "stat", stat)

    assert not FolderWatcher(tmp_path).changed()


def test_a_folder_with_too_many_files_is_cut_short(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(watcher, "MAX_FILES", 2)
    for name in "abc":
        (tmp_path / f"{name}.py").write_text(name)

    assert len(FolderWatcher(tmp_path)._seen) == 2
