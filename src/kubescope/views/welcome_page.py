"""The welcome page: a page over the middle of the app, with what is useful to
know and, after an update, what is new in it.

It takes the place of the side menu and the pages and leaves the top bar
and the footer. The person can ask never to see it again.
"""

from collections.abc import Callable

from PySide6.QtCore import QEvent, QObject, QRect, Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from kubescope.about import PROJECT_URL, SPONSOR_URL
from kubescope.dialogs.changelog_dialog import changelog_html
from kubescope.theme import themed
from kubescope.utils.changelog import Version

CONTENT_WIDTH = 880  # the text is read in a column, not across a wide window


def _style() -> str:
    text, muted = themed("#17191e", text=True), themed("#6b7380", text=True)
    return (
        f"#welcomePage {{ background: {themed('#f7f7fa')}; }}"
        f"QScrollArea#welcomeScroll {{ background: {themed('#f7f7fa')}; border: 0; }}"
        f"QScrollArea#welcomeScroll > QWidget > QWidget {{ background:"
        f" {themed('#f7f7fa')}; }}"
        f"QFrame#welcomeCard {{ background: {themed('#ffffff')};"
        f" border: 1px solid {themed('#e1e3e9')}; border-radius: 10px; }}"
        f"QFrame#welcomeCard QLabel {{ background: transparent; color: {text}; }}"
        f"QLabel#welcomeTitle {{ color: {text}; font-size: 26px; font-weight: 700; }}"
        f"QLabel#welcomeLead, QLabel#welcomeNote {{ color: {muted}; font-size: 14px; }}"
        f"QLabel#welcomeHeading {{ color: {text}; font-size: 16px; font-weight: 700; }}"
        f"QFrame#welcomeFooter {{ background: {themed('#ffffff')};"
        f" border-top: 1px solid {themed('#e4e5eb')}; }}"
        f"QLabel#welcomeCardText {{ color: {muted}; }}"
    )


