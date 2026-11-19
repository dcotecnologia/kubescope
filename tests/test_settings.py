import json
from typing import Any, cast

import pytest

from kubescope.settings import (
    Settings,
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


def test_the_system_title_bar_is_off_by_default_and_persists(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.system_title_bar is False

    settings.system_title_bar = True
    settings.save()
    assert Settings(path).system_title_bar is True

    path.write_text('{"system_title_bar": "yes"}', encoding="utf-8")
    assert Settings(path).system_title_bar is False  # only a real true turns it on


def test_the_windows_animate_unless_the_person_turned_it_off(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.animations is True

    settings.animations = False
    settings.save()
    assert Settings(path).animations is False

    path.write_text('{"animations": 0}', encoding="utf-8")
    assert Settings(path).animations is True  # only a real false counts


def test_a_recent_up_to_date_is_remembered_for_the_version_that_found_it(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert not settings.update_check_is_fresh("1.2.0", 1000.0, 3600)  # never checked

    settings.record_update_check("1.2.0", 1000.0)
    settings.save()
    again = Settings(path)

    assert again.update_check_is_fresh("1.2.0", 1000.0 + 3599, 3600)
    assert not again.update_check_is_fresh("1.2.0", 1000.0 + 3600, 3600)  # stale
    assert not again.update_check_is_fresh("1.3.0", 1100.0, 3600)  # another version
    assert not again.update_check_is_fresh("1.2.0", 900.0, 3600)  # the clock went back

    path.write_text('{"update_checked_at": "soon", "update_checked_for": "1.2.0"}')
    assert not Settings(path).update_check_is_fresh("1.2.0", 1000.0, 3600)
    path.write_text('{"update_checked_at": true, "update_checked_for": "1.2.0"}')
    assert not Settings(path).update_check_is_fresh("1.2.0", 0.5, 3600)


def test_the_width_the_person_gave_the_side_menu_is_kept_when_it_makes_sense(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.sidebar_width == 0  # none given: the usual width

    settings.sidebar_width = 410
    settings.save()
    assert Settings(path).sidebar_width == 410

    for stored in ("12", "99999", '"wide"', "true", "null"):
        path.write_text(f'{{"sidebar_width": {stored}}}', encoding="utf-8")
        assert Settings(path).sidebar_width == 0


def test_the_sections_of_the_menu_the_person_closed_are_kept(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.menu_collapsed == []  # all open

    settings.menu_collapsed = ["config", "workloads"]
    settings.save()
    assert Settings(path).menu_collapsed == ["config", "workloads"]

    path.write_text(
        '{"menu_collapsed": ["network", "other", 3, "network"]}', encoding="utf-8"
    )
    assert Settings(path).menu_collapsed == ["network"]
    path.write_text('{"menu_collapsed": "config"}', encoding="utf-8")
    assert Settings(path).menu_collapsed == []


def test_a_context_without_an_alias_shows_the_end_of_its_name(tmp_path) -> None:
    settings = Settings(tmp_path / "settings.json")
    arn = "arn:aws:eks:us-east-1:123456789012:cluster/shop-eks-hml-us-east-1"

    assert settings.display_name(arn) == "shop-eks-hml-us-east-1"
    assert settings.display_name("arn:aws:eks:us-east-1:123:eks-arm64") == "eks-arm64"
    assert settings.display_name("gke_proj_zone_cluster") == "gke_proj_zone_cluster"
    assert settings.display_name("minikube") == "minikube"
    assert settings.display_name("ends/") == "ends/"  # nothing after it: all of it

    settings.set_context_aliases({arn: "Hml"})
    assert settings.display_name(arn) == "Hml"


def test_the_cloud_accounts_are_saved_without_what_cannot_be_read(tmp_path) -> None:
    good = {"id": "aws-1", "provider": "aws", "name": "work", "fields": {"a": "b"}}
    settings = Settings(tmp_path / "s.json")
    assert settings.integration_accounts == []

    saved: list[Any] = [
        good,
        "not a dict",
        {"id": "aws-1", "provider": "aws", "name": "again", "fields": {}},  # same id
        {"id": "x", "provider": "aws", "name": "", "fields": {}},  # no name
        {"id": 3, "provider": "aws", "name": "n", "fields": {}},  # not text
        {"id": "gcp-1", "provider": "gcp", "name": "g", "fields": ["not", "a dict"]},
        {"id": "az-1", "provider": "azure", "name": "z", "fields": {"k": 1, "t": "v"}},
    ]
    settings.integration_accounts = saved

    assert [account["id"] for account in settings.integration_accounts] == [
        "aws-1",
        "gcp-1",
        "az-1",
    ]
    assert settings.integration_accounts[0] == good
    assert settings.integration_accounts[1]["fields"] == {}
    assert settings.integration_accounts[2]["fields"] == {"t": "v"}

    settings.save()
    assert Settings(tmp_path / "s.json").integration_accounts[0] == good
    damaged: Any = "damaged"
    settings.integration_accounts = damaged
    assert settings.integration_accounts == []


def test_settings_default_and_validation(tmp_path):
    settings = Settings(tmp_path / "s.json")
    assert settings.timezone == "auto"
    settings.timezone = "Europe/Lisbon"
    assert settings.timezone == "Europe/Lisbon"
    settings.timezone = "bogus"
    assert settings.timezone == "auto"


def test_each_extension_has_preferences_of_its_own_that_are_saved(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.extension_data("dco.a") == {}

    settings.extension_data("dco.a")["model"] = "opus"
    settings.extension_data("dco.b")["panel"] = {"width": 400}
    settings.save()
    reloaded = Settings(path)

    assert reloaded.extension_data("dco.a") == {"model": "opus"}
    assert reloaded.extension_data("dco.b") == {"panel": {"width": 400}}
    assert reloaded.extension_data("dco.c") == {}  # no other extension's


def test_the_data_of_an_extension_is_the_live_dictionary(tmp_path) -> None:
    settings = Settings(tmp_path / "settings.json")

    assert settings.extension_data("dco.a") is settings.extension_data("dco.a")


def test_what_is_not_the_id_of_an_extension_is_refused(tmp_path) -> None:
    settings = Settings(tmp_path / "settings.json")

    for bad in ("", "Dco.A", "a/b", "x" * 101):
        with pytest.raises(ValueError, match="not the id of an extension"):
            settings.extension_data(bad)


def test_damaged_preferences_of_extensions_are_dropped_on_load(tmp_path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        '{"extensions": {"dco.ok": {"a": 1}, "Bad Id": {"a": 1}, "dco.list": [1], '
        '"dco.text": "x"}}',
        encoding="utf-8",
    )

    settings = Settings(path)

    assert settings.extension_data("dco.ok") == {"a": 1}
    assert settings.extension_data("dco.list") == {}
    assert settings.extension_data("dco.text") == {}
    path.write_text('{"extensions": [1]}', encoding="utf-8")
    assert Settings(path).extension_data("dco.ok") == {}


def write(path, document: dict) -> None:
    path.write_text(json.dumps(document), encoding="utf-8")


def test_what_the_app_kept_for_the_assistant_moves_to_her_extension(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(
        path,
        {
            "assistant_enabled": False,
            "assistant_panel": {"width": 400},
            "assistant_programs": {"claude": "/x/claude"},
            "assistant_models": {"claude": "opus"},
            "assistant_efforts": {"codex": "high"},
            "assistant": "claude",
            "assistant_consent": True,
            "language": "pt_BR",
        },
    )

    settings = Settings(path)

    assert settings.extension_data("kubescope.gabi") == {
        "enabled": False,
        "panel": {"width": 400},
        "programs": {"claude": "/x/claude"},
        "models": {"claude": "opus"},
        "efforts": {"codex": "high"},
        "assistant": "claude",
        "consent": True,
    }
    settings.save()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert not [key for key in saved if key.startswith("assistant")]
    assert saved["language"] == "pt_BR"
    assert saved["extensions"]["kubescope.gabi"]["consent"] is True


def test_what_she_already_has_is_not_replaced_by_the_old_keys(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(
        path,
        {
            "assistant_consent": False,
            "assistant": "old",
            "extensions": {"kubescope.gabi": {"consent": True}, "dco.other": {"a": 1}},
        },
    )

    settings = Settings(path)

    assert settings.extension_data("kubescope.gabi") == {
        "consent": True,
        "assistant": "old",
    }
    assert settings.extension_data("dco.other") == {"a": 1}


def test_the_key_of_the_shortcut_of_the_assistant_moves_to_her_action(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(path, {"shortcuts": {"assistant": "Ctrl+H", "refresh": "F2"}})

    settings = Settings(path)

    assert settings.shortcuts["kubescope.gabi.ask"] == "Ctrl+H"
    assert (
        "assistant" not in settings.shortcuts and settings.shortcuts["refresh"] == "F2"
    )


def test_a_shortcut_she_already_has_wins_over_the_old_one(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(
        path,
        {"shortcuts": {"assistant": "Ctrl+H", "kubescope.gabi.ask": "Ctrl+J"}},
    )

    assert Settings(path).shortcuts["kubescope.gabi.ask"] == "Ctrl+J"


def test_without_old_keys_nothing_is_made_for_her(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(path, {"language": "de"})
    settings = Settings(path)
    settings.save()

    assert "extensions" not in json.loads(path.read_text(encoding="utf-8")) or (
        "kubescope.gabi"
        not in json.loads(path.read_text(encoding="utf-8"))["extensions"]
    )
    assert "assistant" not in settings.shortcuts


@pytest.mark.parametrize(
    "document",
    [
        {"assistant_consent": True, "extensions": [1]},
        {"assistant_consent": True, "extensions": {"kubescope.gabi": "x"}},
        {"shortcuts": ["assistant"]},
    ],
)
def test_a_damaged_file_still_gets_what_can_be_moved(tmp_path, document) -> None:
    path = tmp_path / "settings.json"
    write(path, document)

    settings = Settings(path)

    expected = {"consent": True} if "assistant_consent" in document else {}
    assert settings.extension_data("kubescope.gabi") == expected


def test_the_app_remembers_which_extensions_it_already_offered(tmp_path) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.extensions_offered == []

    settings.offered("kubescope.gabi")
    settings.offered("kubescope.gabi")  # once
    settings.offered("dco.other")
    settings.save()

    assert Settings(path).extensions_offered == ["kubescope.gabi", "dco.other"]


@pytest.mark.parametrize(
    "stored", [{"extensions_offered": "gabi"}, {"extensions_offered": 3}]
)
def test_a_damaged_list_of_offers_is_empty(tmp_path, stored) -> None:
    path = tmp_path / "settings.json"
    write(path, stored)

    assert Settings(path).extensions_offered == []


def test_only_ids_are_kept_in_the_list_of_offers(tmp_path) -> None:
    path = tmp_path / "settings.json"
    write(
        path,
        {"extensions_offered": ["kubescope.gabi", 3, "Bad Id", "kubescope.gabi", None]},
    )

    assert Settings(path).extensions_offered == ["kubescope.gabi"]


def test_the_time_the_extensions_were_last_looked_at_is_kept_and_read_safely() -> None:
    settings = Settings()

    assert settings.extension_updates_checked_at == 0.0
    settings.record_extension_updates_check(1_700_000_000)
    assert settings.extension_updates_checked_at == 1_700_000_000.0
    settings._data["extension_updates_checked_at"] = "yesterday"
    assert settings.extension_updates_checked_at == 0.0
    settings._data["extension_updates_checked_at"] = -5
    assert settings.extension_updates_checked_at == 0.0
