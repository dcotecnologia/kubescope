from typing import cast

from PySide6.QtWidgets import QLabel

from tests.qt import present
from tests.test_window_flows import _ready_window


def test_the_settings_have_a_section_for_the_extensions(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    form = window.settings_ui
    content = form.settingsContent

    assert not form.extensionsCard.isVisibleTo(content)  # only in its own section

    form.extensionsSectionButton.click()

    assert form.extensionsCard.isVisibleTo(content)
    assert form.extensionsSectionButton.isChecked()
    assert not form.generalSectionButton.isChecked()
    assert not form.generalCard.isVisibleTo(content)


def test_without_extensions_the_section_says_so(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    window.settings_ui.extensionsSectionButton.click()

    grid = window.settings_ui.extensionsCardsGrid
    labels = [
        cast(QLabel, present(present(grid.itemAt(i)).widget()))
        for i in range(grid.count())
    ]
    assert [label.text() for label in labels] == ["No extension is installed"]
