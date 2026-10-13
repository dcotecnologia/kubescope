import json

from PySide6.QtCore import QCoreApplication

from kubescope import i18n
from kubescope.settings import config_directory


def _language(name="Teste", **strings) -> dict:
    return {"name": name, "rtl": False, "strings": strings}


def _write(path, document) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document), encoding="utf-8")


def _digests() -> dict:
    return json.loads((config_directory() / i18n.INSTALLED_FILE).read_text())


def test_a_bundled_language_is_copied_once_and_kept_current(tmp_path) -> None:
    source = tmp_path / "bundled"
    _write(source / "xx.json", _language(A={"One": "Um"}))
    target = i18n.languages_directory() / "xx.json"

    assert i18n.install_bundled_languages(source) == ["xx"]
    assert json.loads(target.read_text())["strings"] == {"A": {"One": "Um"}}
    assert i18n.install_bundled_languages(source) == []  # nothing new

    _write(source / "xx.json", _language(A={"One": "Uno"}))  # the app got an update
    assert i18n.install_bundled_languages(source) == ["xx"]
    assert json.loads(target.read_text())["strings"] == {"A": {"One": "Uno"}}


def test_a_language_the_person_edited_or_deleted_is_left_alone(tmp_path) -> None:
    source = tmp_path / "bundled"
    _write(source / "xx.json", _language(A={"One": "Um"}))
    _write(source / "yy.json", _language(A={"One": "Um"}))
    i18n.install_bundled_languages(source)
    directory = i18n.languages_directory()
    _write(directory / "xx.json", _language(A={"One": "Mine"}))  # edited
    (directory / "yy.json").unlink()  # deleted
    _write(source / "xx.json", _language(A={"One": "Newer"}))
    _write(source / "yy.json", _language(A={"One": "Newer"}))

    assert i18n.install_bundled_languages(source) == []

    assert json.loads((directory / "xx.json").read_text())["strings"]["A"] == {
        "One": "Mine"
    }
    assert not (directory / "yy.json").exists()


def test_a_language_that_cannot_be_installed_is_reported(
    tmp_path, monkeypatch, caplog
) -> None:
    source = tmp_path / "bundled"
    _write(source / "xx.json", _language())
    monkeypatch.setattr(i18n.shutil, "copyfile", lambda *_a: _fail())

    assert i18n.install_bundled_languages(source) == []
    assert "Could not install the language xx" in caplog.text
    assert i18n.install_bundled_languages(tmp_path / "missing") == []


def _fail():
    raise OSError("read-only")


def test_the_record_failing_to_save_is_reported(tmp_path, monkeypatch, caplog) -> None:
    from pathlib import Path

    source = tmp_path / "bundled"
    _write(source / "xx.json", _language())
    original = Path.write_text

    def refuse(self, *args, **kwargs):
        if self.name == i18n.INSTALLED_FILE:
            raise OSError("full")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", refuse)

    assert i18n.install_bundled_languages(source) == ["xx"]
    assert "Could not record the installed languages" in caplog.text


def test_an_unreadable_record_is_no_record() -> None:
    config_directory().mkdir(parents=True, exist_ok=True)
    (config_directory() / i18n.INSTALLED_FILE).write_text("[1]")
    assert i18n._installed_digests() == {}
    (config_directory() / i18n.INSTALLED_FILE).write_text("nope")
    assert i18n._installed_digests() == {}


def test_a_file_in_the_languages_folder_adds_or_overrides_a_language(
    caplog,
) -> None:
    directory = i18n.languages_directory()
    _write(directory / "zz.json", _language("Zeta", Ctx={"Hello": "Olá"}))
    _write(directory / "pt.json", _language("Português meu"))
    _write(directory / "en.json", _language("Not English"))  # English is the source
    (directory / "bad.json").write_text("not json")
    _write(directory / "worse.json", {"name": "", "strings": {}})
    i18n.reload_languages()

    available = i18n.available_languages()

    assert list(available)[0] == "en" and available["en"] == "English"
    assert available["zz"] == "Zeta" and available["pt"] == "Português meu"
    assert "Skipping language bad.json" in caplog.text
    assert "Skipping language worse.json" in caplog.text
    assert i18n.resolve_language("zz") == "zz"
    try:
        assert i18n.apply_language("zz") == "zz"
        assert QCoreApplication.translate("Ctx", "Hello") == "Olá"
        assert QCoreApplication.translate("Ctx", "Other") == "Other"
    finally:
        i18n.apply_language("en")
        i18n.reload_languages()


def test_parse_language_checks_the_document() -> None:
    import pytest

    for bad in ([], {"strings": {}}, {"name": "x"}):
        with pytest.raises(ValueError):
            i18n.parse_language(bad)
    language = i18n.parse_language(
        {"name": " X ", "rtl": True, "strings": {"A": {"b": "c", "d": ""}, "E": 1}}
    )
    assert language == i18n.Language("X", True, {"A": {"b": "c"}})


def test_an_empty_translator_reports_it() -> None:
    assert i18n.JsonTranslator(i18n.Language("X", False, {})).isEmpty()
    assert not i18n.JsonTranslator(
        i18n.Language("X", False, {"A": {"b": "c"}})
    ).isEmpty()
