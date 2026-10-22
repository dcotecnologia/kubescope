import json
import sys
from pathlib import Path
from typing import cast

from kubescope.settings import (
    Settings,
    config_directory,
    is_namespace_name,
    log_directory,
)


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
    settings.language = "Klingon!"
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


def test_theme_defaults_to_dark_and_keeps_any_theme_id(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.theme == "dark"

    settings.theme = "midnight"  # a custom theme's id
    settings.save()
    assert Settings(path).theme == "midnight"

    for empty in ("", "  ", None):
        settings.theme = cast(str, empty)
        assert settings.theme == "dark"

    path.write_text('{"theme": 42}', encoding="utf-8")
    assert Settings(path).theme == "dark"


def test_default_namespace_is_validated_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.default_namespace == ""  # all namespaces

    settings.default_namespace = "kube-system"
    settings.save()
    assert Settings(path).default_namespace == "kube-system"

    settings.default_namespace = "Not Valid!"
    assert settings.default_namespace == ""

    path.write_text(json.dumps({"default_namespace": "-bad-"}), encoding="utf-8")
    assert Settings(path).default_namespace == ""
    path.write_text(json.dumps({"default_namespace": 7}), encoding="utf-8")
    assert Settings(path).default_namespace == ""


def test_namespace_names_follow_the_kubernetes_rule() -> None:
    assert is_namespace_name("a") and is_namespace_name("team-1")
    assert not is_namespace_name("") and not is_namespace_name("Team")
    assert not is_namespace_name("-x") and not is_namespace_name("x-")
    assert not is_namespace_name("a" * 64) and is_namespace_name("a" * 63)


def test_check_updates_defaults_on_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.check_updates is True

    settings.check_updates = False
    settings.save()
    assert Settings(path).check_updates is False

    path.write_text('{"check_updates": "no"}', encoding="utf-8")
    assert Settings(path).check_updates is True  # only a real false turns it off


def test_window_geometry_persists_and_ignores_damaged_values(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.window_geometry == ""

    settings.window_geometry = "AdnQywAD"
    settings.save()
    assert Settings(path).window_geometry == "AdnQywAD"

    path.write_text('{"window_geometry": 5}', encoding="utf-8")
    assert Settings(path).window_geometry == ""


def test_kubeconfig_files_and_sign_in_commands_persist_and_are_validated(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.kubeconfig_files == [] and settings.sign_in_commands == {}

    settings.kubeconfig_files = [" /a/config ", "", "/b/config"]
    settings.sign_in_commands = {
        " oci ": " oci session authenticate ",
        "x": " ",
        "": "y",
    }
    settings.save()
    reloaded = Settings(path)
    assert reloaded.kubeconfig_files == ["/a/config", "/b/config"]
    assert reloaded.sign_in_commands == {"oci": "oci session authenticate"}

    path.write_text(
        json.dumps(
            {
                "kubeconfig_files": ["/ok", 5, " "],
                "sign_in_commands": {"oci": "login", "bad": 3, "": "x", "empty": " "},
            }
        ),
        encoding="utf-8",
    )
    damaged = Settings(path)
    assert damaged.kubeconfig_files == ["/ok"]
    assert damaged.sign_in_commands == {"oci": "login"}

    path.write_text(
        '{"kubeconfig_files": "a", "sign_in_commands": []}', encoding="utf-8"
    )
    assert Settings(path).kubeconfig_files == []
    assert Settings(path).sign_in_commands == {}


def test_pinned_views_persist_without_duplicates_and_ignore_damaged_values(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.pinned_views() == []
    settings.set_pinned_views(["secrets", "pods", "secrets"])
    settings.save()

    assert Settings(path).pinned_views() == ["secrets", "pods"]
    path.write_text('{"pinned_views": ["pods", 3, "", "pods", "leases"]}')
    assert Settings(path).pinned_views() == ["pods", "leases"]
    path.write_text('{"pinned_views": "pods"}')
    assert Settings(path).pinned_views() == []


def test_last_screen_persists_and_ignores_damaged_values(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.last_screen == (0, "")

    settings.last_screen = (1, "pods")
    settings.save()
    assert Settings(path).last_screen == (1, "pods")

    path.write_text('{"last_screen": "pods"}')
    assert Settings(path).last_screen == (0, "")


def test_welcome_dismissed_defaults_off_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.welcome_dismissed is False

    settings.welcome_dismissed = True
    settings.save()
    assert Settings(path).welcome_dismissed is True

    path.write_text('{"welcome_dismissed": "yes"}', encoding="utf-8")
    assert Settings(path).welcome_dismissed is False  # only a real true counts


def test_write_mode_is_off_by_default_and_only_true_turns_it_on(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.write_mode is False

    settings.write_mode = True
    settings.save()
    assert Settings(path).write_mode is True

    for stored in ('"yes"', "1", "null"):
        path.write_text(f'{{"write_mode": {stored}}}', encoding="utf-8")
        assert Settings(path).write_mode is False


def test_wrapping_the_logs_is_off_by_default_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.wrap_log_lines is False

    settings.wrap_log_lines = True
    settings.save()
    assert Settings(path).wrap_log_lines is True

    path.write_text('{"wrap_log_lines": "yes"}', encoding="utf-8")
    assert Settings(path).wrap_log_lines is False  # only a real true turns it on
