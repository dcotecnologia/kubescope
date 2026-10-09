import json
import os
import re
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from kubescope import theme
from kubescope.theme import (
    SURFACE,
    ButtonCursor,
    active_theme,
    apply_theme,
    set_theme,
    themed,
    themed_stylesheet,
)

ROOT = Path(__file__).resolve().parents[1]
application = QApplication.instance() or QApplication([])


def test_light_theme_sets_a_light_palette_and_greys_disabled_text() -> None:
    apply_theme(application)

    palette = application.palette()
    assert application.style().objectName().lower() == "fusion"
    assert palette.color(QPalette.ColorRole.Window).lightness() > 200
    disabled = palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text)
    assert disabled.name() == "#8a919c"


def test_enabled_buttons_get_a_pointing_hand_and_disabled_ones_an_arrow() -> None:
    apply_theme(application)
    apply_theme(application)  # installing twice must not stack filters
    assert len(application.findChildren(ButtonCursor)) == 1

    button = QPushButton("Go")
    button.ensurePolished()
    assert button.cursor().shape() == Qt.CursorShape.PointingHandCursor

    button.setEnabled(False)
    assert button.cursor().shape() == Qt.CursorShape.ArrowCursor
    button.setEnabled(True)
    assert button.cursor().shape() == Qt.CursorShape.PointingHandCursor

    label = QLabel("text")
    label.ensurePolished()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor


def test_light_colors_pass_through_and_dark_ones_are_mapped() -> None:
    assert themed("#20232a") == "#20232a"
    assert (
        themed_stylesheet("QLabel { color: #20232a; }") == "QLabel { color: #20232a; }"
    )

    set_theme("dark")
    assert active_theme() == "dark"
    assert themed("#20232A") == "#e6e9ee"  # case does not matter
    assert themed("#e0a030") == "#e0a030"  # the same warning orange in both themes
    assert themed("#123456") == "#123456"  # unknown colors are left alone

    set_theme("neon")  # not a theme: back to the default
    assert active_theme() == "light"


def test_white_is_a_surface_in_dark_but_stays_white_as_text() -> None:
    set_theme("dark")

    assert themed("#ffffff") == SURFACE
    assert themed("#ffffff", text=True) == "#ffffff"

    recolored = themed_stylesheet(
        "QComboBox#contextCombo { background: #0d315d; color: #ffffff;"
        " border: 1px solid #2d5077; selection-color: #ffffff; }\n"
        'QFrame[card="true"] { background: #ffffff; border: 1px solid #dfe2e9; }\n'
        "QComboBox#c:disabled { color: #6b7380; }"
    )
    assert "color: #ffffff;" in recolored and "selection-color: #ffffff" in recolored
    assert f"background: {SURFACE}" in recolored
    assert "#13171d" in recolored and "#2b3036" in recolored  # navy becomes black
    assert "border: 1px solid #2d333d" in recolored
    assert "color: #7f8a99" in recolored


def test_the_dark_top_bar_is_black_not_navy() -> None:
    set_theme("dark")

    def lightness(color: str) -> int:
        return QColor(color).lightness()

    assert lightness(themed("#06234a")) < 15  # the bar itself
    assert lightness(themed("#0d315d")) < 30  # the context selector on it
    for navy in ("#06234a", "#123764", "#0d315d", "#2d5077", "#1f4f87"):
        color = QColor(themed(navy))
        assert abs(color.red() - color.blue()) < 16  # no blue tint left


def test_every_color_the_app_uses_has_a_dark_counterpart() -> None:
    sources = [
        ROOT / "src/kubescope/ui/main_window.ui",
        ROOT / "src/kubescope/window.py",
        ROOT / "src/kubescope/widgets.py",
    ]
    used = {
        color.lower()
        for source in sources
        for color in re.findall(
            r"#[0-9a-fA-F]{6}\b", source.read_text(encoding="utf-8")
        )
    }
    # white is handled by themed(); the warning orange is the same in both themes
    unmapped = used - set(theme._DARK) - {"#ffffff", "#e0a030"}

    assert unmapped == set(), f"add dark counterparts for {sorted(unmapped)}"


