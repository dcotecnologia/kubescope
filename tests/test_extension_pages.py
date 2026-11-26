import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kubescope.sdk import PageContribution
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from kubescope.extensions.registries import Contributions
from kubescope.views.extension_pages import ExtensionPages

application = QApplication.instance() or QApplication([])


class Page(QLabel):
    opened = 0

    def shown(self) -> None:
        Page.opened += 1


def make():
    window = QWidget()
    menu = QVBoxLayout(window)
    menu.addItem(QSpacerItem(0, 0))  # the spacer that ends the menu
    stack = QStackedWidget(window)
    stack.addWidget(QWidget())  # the page the window starts on
    events: list[object] = []
    pages = ExtensionPages(
        menu, stack, stack.setCurrentIndex, lambda: events.append("left")
    )
    window.show()
    return window, menu, stack, pages, events


def page(title="Instances", visible=None, extension="dco.a", factory=None):
    return PageContribution(
        extension,
        "AWS",
        "RDS",
        title,
        factory or (lambda: Page(title)),
        "Subtitle",
        visible,
    )


def labels(window):
    found = [*window.findChildren(QLabel), *window.findChildren(QPushButton)]
    shown = [one for one in found if one.isVisibleTo(window) and one.text()]
    shown.sort(key=lambda one: one.mapTo(window, one.rect().topLeft()).y())
    return [one.text() for one in shown]


def test_the_section_the_group_and_the_entry_are_in_the_menu() -> None:
    window, _menu, _stack, pages, _events = make()

    pages.apply([page()])

    assert labels(window) == ["AWS", "RDS", "Instances"]


def test_two_entries_of_a_group_share_its_section_and_group() -> None:
    window, _menu, _stack, pages, _events = make()

    pages.apply([page("Instances"), page("Snapshots")])

    assert labels(window) == ["AWS", "RDS", "Instances", "Snapshots"]


def test_the_page_is_built_when_it_is_first_opened_and_told_each_time() -> None:
    window, _menu, stack, pages, _events = make()
    built: list[str] = []
    pages.apply([page(factory=lambda: built.append("x") or Page("x"))])
    Page.opened = 0
    index = stack.count() - 1

    assert built == []
    assert pages.shown(index) == ("RDS: Instances", "Subtitle", None)
    pages.shown(index)

    assert built == ["x"]  # built once
    assert Page.opened == 2


def test_an_entry_that_says_it_is_not_visible_is_hidden_with_its_section() -> None:
    window, _menu, _stack, pages, _events = make()
    using = [False]
    pages.apply([page(visible=lambda: using[0])])

    assert labels(window) == []
    using[0] = True
    pages.sync()
    assert labels(window) == ["AWS", "RDS", "Instances"]


def test_an_entry_that_fails_to_say_is_hidden() -> None:
    window, _menu, _stack, pages, _events = make()

    def broken() -> bool:
        raise RuntimeError

    pages.apply([page(visible=broken)])

    assert labels(window) == []


def test_a_page_that_cannot_be_built_says_so() -> None:
    window, _menu, stack, pages, _events = make()

    def broken() -> QWidget:
        raise RuntimeError

    pages.apply([page(factory=broken)])
    pages.shown(stack.count() - 1)

    assert "This page could not be built." in labels(stack.widget(stack.count() - 1))  # type: ignore[arg-type]


def test_the_entries_leave_with_the_page_that_was_open() -> None:
    window, _menu, stack, pages, events = make()
    pages.apply([page()])
    stack.setCurrentIndex(stack.count() - 1)

    pages.apply([])

    assert events == ["left"]
    assert stack.count() == 1
    assert labels(window) == []


def test_clicking_the_entry_opens_its_page() -> None:
    window, _menu, stack, pages, _events = make()
    pages.apply([page()])
    entry = next(
        one for one in window.findChildren(QPushButton) if one.text() == "Instances"
    )

    entry.click()

    assert stack.currentIndex() == stack.count() - 1


