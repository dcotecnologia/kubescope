import json

from PySide6.QtCore import QCoreApplication

from kubescope import i18n


def _language(name="Teste", **strings) -> dict:
    return {"name": name, "rtl": False, "strings": strings}


def _write(path, document) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document), encoding="utf-8")


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