def test_applying_a_theme_switches_the_palette() -> None:
    apply_theme(application, "dark")
    assert application.palette().color(QPalette.ColorRole.Window).name() == "#11141a"
    disabled = application.palette().color(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text
    )
    assert disabled.name() == "#6b7380"

    apply_theme(application, "light")
    assert application.palette().color(QPalette.ColorRole.Window).name() == "#f7f7fa"


def test_a_theme_always_runs_on_the_fusion_style() -> None:
    application.setStyle("Windows")
    assert application.style().objectName().lower() != "fusion"

    apply_theme(application, "dark")

    assert application.style().objectName().lower() == "fusion"
    apply_theme(application, "light")
    assert application.style().objectName().lower() == "fusion"


@pytest.fixture
def themes_dir(tmp_path):
    folder = tmp_path / "config" / "themes"
    folder.mkdir(parents=True)
    return folder


def _write(folder, name: str, document) -> None:
    text = document if isinstance(document, str) else json.dumps(document)
    (folder / name).write_text(text, encoding="utf-8")


def test_a_custom_theme_starts_from_its_base_and_changes_only_what_it_lists() -> None:
    custom = theme.parse_theme(
        "ocean", {"name": "Ocean", "base": "dark", "colors": {"page": "#001122"}}
    )

    assert custom.base == "dark" and custom.name == "Ocean" and not custom.builtin
    assert custom.colors["#f7f7fa"] == "#001122"  # the role it changed
    assert custom.colors["#20232a"] == theme._DARK["#20232a"]  # inherited from dark

    light_based = theme.parse_theme("plain", {"name": "Plain"})
    assert light_based.base == "light" and light_based.colors == {}


def test_a_role_recolors_every_light_color_it_covers() -> None:
    custom = theme.parse_theme("x", {"name": "X", "colors": {"border": "#ABCDEF"}})

    assert {custom.colors[color] for color in theme.ROLES["border"]} == {"#abcdef"}


def test_on_accent_sets_the_color_of_text_that_is_white_in_the_light_theme() -> None:
    custom = theme.parse_theme("x", {"name": "X", "colors": {"on_accent": "#EEEEEE"}})
    set_theme("light")
    theme._active = custom

    assert themed("#ffffff", text=True) == "#eeeeee"
    assert themed("#ffffff") == "#ffffff"  # as a background it is untouched
    assert "color: #eeeeee" in themed_stylesheet("QLabel { color: #ffffff; }")
    assert "background: #ffffff" in themed_stylesheet("QLabel { background: #ffffff; }")


@pytest.mark.parametrize(
    "document",
    [
        [],
        {"base": "light"},
        {"name": 3},
        {"name": "X", "base": "neon"},
        {"name": "X", "colors": []},
        {"name": "X", "colors": {"nonsense": "#112233"}},
        {"name": "X", "colors": {"page": "red"}},
        {"name": "X", "colors": {"page": 12}},
    ],
)
def test_malformed_themes_are_rejected(document) -> None:
    with pytest.raises(ValueError):
        theme.parse_theme("x", document)


def test_custom_themes_are_loaded_from_the_themes_folder(themes_dir, caplog) -> None:
    _write(themes_dir, "ocean.json", {"name": "Ocean", "colors": {"page": "#001122"}})
    _write(themes_dir, "broken.json", "{not json")
    _write(themes_dir, "wrong.json", {"name": "Wrong", "base": "neon"})
    _write(themes_dir, "notes.txt", "ignored")
    _write(themes_dir, "dark.json", {"name": "Fake dark"})  # cannot replace a built-in

    with caplog.at_level("WARNING"):
        themes = theme.load_custom_themes()
        listed = theme.available_themes()

    assert set(themes) == {"ocean", "dark"}
    assert [t.id for t in listed] == ["light", "dark", "ocean"]
    assert "Skipping theme broken.json" in caplog.text
    assert "Skipping theme wrong.json" in caplog.text


def test_no_themes_folder_means_only_the_built_in_themes() -> None:
    assert theme.load_custom_themes() == {}
    assert [t.id for t in theme.available_themes()] == ["light", "dark"]


