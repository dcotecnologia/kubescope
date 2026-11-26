import pytest

from kubescope.extensions.manifest import (
    MANIFEST_NAME,
    MAX_MANIFEST_BYTES,
    ManifestError,
    parse_manifest,
    read_manifest,
)

GOOD = b"""
id = "kubescope.gabi"
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

    assert manifest.id == "kubescope.gabi"
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
        (replaced('id = "kubescope.gabi"', "id = 3"), "id must be a text"),
        (replaced('id = "kubescope.gabi"', 'id = ""'), "id must be a text"),
        (replaced('"kubescope.gabi"', '"Gabi"'), "id must look like"),
        (replaced('"kubescope.gabi"', '"a/b.c"'), "id must look like"),
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

    assert read_manifest(tmp_path).id == "kubescope.gabi"


def test_a_folder_without_a_manifest_is_refused(tmp_path) -> None:
    with pytest.raises(ManifestError, match="could not be read"):
        read_manifest(tmp_path)


def test_a_folder_with_a_huge_manifest_is_refused(tmp_path) -> None:
    (tmp_path / MANIFEST_NAME).write_bytes(b"x" * (MAX_MANIFEST_BYTES + 1))

    with pytest.raises(ManifestError, match="too big"):
        read_manifest(tmp_path)


def test_the_commands_an_extension_adds_are_in_the_manifest() -> None:
    manifest = parse_manifest(
        GOOD.replace(
            b'permissions = ["cluster.read", "ui.dock"]', b'permissions = ["cli"]'
        )
        + b'commands = ["chat", "ask-me"]\n'
    )

    assert manifest.commands == ("chat", "ask-me")
    assert parse_manifest(GOOD).commands == ()


@pytest.mark.parametrize(
    "commands",
    [
        '"chat"',
        "[1]",
        '["Chat"]',
        '["chat", "chat"]',
        '["with space"]',
        '["1st"]',
        "[" + ", ".join(f'"c{i}"' for i in range(9)) + "]",
    ],
)
def test_commands_that_do_not_fit_are_refused(commands) -> None:
    content = (
        GOOD.replace(
            b'permissions = ["cluster.read", "ui.dock"]', b'permissions = ["cli"]'
        )
        + f"commands = {commands}\n".encode()
    )

    with pytest.raises(ManifestError, match="commands must be"):
        parse_manifest(content)


def test_commands_need_the_permission_to_add_them() -> None:
    with pytest.raises(ManifestError, match="need the permission cli"):
        parse_manifest(GOOD + b'commands = ["chat"]\n')


def test_what_is_for_production_is_read_and_the_required_is_always_kept() -> None:
    manifest = parse_manifest(GOOD + b'production = ["languages", "src", "assets/"]\n')

    assert manifest.production == ("assets",)  # languages and src are known
    assert manifest.kept == {
        MANIFEST_NAME,
        "LICENSE",
        "README.md",
        "src",
        "languages",
        "assets",
    }
    assert parse_manifest(GOOD).production == ()


@pytest.mark.parametrize(
    "value", ['"src"', "[1]", '["../x"]', '["a/b"]', '["/etc"]', '[""]', '["."]']
)
def test_production_must_list_names_at_the_top(value) -> None:
    with pytest.raises(ManifestError, match="production"):
        parse_manifest(GOOD + f"production = {value}\n".encode())


def test_an_extension_that_needs_a_newer_app_is_refused(monkeypatch) -> None:
    from kubescope.extensions import manifest as manifest_module

    monkeypatch.setattr(manifest_module, "__version__", "2.3.1")
    needing = GOOD + b'min_app = "2.4.0"\n'

    with pytest.raises(ManifestError, match="needs KubeScope 2.4.0 or later"):
        parse_manifest(needing)

    monkeypatch.setattr(manifest_module, "__version__", "2.4.0")
    assert parse_manifest(needing).min_app == "2.4.0"  # this app is enough
    monkeypatch.setattr(manifest_module, "__version__", "2.10.0")
    assert parse_manifest(needing).min_app == "2.4.0"  # compared as numbers


def test_min_app_is_optional_and_must_be_a_version(monkeypatch) -> None:
    from kubescope.extensions import manifest as manifest_module

    assert parse_manifest(GOOD).min_app == ""
    with pytest.raises(ManifestError, match="min_app must look like 2.4.0"):
        parse_manifest(GOOD + b'min_app = "soon"\n')
    with pytest.raises(ManifestError, match="min_app must be a text"):
        parse_manifest(GOOD + b"min_app = 2\n")

    monkeypatch.setattr(manifest_module, "__version__", "dev")  # a build with none
    assert parse_manifest(GOOD + b'min_app = "9.0.0"\n').min_app == "9.0.0"


def test_a_manifest_that_needs_a_newer_app_is_told_without_being_read_whole(
    monkeypatch,
) -> None:
    from kubescope.extensions import manifest as manifest_module
    from kubescope.extensions.manifest import needs_newer_app

    monkeypatch.setattr(manifest_module, "__version__", "2.3.1")

    assert needs_newer_app(b'min_app = "2.4.0"\n') == "2.4.0"
    assert needs_newer_app(b'min_app = "2.3.1"\n') == ""  # enough
    assert needs_newer_app(b"") == ""  # says nothing
    assert needs_newer_app(b"min_app = 4\n") == ""  # not a text
    assert needs_newer_app(b'min_app = "soon"\n') == ""
    assert needs_newer_app(b"\xff") == ""  # left to the install to refuse
    assert needs_newer_app(b"not = [toml") == ""


def test_an_extension_made_for_older_apps_is_refused_by_a_newer_one(
    monkeypatch,
) -> None:
    from kubescope.extensions import manifest as manifest_module
    from kubescope.extensions.manifest import needs_older_app

    limited = GOOD + b'max_app = "2.9.0"\n'
    monkeypatch.setattr(manifest_module, "__version__", "2.9.0")
    assert parse_manifest(limited).max_app == "2.9.0"  # the newest it works with
    assert needs_older_app(b'max_app = "2.9.0"\n') == ""
    monkeypatch.setattr(manifest_module, "__version__", "2.10.0")  # as numbers
    with pytest.raises(ManifestError, match="works up to KubeScope 2.9.0"):
        parse_manifest(limited)
    assert needs_older_app(b'max_app = "2.9.0"\n') == "2.9.0"
    assert needs_older_app(b"") == ""
    assert needs_older_app(b"max_app = 4\n") == ""
    assert needs_older_app(b'max_app = "soon"\n') == ""
    assert needs_older_app(b"\xff") == ""
    assert needs_older_app(b"not = [toml") == ""


def test_max_app_is_optional_and_must_be_a_version(monkeypatch) -> None:
    from kubescope.extensions import manifest as manifest_module

    assert parse_manifest(GOOD).max_app == ""
    with pytest.raises(ManifestError, match="max_app must look like 2.9.0"):
        parse_manifest(GOOD + b'max_app = "soon"\n')
    with pytest.raises(ManifestError, match="max_app must be a text"):
        parse_manifest(GOOD + b"max_app = 2\n")
    monkeypatch.setattr(manifest_module, "__version__", "dev")
    assert parse_manifest(GOOD + b'max_app = "1.0.0"\n').max_app == "1.0.0"