class WelcomePage(QFrame):
    """What is useful to know about KubeScope, and what is new after an update.

    `news` are the versions released since the one the person had; none
    on a first run.
    """

    closed = Signal(bool)  # the person is done; whether never to show it again
    changelog_requested = Signal()

    def __init__(
        self,
        parent: QWidget,
        logo: str,
        version: str,
        news: list[Version],
        previous: str = "",
    ) -> None:
        super().__init__(parent)
        self.version = version
        self.setObjectName("welcomePage")
        self.setStyleSheet(_style())
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.scroller = QScrollArea()
        self.scroller.setObjectName("welcomeScroll")
        self.scroller.setWidgetResizable(True)
        self.scroller.setFrameShape(QFrame.Shape.NoFrame)
        body = QWidget()
        body.setObjectName("welcomePage")
        column = QVBoxLayout(body)
        column.setContentsMargins(24, 28, 24, 28)
        column.setSpacing(18)
        column.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.column = QWidget()
        self.column.setMaximumWidth(CONTENT_WIDTH)
        inner = QVBoxLayout(self.column)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(18)
        inner.addLayout(self._header(logo, bool(news)))
        if news:
            inner.addWidget(self._news(news, previous))
        inner.addWidget(self._heading(self.tr("Good to know")))
        for title, text in self._tips():
            inner.addWidget(self._card(title, text))
        inner.addWidget(self._contribute())
        inner.addStretch(1)
        column.addWidget(self.column, 1)
        self.scroller.setWidget(body)
        outer.addWidget(self.scroller, 1)
        outer.addWidget(self._footer())

    # the parts

    def _header(self, logo: str, updated: bool) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(16)
        picture = QLabel()
        picture.setPixmap(QPixmap(logo).scaledToWidth(56))
        names = QVBoxLayout()
        names.setSpacing(2)
        self.title = QLabel(
            self.tr("KubeScope {version}").format(version=self.version)
            if updated
            else self.tr("Welcome to KubeScope")
        )
        self.title.setObjectName("welcomeTitle")
        lead = QLabel(
            self.tr(
                "A desktop IDE for Kubernetes. It is read-only by default and runs "
                "on this computer."
            )
        )
        lead.setObjectName("welcomeLead")
        lead.setWordWrap(True)
        names.addWidget(self.title)
        names.addWidget(lead)
        row.addWidget(picture, 0, Qt.AlignmentFlag.AlignTop)
        row.addLayout(names, 1)
        return row

    @staticmethod
    def _heading(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("welcomeHeading")
        return label

    def _news(self, news: list[Version], previous: str) -> QFrame:
        """What changed since the version the person had, in a card."""
        card = QFrame()
        card.setObjectName("welcomeCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        layout.addWidget(self._heading(self.tr("What's new")))
        note = QLabel(
            self.tr("Updated from {previous} to {version}.").format(
                previous=previous, version=self.version
            )
        )
        note.setObjectName("welcomeNote")
        layout.addWidget(note)
        text = QLabel(changelog_html(news, self.version))
        text.setTextFormat(Qt.TextFormat.RichText)
        text.setWordWrap(True)
        text.setOpenExternalLinks(True)
        text.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(text)
        self.news_text = text
        more = QPushButton(self.tr("Full changelog"))
        more.setProperty("variant", "secondary")
        more.clicked.connect(self.changelog_requested)
        layout.addWidget(more, 0, Qt.AlignmentFlag.AlignLeft)
        return card

    def _tips(self) -> list[tuple[str, str]]:
        return [
            (
                self.tr("Connect your clusters"),
                self.tr(
                    "KubeScope reads your kubeconfig. Pick a context in the top bar; "
                    "connect or disconnect contexts in Settings → Kube."
                ),
            ),
            (
                self.tr("Read-only by default"),
                self.tr(
                    "Nothing changes in a cluster unless you turn on the write mode "
                    "in Settings, and each change is confirmed first."
                ),
            ),
            (
                self.tr("Make it yours"),
                self.tr(
                    "Install extensions (the AI assistant Gabi, AWS and more), "
                    "themes and languages from Settings."
                ),
            ),
        ]

    def _card(self, title: str, text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("welcomeCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(4)
        layout.addWidget(self._heading(title))
        body = QLabel(text)
        body.setObjectName("welcomeCardText")
        body.setWordWrap(True)
        layout.addWidget(body)
        return card

    def _contribute(self) -> QFrame:
        card = self._card(
            self.tr("Contribute"),
            self.tr(
                "KubeScope is free and open source software. If it helps you, "
                "please consider contributing: star the project on GitHub, report "
                "a problem, suggest an idea, translate it into your language, send "
                "a pull request or become a sponsor."
            ),
        )
        layout = card.layout()
        assert isinstance(layout, QVBoxLayout)
        row = QHBoxLayout()
        row.setSpacing(8)
        for label, address in (
            (self.tr("Open on GitHub"), PROJECT_URL),
            (self.tr("Sponsor on GitHub"), SPONSOR_URL),
        ):
            button = QPushButton(label)
            button.setProperty("variant", "secondary")
            button.clicked.connect(
                lambda _checked=False, url=address: QDesktopServices.openUrl(QUrl(url))
            )
            row.addWidget(button)
        row.addStretch(1)
        layout.addLayout(row)
        return card

    def _footer(self) -> QFrame:
        footer = QFrame()
        footer.setObjectName("welcomeFooter")
        row = QHBoxLayout(footer)
        row.setContentsMargins(24, 10, 24, 10)
        self.never = QCheckBox(self.tr("Don't show this again"))
        start = QPushButton(self.tr("Start using KubeScope"))
        start.setProperty("variant", "primary")
        start.clicked.connect(lambda: self.closed.emit(self.never.isChecked()))
        self.start = start
        row.addWidget(self.never)
        row.addStretch(1)
        row.addWidget(start)
        return footer


class Overlay(QObject):
    """Keeps a page over an area of its host, however the host is resized."""

    def __init__(self, host: QWidget, page: QWidget, area: Callable[[], QRect]) -> None:
        super().__init__(page)
        self.host, self.page, self.area = host, page, area
        host.installEventFilter(self)
        self.place()

    def place(self) -> None:
        self.page.setGeometry(self.area())
        self.page.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.host and event.type() == QEvent.Type.Resize:
            self.place()
        return False