def test_a_custom_theme_can_be_made_active_and_a_missing_one_falls_back(
    themes_dir,
) -> None:
    _write(themes_dir, "ocean.json", {"name": "Ocean", "colors": {"page": "#001122"}})

    set_theme("ocean")
    assert active_theme() == "ocean" and themed("#f7f7fa") == "#001122"

    (themes_dir / "ocean.json").unlink()
    set_theme("ocean")  # the file is gone
    assert active_theme() == "light" and themed("#f7f7fa") == "#f7f7fa"

    set_theme("dark")
    assert active_theme() == "dark"


def test_theme_tokens_show_the_color_of_every_role() -> None:
    light = theme.theme_tokens(theme.LIGHT_THEME)
    dark = theme.theme_tokens(theme.DARK_THEME)

    assert set(light) == set(theme.TOKENS) == set(dark)
    assert light["page"] == "#f7f7fa" and dark["page"] == "#11141a"
    assert light["on_accent"] == dark["on_accent"] == "#ffffff"
    assert dark["bar_warning"] == "#e0a030"  # the same orange in both


def test_saving_a_theme_stores_only_what_differs_and_never_overwrites(
    themes_dir,
) -> None:
    tokens = theme.theme_tokens(theme.LIGHT_THEME)
    tokens["page"] = "#001122"

    saved = theme.save_custom_theme("Ocean Blue!", "light", tokens)

    assert saved.id == "ocean-blue" and saved.colors["#f7f7fa"] == "#001122"
    document = json.loads((themes_dir / "ocean-blue.json").read_text(encoding="utf-8"))
    assert document == {
        "name": "Ocean Blue!",
        "base": "light",
        "colors": {"page": "#001122"},
    }

    again = theme.save_custom_theme("Ocean Blue!", "light", tokens)
    assert again.id == "ocean-blue-2"  # a second theme with the same name
    assert (
        theme.save_custom_theme("Dark", "dark", theme.theme_tokens(theme.DARK_THEME)).id
        == "dark-2"
    )
    assert theme.save_custom_theme("???", "light", tokens).id == "theme"  # no letters

    tokens["page"] = "#334455"
    edited = theme.save_custom_theme(
        "Ocean Blue (edited)", "light", tokens, "ocean-blue"
    )
    assert edited.id == "ocean-blue" and edited.name == "Ocean Blue (edited)"
    assert theme.load_custom_themes()["ocean-blue"].colors["#f7f7fa"] == "#334455"


def test_applying_a_custom_theme_colors_the_palette(themes_dir) -> None:
    _write(themes_dir, "ocean.json", {"name": "Ocean", "colors": {"page": "#001122"}})

    apply_theme(application, "ocean")

    assert application.palette().color(QPalette.ColorRole.Window).name() == "#001122"
    apply_theme(application, "light")


@pytest.fixture
def community(tmp_path):
    folder = tmp_path / "community"
    folder.mkdir()
    return folder


def test_community_themes_are_copied_to_the_themes_folder(
    community, themes_dir
) -> None:
    _write(community, "ocean.json", {"name": "Ocean", "colors": {"page": "#001122"}})
    _write(community, "reef.json", {"name": "Reef", "base": "dark"})
    _write(community, "notes.txt", "ignored")

    added = theme.install_community_themes(community)

    assert added == ["ocean", "reef"]
    assert (themes_dir / "ocean.json").read_text(encoding="utf-8") == (
        community / "ocean.json"
    ).read_text(encoding="utf-8")
    assert not (themes_dir / "notes.txt").exists()
    assert [t.id for t in theme.available_themes()] == [
        "light",
        "dark",
        "ocean",
        "reef",
    ]
    assert theme.install_community_themes(community) == []  # nothing new the 2nd time


def test_installed_themes_are_not_overwritten_or_brought_back(
    community, themes_dir
) -> None:
    _write(community, "ocean.json", {"name": "Ocean", "colors": {"page": "#001122"}})
    theme.install_community_themes(community)

    _write(
        themes_dir, "ocean.json", {"name": "My ocean", "colors": {"page": "#999999"}}
    )
    _write(community, "ocean.json", {"name": "Ocean v2", "colors": {"page": "#000011"}})
    theme.install_community_themes(community)
    assert (
        json.loads((themes_dir / "ocean.json").read_text(encoding="utf-8"))["name"]
        == "My ocean"
    )

    (themes_dir / "ocean.json").unlink()  # the person deleted it
    assert theme.install_community_themes(community) == []
    assert not (themes_dir / "ocean.json").exists()


