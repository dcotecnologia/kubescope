import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

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
from kubescope.sdk import PageContribution
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
    assert pages.shown(index) == ("Instances", "Subtitle")
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