def test_a_page_added_by_an_extension_is_removed_with_it() -> None:
    contributions = Contributions()
    contributions.pages.append(page(extension="dco.a"))
    contributions.pages.append(page(extension="dco.b"))

    contributions.remove_extension("dco.a")

    assert [one.extension for one in contributions.pages] == ["dco.b"]


def test_a_page_whose_entry_goes_away_while_it_is_open_is_left() -> None:
    window, _menu, stack, pages, events = make()
    using = [True]
    pages.apply([page(visible=lambda: using[0])])
    stack.setCurrentIndex(stack.count() - 1)

    using[0] = False
    pages.sync()

    assert events == ["left"]


def test_a_page_that_fails_when_it_is_opened_does_not_stop_the_window(caplog) -> None:
    class Broken(QLabel):
        def shown(self) -> None:
            raise RuntimeError("boom")

    window, _menu, stack, pages, _events = make()
    pages.apply([page(factory=lambda: Broken("x"))])

    found = pages.shown(stack.count() - 1)

    assert found == ("RDS: Instances", "Subtitle", None)
    assert "The page Instances failed" in caplog.text


def test_each_section_has_a_title_that_folds_its_entries_and_remembers() -> None:
    window = QWidget()
    menu = QVBoxLayout(window)
    menu.addItem(QSpacerItem(0, 0))
    stack = QStackedWidget(window)
    stack.addWidget(QWidget())
    kept: list[tuple[str, bool]] = []
    pages = ExtensionPages(
        menu,
        stack,
        stack.setCurrentIndex,
        lambda: None,
        lambda name: name == "section:aws",  # it was folded last time
        lambda: False,
        lambda name, folded: kept.append((name, folded)),
    )
    window.show()
    pages.apply([page("Instances")])

    (fold,) = pages.folds.values()
    assert fold.folded and "Instances" not in labels(window)

    fold.toggle()
    assert "Instances" in labels(window) and kept == [("section:aws", False)]
    assert isinstance(fold.title, QLabel) and fold.title.text() == "AWS"

    pages.apply([page("Instances")])  # built again: the folds are too
    (again,) = pages.folds.values()
    assert again is not fold and again.folded


def test_a_section_without_a_visible_entry_has_no_title_and_no_block() -> None:
    window, _menu, _stack, pages, _events = make()
    pages.apply([page("Instances", visible=lambda: False)])

    (fold,) = pages.folds.values()

    assert fold.title.isHidden() and fold.body.isHidden()


def test_a_group_looks_as_the_ones_of_the_app_with_an_icon_and_an_arrow() -> None:
    from PySide6.QtGui import QIcon, QPixmap

    window = QWidget()
    menu = QVBoxLayout(window)
    menu.addItem(QSpacerItem(0, 0))
    stack = QStackedWidget(window)
    stack.addWidget(QWidget())
    icon = QIcon(QPixmap(16, 16))
    kept: list[tuple[str, bool]] = []
    pages = ExtensionPages(
        menu,
        stack,
        stack.setCurrentIndex,
        lambda: None,
        lambda name: False,
        lambda: False,
        lambda name, folded: kept.append((name, folded)),
        lambda _group: icon,
    )
    window.show()
    pages.apply([page("Instances"), page("Snapshots")])

    (header,) = [b for b in window.findChildren(QPushButton) if b.text() == "RDS"]
    assert not header.icon().isNull() and header.minimumHeight() == 24
    assert header.findChildren(QLabel)  # the arrow of the entries that fold
    submenu = next(e.button.parentWidget() for e in pages._entries)
    assert submenu is not None and submenu.property("submenu") == "true"
    assert "Instances" in labels(window)

    header.click()  # the whole group goes, the entries with it
    assert "Instances" not in labels(window) and "RDS" in labels(window)
    assert kept == [("section:aws/rds", True)]
    header.click()
    assert "Instances" in labels(window) and "Snapshots" in labels(window)

    pages.restyle()  # the theme changed: the icon is asked again
    assert not header.icon().isNull()


