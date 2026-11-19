import io
import stat
import zipfile

import pytest

from kubescope.extensions import archive
from kubescope.extensions.archive import ArchiveError, extract


def make_zip(files: dict[str, bytes], links: tuple[str, ...] = ()) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, content in files.items():
            zipped.writestr(name, content)
        for name in links:
            info = zipfile.ZipInfo(name)
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zipped.writestr(info, "target")
    return buffer.getvalue()


def test_files_and_folders_are_unpacked(tmp_path) -> None:
    extract(make_zip({"a/b.txt": b"hi", "c/": b""}), tmp_path)

    assert (tmp_path / "a" / "b.txt").read_bytes() == b"hi"
    assert (tmp_path / "c").is_dir()


@pytest.mark.parametrize(
    "name",
    ["../x.txt", "a/../../x.txt", "/etc/x", "C:/x", "a\\b.txt"],
)
def test_a_name_that_leaves_the_folder_is_refused(tmp_path, name) -> None:
    with pytest.raises(ArchiveError, match="unsafe name"):
        extract(make_zip({name: b"x"}), tmp_path)

    assert list(tmp_path.iterdir()) == []


def test_a_link_is_refused(tmp_path) -> None:
    with pytest.raises(ArchiveError, match="It has a link"):
        extract(make_zip({}, links=("a",)), tmp_path)


def test_a_repeated_name_is_refused(tmp_path) -> None:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        zipped.writestr("a.txt", "1")
        with pytest.warns(UserWarning):
            zipped.writestr("a.txt", "2")

    with pytest.raises(ArchiveError, match="twice"):
        extract(buffer.getvalue(), tmp_path)


def test_something_that_is_not_a_zip_is_refused(tmp_path) -> None:
    with pytest.raises(ArchiveError, match="not a zip"):
        extract(b"nope", tmp_path)


def test_an_archive_too_big_is_refused(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(archive, "MAX_ARCHIVE", 10)

    with pytest.raises(ArchiveError, match="too big to be"):
        extract(make_zip({"a": b"x" * 100}), tmp_path)


def test_too_many_files_are_refused(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(archive, "MAX_FILES", 2)

    with pytest.raises(ArchiveError, match="too many files"):
        extract(make_zip({"a": b"1", "b": b"2", "c": b"3"}), tmp_path)


def test_more_data_than_allowed_is_refused_as_it_is_written(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setattr(archive, "MAX_UNPACKED", 100)

    with pytest.raises(ArchiveError, match="too big once unpacked"):
        extract(make_zip({"a": b"x" * 200}), tmp_path)


def make_tree(root):
    (root / "src").mkdir(parents=True)
    (root / "src" / "a.py").write_text("a")
    (root / "b.txt").write_text("b")
    return root


def test_a_folder_is_copied_in_order_and_what_is_ignored_is_left_out(tmp_path) -> None:
    source = make_tree(tmp_path / "source")
    (source / ".git").mkdir()
    (source / ".git" / "HEAD").write_text("x")
    (source / "src" / "__pycache__").mkdir()
    (source / "src" / "__pycache__" / "a.pyc").write_bytes(b"x")
    target = tmp_path / "target"
    target.mkdir()

    archive.copy_tree(source, target)

    assert sorted(p.relative_to(target).as_posix() for p in target.rglob("*")) == [
        "b.txt",
        "src",
        "src/a.py",
    ]


def test_a_folder_with_a_link_is_refused_whether_file_or_folder(tmp_path) -> None:
    source = make_tree(tmp_path / "source")
    target = tmp_path / "target"
    target.mkdir()
    (source / "alias.py").symlink_to(source / "b.txt")
    with pytest.raises(ArchiveError, match="It has a link: 'alias.py'"):
        archive.copy_tree(source, target)

    (source / "alias.py").unlink()
    (source / "elsewhere").symlink_to(tmp_path)
    with pytest.raises(ArchiveError, match="It has a link: 'elsewhere'"):
        archive.copy_tree(source, target)


def test_a_missing_folder_is_refused(tmp_path) -> None:
    with pytest.raises(ArchiveError, match="not a folder"):
        archive.copy_tree(tmp_path / "missing", tmp_path)


def test_a_folder_with_too_many_files_or_bytes_is_refused(
    tmp_path, monkeypatch
) -> None:
    source = make_tree(tmp_path / "source")
    target = tmp_path / "target"
    target.mkdir()

    monkeypatch.setattr(archive, "MAX_FILES", 1)
    with pytest.raises(ArchiveError, match="too many files"):
        archive.copy_tree(source, target)

    monkeypatch.setattr(archive, "MAX_FILES", 10)
    monkeypatch.setattr(archive, "MAX_UNPACKED", 1)
    with pytest.raises(ArchiveError, match="It is too big"):
        archive.copy_tree(source, target)


def test_the_digest_follows_the_paths_and_the_content(tmp_path) -> None:
    one = make_tree(tmp_path / "one")
    two = make_tree(tmp_path / "two")
    same = archive.tree_digest(one)

    assert archive.tree_digest(two) == same
    (two / "b.txt").write_text("changed")
    assert archive.tree_digest(two) != same
    (two / "b.txt").write_text("b")
    (two / "b.txt").rename(two / "c.txt")
    assert archive.tree_digest(two) != same


def test_a_file_that_would_land_outside_through_a_link_in_the_folder_is_refused(
    tmp_path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    destination = tmp_path / "out"
    destination.mkdir()
    (destination / "link").symlink_to(outside)  # the folder already has a link
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        zipped.writestr("link/evil.txt", "x")

    with pytest.raises(ArchiveError, match="leaves the folder"):
        extract(buffer.getvalue(), destination)
    assert not (outside / "evil.txt").exists()
