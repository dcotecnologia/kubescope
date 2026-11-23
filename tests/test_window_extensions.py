from PySide6.QtWidgets import QLabel, QPushButton

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

    panel = window.extensions_panel

    assert panel.empty_label.text() == "No extension is installed"
    assert not panel.empty_label.isHidden() and panel.table.isHidden()


def test_a_page_of_an_extension_is_in_the_menu_and_opens_with_its_title(
    monkeypatch,
) -> None:
    from kubescope.sdk import PageContribution
    from PySide6.QtWidgets import QPushButton

    window = _ready_window(monkeypatch)
    refreshed: list[int] = []
    window.extension_host.contributions.pages.append(
        PageContribution(
            "dco.a",
            "Cloud",
            "Databases",
            "Instances",
            lambda: QLabel("the page"),
            "Of the account",
            None,
            lambda: refreshed.append(1),
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
    assert window.extension_refresh_button.isVisibleTo(window)
    window.extension_refresh_button.click()
    assert refreshed == [1]

    window.nav_overview.click()

    assert not entry.isChecked()
    assert not window.extension_refresh_button.isVisibleTo(window)


def test_the_refresh_button_of_a_page_of_an_extension_spins_while_it_reads(
    monkeypatch,
) -> None:
    from kubescope.sdk import PageContribution
    from PySide6.QtWidgets import QApplication

    window = _ready_window(monkeypatch)
    spinning: list[object] = []

    def refresh() -> None:  # what an extension does: an action off the UI thread
        window._run_action(lambda: 1, lambda _result: None)
        spinning.append(window._spinner_button)

    window.extension_host.contributions.pages.append(
        PageContribution(
            "dco.a", "Cloud", "DB", "Spin", lambda: QLabel("page"), "", None, refresh
        )
    )
    window._apply_extension_contributions()
    entry = [
        b for b in window.ui.sidebarNav.findChildren(QPushButton) if b.text() == "Spin"
    ]
    entry[-1].click()

    window.extension_refresh_button.click()

    assert spinning == [window.extension_refresh_button]
    for worker in list(window._action_workers):
        worker.wait()
    QApplication.processEvents()
    assert window._spinner_button is None  # and it stops


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


def _order(window) -> list[str]:
    layout = window.ui.sidebarNavLayout
    items = (layout.itemAt(i).widget() for i in range(layout.count()))
    return [
        widget.text()
        for widget in items
        if isinstance(widget, QLabel) and widget.objectName() == "navSection"
    ]


def _two_sections(window) -> None:
    from kubescope.sdk import PageContribution

    for extension, section in (("dco.a", "AWS"), ("dco.b", "Secrets")):
        window.extension_host.contributions.pages.append(
            PageContribution(
                extension, section, "G", "T" + section, lambda: QLabel("page")
            )
        )
    window._apply_extension_contributions()


def test_a_block_of_the_side_menu_moves_up_and_down_and_the_order_is_kept(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    _two_sections(window)
    assert _order(window) == ["MONITORING", "AWS", "SECRETS"]

    window._move_section("section:secrets", -1)
    assert _order(window) == ["MONITORING", "SECRETS", "AWS"]
    assert window.settings.section_order == [
        "section:monitoring",
        "section:secrets",
        "section:aws",
    ]

    window._apply_extension_contributions()  # built again: the order stays
    assert _order(window) == ["MONITORING", "SECRETS", "AWS"]

    window._move_section("section:monitoring", 1)
    assert _order(window) == ["SECRETS", "MONITORING", "AWS"]
    window._move_section("section:aws", 1)  # the last one cannot go down
    window._move_section("section:nothing", -1)  # nor one that is not there
    assert _order(window) == ["SECRETS", "MONITORING", "AWS"]


def test_a_block_skips_the_ones_that_are_hidden_when_it_moves(monkeypatch) -> None:
    from kubescope.sdk import PageContribution

    window = _ready_window(monkeypatch)
    _two_sections(window)
    window.extension_host.contributions.pages.append(
        PageContribution(
            "dco.c", "Hidden", "G", "T", lambda: QLabel("page"), "", lambda: False
        )
    )
    window._apply_extension_contributions()
    assert window._visible_sections() == [
        "section:monitoring",
        "section:aws",
        "section:secrets",
    ]
    window._move_section("section:hidden", -1)  # it does not show: nothing moves
    window._move_section("section:secrets", -1)
    assert window._visible_sections()[1] == "section:secrets"


def test_the_title_of_a_block_has_a_reorganize_menu(monkeypatch) -> None:
    from PySide6.QtCore import QPoint

    window = _ready_window(monkeypatch)
    _two_sections(window)
    seen: list[list[tuple[str, bool]]] = []
    monkeypatch.setattr(
        window,
        "_open_section_menu",
        lambda menu, _at: seen.append(
            [
                (action.text(), action.isEnabled())
                for action in menu.actions()[0].menu().actions()  # type: ignore[union-attr]
            ]
        ),
    )
    labels = {
        "section:monitoring": window.ui.navSection,
        **{name: block.label for name, block in window.extension_pages.blocks.items()},
    }

    window._section_menu(
        "section:monitoring", labels["section:monitoring"], QPoint(1, 1)
    )
    window._section_menu("section:aws", labels["section:aws"], QPoint(1, 1))
    window._section_menu("section:secrets", labels["section:secrets"], QPoint(1, 1))
    window._section_menu("section:nothing", window.ui.navSection, QPoint(1, 1))

    assert seen == [
        [("Move up", False), ("Move down", True)],
        [("Move up", True), ("Move down", True)],
        [("Move up", True), ("Move down", False)],
    ]


def test_a_right_click_on_a_title_opens_its_menu(monkeypatch) -> None:
    from PySide6.QtCore import QPoint

    window = _ready_window(monkeypatch)
    _two_sections(window)
    opened: list[object] = []
    monkeypatch.setattr(
        window, "_open_section_menu", lambda menu, at: opened.append(at)
    )

    window.ui.navSection.customContextMenuRequested.emit(QPoint(2, 3))
    window.extension_pages.blocks["section:aws"].label.customContextMenuRequested.emit(
        QPoint(2, 3)
    )

    assert len(opened) == 2


def test_the_menu_of_a_block_is_opened_where_it_was_asked(monkeypatch) -> None:
    from typing import cast

    from PySide6.QtCore import QPoint
    from PySide6.QtWidgets import QMenu

    window = _ready_window(monkeypatch)
    seen: list[QPoint] = []

    class Menu:
        def exec(self, at):
            seen.append(at)

    window._open_section_menu(cast(QMenu, Menu()), QPoint(3, 4))

    assert seen == [QPoint(3, 4)]


def _gaps(window) -> list[bool]:
    """Whether there is air above each block, in the order they are in."""
    blocks = window._section_blocks()
    return [
        blocks[name].widgets[0].isVisibleTo(window.ui.sidebarNav)
        for name in window._section_order(blocks)
        if not blocks[name].label.isHidden()
    ]


def test_every_block_has_air_above_it_but_the_first_one(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    _two_sections(window)
    assert _gaps(window) == [False, True, True]

    window._move_section("section:monitoring", 1)  # the one of the app is not first
    assert _order(window) == ["AWS", "MONITORING", "SECRETS"]
    assert _gaps(window) == [False, True, True]

    window._move_section("section:aws", 1)
    window._move_section("section:aws", 1)
    assert _order(window) == ["MONITORING", "SECRETS", "AWS"]
    assert _gaps(window) == [False, True, True]


def test_a_block_that_does_not_show_has_no_air_and_does_not_count_as_the_first(
    monkeypatch,
) -> None:
    from kubescope.sdk import PageContribution

    window = _ready_window(monkeypatch)
    shown = [False]
    window.extension_host.contributions.pages.append(
        PageContribution(
            "dco.c", "Hidden", "G", "T", lambda: QLabel("page"), "", lambda: shown[0]
        )
    )
    window._apply_extension_contributions()
    window._move_section("section:monitoring", 1)  # nothing else shows: no move
    assert _gaps(window) == [False]

    shown[0] = True
    window.extension_pages.sync()
    assert _gaps(window) == [False, True]
    assert (
        window.extension_pages.blocks["section:hidden"]
        .widgets[0]
        .isVisibleTo(window.ui.sidebarNav)
    )