def test_a_group_folded_last_time_starts_folded_and_waits_for_its_entries() -> None:
    window = QWidget()
    menu = QVBoxLayout(window)
    menu.addItem(QSpacerItem(0, 0))
    stack = QStackedWidget(window)
    stack.addWidget(QWidget())
    pages = ExtensionPages(
        menu,
        stack,
        stack.setCurrentIndex,
        lambda: None,
        lambda name: name == "section:aws/rds",
        lambda: False,
    )
    window.show()

    pages.apply([page("Instances", visible=lambda: False)])
    assert "RDS" not in labels(window)  # no entry shows: no group either

    pages.apply([page("Instances")])
    assert "RDS" in labels(window) and "Instances" not in labels(window)


def test_the_blocks_are_named_and_the_window_is_told_when_they_are_built() -> None:
    window, _menu, _stack, pages, _events = make()
    built: list[list[str]] = []
    pages._on_changed = lambda: built.append(list(pages.blocks))

    pages.apply([page(), PageContribution("dco.b", "Secrets", "ES", "L", object)])

    assert built == [["section:aws", "section:secrets"]]  # told once, by the sync
    block = pages.blocks["section:aws"]
    assert block.label.text() == "AWS"
    assert [type(widget).__name__ for widget in block.widgets] == [
        "QWidget",
        "QLabel",
        "QFrame",
    ]  # the air, the title and the body
    pages.apply([])
    assert pages.blocks == {}


def test_each_group_asks_for_its_own_icon_by_name_and_again_on_a_new_theme() -> None:
    from PySide6.QtGui import QIcon, QPixmap

    window, menu, stack, _pages, _events = make()
    asked: list[str] = []

    def icon_of(group: str) -> QIcon:
        asked.append(group)
        return QIcon(QPixmap(16, 16))

    pages = ExtensionPages(
        menu, stack, stack.setCurrentIndex, lambda: None, group_icon=icon_of
    )
    other = PageContribution("dco.b", "AWS", "EKS", "Clusters", object)

    pages.apply([page(), other])
    pages.restyle()

    assert asked == ["RDS", "EKS", "RDS", "EKS"]
    window.close()


def test_a_page_for_a_section_of_the_app_goes_into_it() -> None:
    window = QWidget()
    menu = QVBoxLayout(window)
    menu.addItem(QSpacerItem(0, 0))
    own = QWidget()
    own_body = QVBoxLayout(own)  # the body of the Monitoring section of the app
    own_body.addWidget(QLabel("Workloads"))
    menu.insertWidget(0, own)
    stack = QStackedWidget(window)
    stack.addWidget(QWidget())
    pages = ExtensionPages(
        menu,
        stack,
        stack.setCurrentIndex,
        lambda: None,
        builtin={"monitoring": own_body},
    )
    window.show()
    mine = PageContribution(
        "dco.plugins", "Monitoring", "Plugins", "Installed", lambda: Page("x")
    )

    pages.apply([mine])

    assert labels(window) == [
        "Workloads",
        "Plugins",
        "Installed",
    ]  # no section of its own
    assert not pages.blocks and not pages.folds

    pages.apply([])

    assert labels(window) == ["Workloads"]


def test_a_page_can_be_found_and_opened_by_its_pin_key():
    from kubescope.views.extension_pages import pin_key

    _window, _menu, stack, pages, _events = make()
    seen: list[str] = []
    pages._on_entry = lambda key, _button: seen.append(key)
    one = page()
    pages.apply([one])
    key = pin_key(one)
    assert seen == [key]
    assert key == "extension:dco.a/AWS/RDS/Instances"
    assert pages.button_for("extension:none") is None
    assert not pages.is_open(key)
    pages.open_key(key)
    pages.open_key("extension:none")
    assert pages.is_open(key)
    assert pages.button_for(key) is not None
