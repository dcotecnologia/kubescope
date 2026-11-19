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


def test_a_page_of_an_extension_is_in_the_menu_and_opens_with_its_title(
    monkeypatch,
) -> None:
    from PySide6.QtWidgets import QPushButton

    from kubescope.sdk import PageContribution

    window = _ready_window(monkeypatch)
    window.extension_host.contributions.pages.append(
        PageContribution(
            "dco.a",
            "Cloud",
            "Databases",
            "Instances",
            lambda: QLabel("the page"),
            "Of the account",
        )
    )

    window._apply_extension_contributions()
    entry = [
        one
        for one in window.ui.sidebarNav.findChildren(QPushButton)
        if one.text() == "Instances"
    ][-1]  # the one added last; the app has its own Instances until RDS leaves
    entry.click()

    assert window.ui.pageTitle.text() == "Instances"
    assert window.ui.pageSubtitle.text() == "Of the account"
    assert entry.isChecked() and not window.nav_overview.isChecked()

    window.nav_overview.click()

    assert not entry.isChecked()
