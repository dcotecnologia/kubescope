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


def test_the_language_list_is_english_first_then_by_english_name() -> None:
    directory = i18n.languages_directory()
    _write(directory / "xx.json", _language("Mine"))  # a code Qt does not know
    i18n.reload_languages()
    try:
        choices = i18n.language_choices()
    finally:
        i18n.reload_languages()

    codes = [code for code, _ in choices]
    labels = dict(choices)
    assert codes[0] == "en" and labels["en"] == "English"
    assert labels["ko"] == "한국어 · Korean" and labels["xx"] == "Mine"
    named = [label.split(" · ")[-1] for code, label in choices[1:] if code != "xx"]
    assert named == sorted(named, key=str.casefold)


def test_a_system_locale_picks_the_language_of_its_territory(monkeypatch) -> None:
    from PySide6.QtCore import QLocale

    def system(name):
        class Locale(QLocale):
            @staticmethod
            def system():
                return QLocale(name)

        monkeypatch.setattr(i18n, "QLocale", Locale)

    for name, expected in (
        ("zh_TW", "zh_TW"),
        ("zh_HK", "zh_TW"),  # Hong Kong reads the traditional characters too
        ("zh_CN", "zh"),
        ("pt_BR", "pt"),
        ("xx_YY", "en"),
    ):
        system(name)
        assert i18n.resolve_language("auto") == expected


def test_traditional_chinese_is_listed_apart_from_simplified() -> None:
    labels = dict(i18n.language_choices())

    assert labels["zh_TW"] == "繁體中文 · Chinese (Taiwan)"
    assert labels["zh"].endswith("· Chinese")


def test_a_language_is_named_in_english_for_the_assistant() -> None:
    assert i18n.language_name("en") == "English"
    assert i18n.language_name("pt") == "Portuguese"
    assert i18n.language_name("zh_TW") == "Chinese (Taiwan)"
