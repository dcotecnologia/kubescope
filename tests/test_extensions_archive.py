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
