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


def test_the_bundled_gabi_is_a_card_in_the_section(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    window.settings_ui.extensionsSectionButton.click()

    grid = window.settings_ui.extensionsCardsGrid
    [card] = [present(grid.itemAt(i)).widget() for i in range(grid.count())]
    title = present(card).findChild(QLabel, "extensionCardTitle")
    badge = present(card).findChild(QLabel, "extensionCardBadge")
    assert (
        present(title).text() == "Gabi - AI Assistant"
        and present(badge).text() == "Bundled"
    )