def test_a_file_of_the_same_name_is_the_persons_own(community, themes_dir) -> None:
    _write(themes_dir, "ocean.json", {"name": "Mine"})
    _write(community, "ocean.json", {"name": "Ocean"})

    assert theme.install_community_themes(community) == [
        "ocean"
    ]  # recorded, not copied

    assert (
        json.loads((themes_dir / "ocean.json").read_text(encoding="utf-8"))["name"]
        == "Mine"
    )


def test_unusable_community_themes_are_skipped(community, themes_dir, caplog) -> None:
    _write(community, "broken.json", "{not json")
    _write(community, "wrong.json", {"name": "Wrong", "base": "neon"})
    _write(community, "dark.json", {"name": "Fake dark"})
    _write(community, "fine.json", {"name": "Fine"})

    with caplog.at_level("WARNING"):
        added = theme.install_community_themes(community)

    assert added == ["fine"]
    assert "Skipping community theme broken.json" in caplog.text
    assert "Skipping community theme wrong.json" in caplog.text
    assert "hide a built-in theme" in caplog.text


def test_a_missing_community_folder_or_unwritable_config_is_harmless(
    community, tmp_path, monkeypatch, caplog
) -> None:
    assert theme.install_community_themes(tmp_path / "nothing") == []

    _write(community, "ocean.json", {"name": "Ocean"})
    blocker = tmp_path / "blocker"
    blocker.write_text("a file where a folder is needed")
    monkeypatch.setattr(theme, "themes_directory", lambda: blocker / "themes")
    with caplog.at_level("WARNING"):
        assert theme.install_community_themes(community) == []
    assert "Skipping community theme ocean.json" in caplog.text


def test_failing_to_record_the_installed_themes_only_warns(
    community, themes_dir, tmp_path, monkeypatch, caplog
) -> None:
    _write(community, "ocean.json", {"name": "Ocean"})
    monkeypatch.setattr(theme, "INSTALLED_FILE", "missing-folder/installed.json")

    with caplog.at_level("WARNING"):
        assert theme.install_community_themes(community) == ["ocean"]

    assert "Could not record the installed themes" in caplog.text


def test_a_damaged_record_of_installed_themes_is_ignored(
    community, themes_dir, tmp_path
) -> None:
    _write(community, "ocean.json", {"name": "Ocean"})
    record = tmp_path / "config" / theme.INSTALLED_FILE
    record.write_text('{"not": "a list"}', encoding="utf-8")
    assert theme.install_community_themes(community) == ["ocean"]

    record.write_text('["ocean", 3, null]', encoding="utf-8")
    (themes_dir / "ocean.json").unlink()
    assert theme.install_community_themes(community) == []  # still recorded


def test_every_community_theme_that_ships_is_valid() -> None:
    files = sorted(theme.COMMUNITY_DIRECTORY.glob("*.json"))

    assert {f.stem for f in files} >= {"midnight", "high-contrast", "sepia"}
    for path in files:
        assert path.stem == theme.slugify(path.stem), "use a lowercase-with-dashes name"
        assert path.stem not in theme.BUILTIN
        parsed = theme.parse_theme(
            path.stem, json.loads(path.read_text(encoding="utf-8"))
        )
        assert parsed.name


def test_community_themes_keep_their_text_readable() -> None:
    def contrast(a: str, b: str) -> float:
        def luminance(color: str) -> float:
            def channel(value: float) -> float:
                value /= 255
                return (
                    value / 12.92
                    if value <= 0.03928
                    else ((value + 0.055) / 1.055) ** 2.4
                )

            c = QColor(color)
            return (
                0.2126 * channel(c.red())
                + 0.7152 * channel(c.green())
                + 0.0722 * channel(c.blue())
            )

        high, low = sorted((luminance(a), luminance(b)), reverse=True)
        return (high + 0.05) / (low + 0.05)

    for path in theme.COMMUNITY_DIRECTORY.glob("*.json"):
        tokens = theme.theme_tokens(
            theme.parse_theme(path.stem, json.loads(path.read_text(encoding="utf-8")))
        )
        assert contrast(tokens["text"], tokens["page"]) >= 4.5, path.name
        assert contrast(tokens["text"], tokens["surface"]) >= 4.5, path.name
