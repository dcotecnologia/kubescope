import os

from PySide6.QtWidgets import QPushButton

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QColorDialog

from kubescope import theme
from kubescope.dialogs import theme_editor
from kubescope.dialogs.theme_editor import ThemeEditor, token_labels
from kubescope.theme import DARK_THEME, LIGHT_THEME, theme_tokens

application = QApplication.instance() or QApplication([])


def _editor(theme_in=LIGHT_THEME, *, new=True, name="My theme") -> ThemeEditor:
    return ThemeEditor(
        None, name=name, base=theme_in.base, tokens=theme_tokens(theme_in), new=new
    )


def _save_button(editor) -> QPushButton:
    return editor.save_button


def test_every_color_role_has_a_label_and_a_swatch() -> None:
    editor = _editor()

    assert set(token_labels()) == set(theme.TOKENS)
    assert set(editor._swatches) == set(theme.TOKENS)
    assert editor._swatches["page"].text() == "#dfe2e8"
    assert "background: #dfe2e8" in editor._swatches["page"].styleSheet()


def test_swatch_text_stays_readable_on_light_and_dark_colors() -> None:
    assert theme_editor._readable_on(QColor("#ffffff")) == "#000000"
    assert theme_editor._readable_on(QColor("#101010")) == "#ffffff"


def test_picking_a_color_updates_the_swatch_and_the_result(monkeypatch) -> None:
    editor = _editor()
    monkeypatch.setattr(
        QColorDialog, "getColor", staticmethod(lambda *_a: QColor("#112233"))
    )

    editor._swatches["page"].click()

    assert editor._swatches["page"].text() == "#112233"
    assert editor.values()[2]["page"] == "#112233"


def test_cancelling_the_color_dialog_keeps_the_color(monkeypatch) -> None:
    editor = _editor()
    monkeypatch.setattr(QColorDialog, "getColor", staticmethod(lambda *_a: QColor()))

    editor._swatches["page"].click()

    assert editor.values()[2]["page"] == "#dfe2e8"


def test_a_new_theme_can_restart_from_the_other_built_in_theme(monkeypatch) -> None:
    editor = _editor(new=True)
    monkeypatch.setattr(
        QColorDialog, "getColor", staticmethod(lambda *_a: QColor("#112233"))
    )
    editor._swatches["page"].click()
    assert editor.base_combo.isEnabled()

    editor.base_combo.setCurrentIndex(editor.base_combo.findData("dark"))

    name, base, tokens = editor.values()
    assert base == "dark" and tokens == theme_tokens(DARK_THEME)  # edits dropped
    assert editor._swatches["page"].text() == "#11141a"


def test_an_existing_theme_keeps_its_base_and_its_title_names_it() -> None:
    editor = _editor(DARK_THEME, new=False, name="Midnight")

    assert not editor.base_combo.isEnabled()
    assert editor.windowTitle() == "Edit theme: Midnight"
    assert editor.values()[:2] == ("Midnight", "dark")
    assert _editor(new=True).windowTitle() == "New theme"


def test_saving_needs_a_name_and_trims_it() -> None:
    editor = _editor(name="  Ocean  ")
    assert _save_button(editor).isEnabled() and editor.values()[0] == "Ocean"

    editor.name_edit.setText("   ")
    assert not _save_button(editor).isEnabled()

    editor.name_edit.setText("Reef")
    assert _save_button(editor).isEnabled()


def test_reset_undoes_the_color_changes_of_the_session(monkeypatch) -> None:
    editor = _editor(DARK_THEME, new=False, name="Midnight")
    monkeypatch.setattr(
        QColorDialog, "getColor", staticmethod(lambda *_a: QColor("#112233"))
    )
    assert not editor.reset_button.isEnabled()  # nothing to undo yet

    editor._swatches["page"].click()
    editor._swatches["text"].click()
    assert editor.reset_button.isEnabled()

    editor.reset_button.click()

    assert editor.values()[2] == theme_tokens(DARK_THEME)
    assert editor._swatches["page"].text() == "#11141a"
    assert not editor.reset_button.isEnabled()


def test_reset_goes_back_to_the_theme_a_new_one_restarted_from(monkeypatch) -> None:
    editor = _editor(LIGHT_THEME, new=True)
    editor.base_combo.setCurrentIndex(editor.base_combo.findData("dark"))
    monkeypatch.setattr(
        QColorDialog, "getColor", staticmethod(lambda *_a: QColor("#112233"))
    )
    editor._swatches["page"].click()

    editor.reset_button.click()

    assert editor.values()[2] == theme_tokens(DARK_THEME)


def test_the_inputs_and_buttons_use_the_projects_styles() -> None:
    editor = _editor()

    assert editor.name_edit.property("variant") == "filter"
    assert editor.base_combo.property("variant") == "filter"
    assert editor.reset_button.property("variant") == "secondary"
    assert editor.save_button.property("variant") == "primary"
    assert editor.save_button.isDefault()
