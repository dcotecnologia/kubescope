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


def test_an_extension_shows_details_and_a_log_in_tabs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    ui = window.extension_host.ui
    assert ui is not None
    monkeypatch.setattr(
        window, "_run_action", lambda function, done, *a, **k: done(function(*a))
    )

    ui.show_json("RDS: orders", {"a": 1})
    ui.open_log("orders", "error.log", lambda: "line one\nline two")

    titles = [window.viewer_tabs.tabText(i) for i in range(window.viewer_tabs.count())]
    assert titles == ["RDS: orders", "Logs: orders / error.log"]
    assert window.pages.currentIndex() == 3


def test_a_forward_of_an_extension_goes_to_the_forwards_page(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    started = []
    monkeypatch.setattr(
        window.forward_runner, "start", lambda *args: started.append(args)
    )
    monkeypatch.setattr("kubescope.forwards.port_in_use", lambda port: False)

    assert window._begin_forward("RDS x", "ssm", ["aws"], {}, 15432, "db:5432")

    assert started == [("RDS x", "ssm", ["aws"], {}, 15432, "db:5432")]
    assert window.pages.currentIndex() == 5
