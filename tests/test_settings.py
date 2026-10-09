import json
import sys
from pathlib import Path

from kubescope.settings import Settings, config_directory, log_directory


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


def test_hidden_columns_persist_and_ignore_damaged_values(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.hidden_columns("pods") == set()
    settings.set_hidden_columns("pods", {7, 5})
    settings.save()

    assert Settings(path).hidden_columns("pods") == {5, 7}
    path.write_text('{"hidden_columns": {"pods": [1, "x"], "deployments": 3}}')
    assert Settings(path).hidden_columns("pods") == set()
    assert Settings(path).hidden_columns("deployments") == set()


def test_config_directory_follows_the_platform(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("KUBESCOPE_CONFIG_DIR", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("APPDATA", str(tmp_path / "roaming"))
    assert config_directory() == tmp_path / "roaming" / "kubescope"
    monkeypatch.delenv("APPDATA")
    assert config_directory() == tmp_path / "AppData" / "Roaming" / "kubescope"

    monkeypatch.setattr(sys, "platform", "darwin")
    assert (
        config_directory() == tmp_path / "Library" / "Application Support" / "kubescope"
    )

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    assert config_directory() == tmp_path / "xdg" / "kubescope"
    monkeypatch.delenv("XDG_CONFIG_HOME")
    assert config_directory() == tmp_path / ".config" / "kubescope"


def test_debug_logging_defaults_off_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.debug_logging is False

    settings.debug_logging = True
    settings.save()
    assert Settings(path).debug_logging is True

    path.write_text('{"debug_logging": "yes"}', encoding="utf-8")
    assert Settings(path).debug_logging is False  # only a real true turns it on


def test_log_directory_lives_in_the_config_directory(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path))

    assert log_directory() == tmp_path / "logs"


def test_theme_defaults_to_light_and_ignores_unknown_values(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.theme == "light"

    settings.theme = "dark"
    settings.save()
    assert Settings(path).theme == "dark"

    settings.theme = "neon"  # not a theme
    assert settings.theme == "light"

    path.write_text('{"theme": "sepia"}', encoding="utf-8")
    assert Settings(path).theme == "light"
