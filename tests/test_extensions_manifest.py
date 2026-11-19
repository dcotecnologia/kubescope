import pytest

from kubescope.extensions.manifest import (
    MANIFEST_NAME,
    MAX_MANIFEST_BYTES,
    ManifestError,
    parse_manifest,
    read_manifest,
)

GOOD = b"""
id = "dco.gabi"
name = "Gabi"
version = "1.2.3"
api = "0"
entry = "gabi.main:activate"
description = "The assistant"
author = "DCO"
permissions = ["cluster.read", "ui.dock"]
"""


def replaced(old: str, new: str) -> bytes:
    return GOOD.decode().replace(old, new).encode()


def test_a_good_manifest_is_read() -> None:
    manifest = parse_manifest(GOOD)

    assert manifest.id == "dco.gabi"
    assert manifest.name == "Gabi"
    assert manifest.version == "1.2.3"
    assert manifest.entry == "gabi.main:activate"
    assert manifest.permissions == {"cluster.read", "ui.dock"}
    assert manifest.description == "The assistant"
    assert manifest.author == "DCO"


def test_description_author_and_permissions_are_optional() -> None:
    manifest = parse_manifest(
        b'id="a.b"\nname="B"\nversion="0.0.1"\napi="0"\nentry="b:go"\n'
    )

    assert manifest.permissions == frozenset()
    assert manifest.description == manifest.author == ""


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (b"\xff\xfe", "not a valid TOML"),
        (b"id = ", "not a valid TOML"),
        (b"x" * (MAX_MANIFEST_BYTES + 1), "too big"),
        (replaced('id = "dco.gabi"', "id = 3"), "id must be a text"),
        (replaced('id = "dco.gabi"', 'id = ""'), "id must be a text"),
        (replaced('"dco.gabi"', '"Gabi"'), "id must look like"),
        (replaced('"dco.gabi"', '"a/b.c"'), "id must look like"),
        (replaced('"1.2.3"', '"1.2"'), "version must look like"),
        (replaced('api = "0"', 'api = "9"'), "needs the API 9"),
        (replaced('"gabi.main:activate"', '"gabi.main"'), "entry must look like"),
        (replaced('"gabi.main:activate"', '"../x:go"'), "entry must look like"),
        (replaced('["cluster.read", "ui.dock"]', '"cluster.read"'), "list of texts"),
        (replaced('["cluster.read", "ui.dock"]', "[1]"), "list of texts"),
        (replaced('"cluster.read"', '"teleport"'), "unknown permissions: teleport"),
        (replaced('name = "Gabi"', 'name = "' + "x" * 301 + '"'), "name is too long"),
        (replaced('author = "DCO"', "author = 5"), "author must be a text"),
    ],
)
def test_a_manifest_that_does_not_fit_is_refused(content: bytes, message: str) -> None:
    with pytest.raises(ManifestError, match=message):
        parse_manifest(content)


def test_the_manifest_is_read_from_the_folder(tmp_path) -> None:
    (tmp_path / MANIFEST_NAME).write_bytes(GOOD)

    assert read_manifest(tmp_path).id == "dco.gabi"


def test_a_folder_without_a_manifest_is_refused(tmp_path) -> None:
    with pytest.raises(ManifestError, match="could not be read"):
        read_manifest(tmp_path)


def test_a_folder_with_a_huge_manifest_is_refused(tmp_path) -> None:
    (tmp_path / MANIFEST_NAME).write_bytes(b"x" * (MAX_MANIFEST_BYTES + 1))

    with pytest.raises(ManifestError, match="too big"):
        read_manifest(tmp_path)
