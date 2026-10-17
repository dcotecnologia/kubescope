from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from kubescope import PROJECT_URL, __version__
from kubescope.theme import themed
from kubescope.utils.changelog import (
    Version,
    inline_html,
    parse_changelog,
    read_changelog,
)


def changelog_html(versions: list[Version], current: str = "") -> str:
    """The versions as rich text in the colors of the active theme: a heading
    with the date for each version (and a badge on the one installed), a
    colored badge for each section and a spaced list."""
    text, muted = themed("#20232a", text=True), themed("#6b7380", text=True)
    accent, soft = themed("#3220a0", text=True), themed("#eee9f7")
    border = themed("#e1e3e9")
    good, good_bg = themed("#176b58", text=True), themed("#e5f4eb")
    warning, warning_bg = themed("#985415", text=True), themed("#fff2de")
    bad, bad_bg = themed("#a33d45", text=True), themed("#fce9ea")
    tone = {
        "Added": (good, good_bg),
        "Changed": (accent, soft),
        "Fixed": (warning, warning_bg),
        "Removed": (bad, bad_bg),
        "Security": (bad, bad_bg),
    }
    translate = QCoreApplication.translate
    badge = translate("ChangelogDialog", "INSTALLED")
    names = {
        "Added": translate("ChangelogDialog", "ADDED"),
        "Changed": translate("ChangelogDialog", "CHANGED"),
        "Fixed": translate("ChangelogDialog", "FIXED"),
        "Removed": translate("ChangelogDialog", "REMOVED"),
        "Security": translate("ChangelogDialog", "SECURITY"),
    }
    parts = [f'<div style="color: {text}; font-size: 13px;">']
    for index, version in enumerate(versions):
        installed = (
            f' <span style="background-color: {soft}; color: {accent};'
            f' font-size: 10px;">&nbsp;{badge}&nbsp;</span>'
            if version.name == current
            else ""
        )
        date = version.date
        parts.append(
            f'<table width="100%" style="margin-top: {18 if index else 4}px;">'
            f'<tr><td><span style="font-size: 20px; font-weight: 700;">'
            f"{version.name}</span>{installed}</td>"
            f'<td align="right" style="color: {muted};">{date}</td></tr></table>'
            f'<hr style="background-color: {border}; border: 0;">'
        )
        for title, items in version.sections:
            color, background = tone.get(title, (muted, border))
            parts.append(
                f'<p style="margin: 12px 0 2px 0;"><span style="background-color: '
                f"{background}; color: {color}; font-size: 10px; font-weight: 700;"
                f'">&nbsp;{names.get(title, title.upper())}&nbsp;</span></p>'
                '<ul style="margin-top: 4px;">'
            )
            for item in items:
                body = inline_html(item, muted, accent)
                parts.append(f'<li style="margin-bottom: 6px;">{body}</li>')
            parts.append("</ul>")
    parts.append("</div>")
    return "".join(parts)


class ChangelogDialog(QDialog):
    """What changed in each version, read from the changelog the app
    carries."""

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("Changelog"))
        self.resize(680, 560)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        self.text = QTextBrowser()
        self.text.setOpenExternalLinks(True)  # the links of the releases
        changelog = read_changelog()
        if changelog is None:
            self.text.setPlainText(
                self.tr("The changelog is not available in this installation.")
            )
        elif versions := [
            v for v in parse_changelog(changelog) if v.name.lower() != "unreleased"
        ]:  # what is not released yet is not news to the person using the app
            self.text.setHtml(changelog_html(versions, __version__))
        else:  # not in the usual format: show it as it is
            self.text.setMarkdown(changelog)
        layout.addWidget(self.text, 1)
        actions = QHBoxLayout()
        releases = QPushButton(self.tr("Open the releases on GitHub"))
        releases.setProperty("variant", "secondary")
        releases.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(f"{PROJECT_URL}/releases"))
        )
        close_button = QPushButton(self.tr("Close"))
        close_button.setProperty("variant", "primary")
        close_button.setDefault(True)
        close_button.clicked.connect(self.accept)
        actions.addWidget(releases)
        actions.addStretch()
        actions.addWidget(close_button)
        layout.addLayout(actions)
