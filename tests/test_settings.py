import json

from kubescope.settings import Settings


def test_defaults_when_no_file_exists(tmp_path) -> None:
    settings = Settings(tmp_path / "settings.json")

    assert settings.language == "auto"
    assert settings.remember_last_context is True
    assert settings.last_context is None
    assert settings.context_aliases == {}


def test_save_and_reload_round_trip(tmp_path) -> None:
    path = tmp_path / "nested" / "settings.json"
    settings = Settings(path)
    settings.language = "pt"
    settings.remember_last_context = False
    settings.last_context = "prod-eks"
    settings.set_context_aliases({"prod-eks": " Prod ✓ ", "dev": "  "})
    settings.save()

    reloaded = Settings(path)

    assert reloaded.language == "pt"
    assert reloaded.remember_last_context is False
    assert reloaded.last_context == "prod-eks"
    assert reloaded.context_aliases == {"prod-eks": "Prod ✓"}
    assert reloaded.display_name("prod-eks") == "Prod ✓"
    assert reloaded.display_name("dev") == "dev"
    assert not path.with_suffix(".tmp").exists()


def test_damaged_or_foreign_files_fall_back_to_defaults(tmp_path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("{not json", encoding="utf-8")
    assert Settings(path).language == "auto"

    path.write_text(
        json.dumps({"language": "klingon", "context_aliases": ["x"], "other": 1}),
        encoding="utf-8",
    )
    settings = Settings(path)
    assert settings.language == "auto"
    assert settings.context_aliases == {}


def test_unknown_language_is_ignored_on_assignment(tmp_path) -> None:
    settings = Settings(tmp_path / "settings.json")
    settings.language = "xx"
    assert settings.language == "auto"
