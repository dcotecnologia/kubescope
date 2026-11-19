"""The pages that extensions add to the side menu.

Each page has an entry in a menu group of a section (like "RDS" in
"AWS") and a widget the extension builds the first time the page is
opened. The entries leave with the extension that added them.
"""

import logging
from collections.abc import Callable, Sequence
from functools import partial

from PySide6.QtCore import QObject
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from kubescope.sdk import PageContribution

logger = logging.getLogger(__name__)


class _Entry:
    def __init__(
        self,
        page: PageContribution,
        button: QPushButton,
        host: QWidget,
        group: QWidget,
        section: QLabel,
    ) -> None:
        self.page = page
        self.button = button
        self.host = host  # the widget in the stack, which holds the page's own
        self.group = group
        self.section = section
        self.built = False


class ExtensionPages(QObject):
    def __init__(
        self,
        menu: QVBoxLayout,
        stack: QStackedWidget,
        open_page: Callable[[int], None],
        leave: Callable[[], None],
    ) -> None:
        super().__init__(stack)
        self.menu = menu  # its last item is the spacer that ends it
        self.stack = stack
        self.open_page = open_page  # show the page of this index
        self.leave = leave  # the page shown went away
        self._entries: list[_Entry] = []
        self._widgets: list[QWidget] = []  # what was added to the menu

    def apply(self, pages: Sequence[PageContribution]) -> None:
        """Build the entries of the pages that the running extensions added."""
        showing = self.stack.currentWidget()
        for entry in self._entries:
            self.stack.removeWidget(entry.host)
            entry.host.deleteLater()
        for widget in self._widgets:
            self.menu.removeWidget(widget)
            widget.hide()  # until it is deleted
            widget.deleteLater()
        self._entries, self._widgets = [], []
        sections: dict[str, QLabel] = {}
        groups: dict[tuple[str, str], tuple[QPushButton, QFrame]] = {}
        for page in pages:
            if page.section not in sections:
                label = QLabel(page.section.upper())
                label.setObjectName("navSection")
                self._add(label)
                sections[page.section] = label
            if (page.section, page.group) not in groups:
                header = QPushButton(page.group)
                header.setProperty("nav", "true")
                submenu = QFrame()
                submenu.setProperty("submenu", "true")
                layout = QVBoxLayout(submenu)
                layout.setContentsMargins(4, 0, 0, 0)
                layout.setSpacing(0)
                header.clicked.connect(
                    lambda _checked=False, box=submenu: box.setVisible(
                        not box.isVisible()
                    )
                )
                self._add(header)
                self._add(submenu)
                groups[(page.section, page.group)] = (header, submenu)
            header, submenu = groups[(page.section, page.group)]
            button = QPushButton(page.title)
            button.setProperty("nav", "true")
            button.setCheckable(True)
            button.setAutoExclusive(False)
            submenu.layout().addWidget(button)  # type: ignore[union-attr]
            host = QWidget()
            QVBoxLayout(host).setContentsMargins(0, 0, 0, 0)
            self.stack.addWidget(host)
            entry = _Entry(page, button, host, header, sections[page.section])
            button.clicked.connect(partial(self._clicked, entry))
            self._entries.append(entry)
        self.sync()
        if showing is not None and self.stack.indexOf(showing) < 0:
            self.leave()  # the page that was shown is gone

    def _add(self, widget: QWidget) -> None:
        self.menu.insertWidget(self.menu.count() - 1, widget)
        self._widgets.append(widget)

    def _clicked(self, entry: _Entry, _checked: bool = False) -> None:
        self.open_page(self.stack.indexOf(entry.host))

    def sync(self) -> None:
        """Show the entries that say they are visible, and the sections and
        groups that have one."""
        shown: set[QWidget] = set()
        for entry in self._entries:
            try:
                visible = entry.page.visible is None or bool(entry.page.visible())
            except Exception:
                logger.exception(
                    "The extension %s could not say if %s shows",
                    entry.page.extension,
                    entry.page.title,
                )
                visible = False
            entry.button.setVisible(visible)
            if visible:
                shown.update((entry.group, entry.section))
        for entry in self._entries:
            entry.group.setVisible(entry.group in shown)
            entry.section.setVisible(entry.section in shown)
            submenu = entry.button.parentWidget()
            if submenu is not None:
                submenu.setVisible(entry.group in shown)
        current = self.stack.currentWidget()
        if any(
            entry.host is current and entry.button.isHidden() for entry in self._entries
        ):
            self.leave()  # its entry went away while it was open

    def owns(self, index: int) -> bool:
        return any(self.stack.indexOf(entry.host) == index for entry in self._entries)

    def shown(self, index: int) -> tuple[str, str, Callable[[], None] | None] | None:
        """Check the entry of the page opened and build it the first time; the
        title, the subtitle and what its refresh button does, if it is one of
        these pages."""
        found: tuple[str, str, Callable[[], None] | None] | None = None
        for entry in self._entries:
            mine = self.stack.indexOf(entry.host) == index
            entry.button.setChecked(mine)
            if not mine:
                continue
            found = (entry.page.title, entry.page.subtitle, entry.page.refresh)
            if not entry.built:
                entry.built = True
                self._build(entry)
            opened = getattr(entry.host.layout().itemAt(0).widget(), "shown", None)  # type: ignore[union-attr]
            if callable(opened):
                try:
                    opened()
                except Exception:
                    logger.exception("The page %s failed", entry.page.title)
        return found

    def _build(self, entry: _Entry) -> None:
        layout = entry.host.layout()
        assert layout is not None
        try:
            widget = entry.page.factory()
        except Exception:
            logger.exception(
                "The extension %s could not build %s",
                entry.page.extension,
                entry.page.title,
            )
            widget = QLabel(self.tr("This page could not be built."))
        layout.addWidget(widget)
