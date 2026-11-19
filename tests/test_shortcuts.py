from kubescope.settings import Settings
from kubescope.utils.shortcuts import DEFAULTS, MAX_KEY, clean, duplicate


def test_missing_or_damaged_fall_back_to_defaults():
    assert clean(None) == DEFAULTS
    assert clean({"search": 3, "bogus": "X"}) == DEFAULTS


def test_defaults_do_not_share_a_key():
    assert duplicate(DEFAULTS) is None


def test_empty_turns_an_action_off():
    assert clean({"refresh": " "})["refresh"] == ""


def test_duplicate_ignores_empty_keys():
    assert duplicate({"a": "", "b": ""}) is None
    assert duplicate({"a": "F5", "b": "F5"}) == "F5"


def test_settings_keep_shortcuts(tmp_path):
    settings = Settings(tmp_path / "s.json")
    assert settings.shortcuts == DEFAULTS
    settings.shortcuts = {"search": "Ctrl+P"}
    assert settings.shortcuts["search"] == "Ctrl+P"
    assert settings.shortcuts["refresh"] == DEFAULTS["refresh"]


def test_the_shortcuts_of_extensions_are_kept_as_they_were_saved():
    kept = clean(
        {
            "refresh": "F2",
            "kubescope.gabi.ask": " Ctrl+G ",
            "Bad Id": "x",
            "kubescope.number": 5,
            "kubescope.long": "k" * (MAX_KEY + 1),
        }
    )

    assert kept["refresh"] == "F2"
    assert kept["kubescope.gabi.ask"] == "Ctrl+G"
    assert set(kept) == set(DEFAULTS) | {"kubescope.gabi.ask"}
