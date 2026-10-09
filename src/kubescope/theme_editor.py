"""The dialog where people create and edit their own themes."""

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from kubescope.theme import BUILTIN, DARK, LIGHT, theme_tokens


def token_labels() -> dict[str, str]:
    """What each color role is called, in the language in use."""
    return {
        "page": QCoreApplication.translate("ThemeEditor", "Page background"),
        "surface": QCoreApplication.translate("ThemeEditor", "Panels and cards"),
        "surface_alt": QCoreApplication.translate("ThemeEditor", "Alternate panels"),
        "track": QCoreApplication.translate("ThemeEditor", "Bar tracks"),
        "border": QCoreApplication.translate("ThemeEditor", "Borders"),
        "topbar": QCoreApplication.translate("ThemeEditor", "Top bar"),
        "topbar_brand": QCoreApplication.translate("ThemeEditor", "Top bar logo"),
        "topbar_field": QCoreApplication.translate("ThemeEditor", "Top bar selector"),
        "topbar_border": QCoreApplication.translate(
            "ThemeEditor", "Top bar selector border"
        ),
        "topbar_selection": QCoreApplication.translate(
            "ThemeEditor", "Top bar selection"
        ),
        "topbar_text": QCoreApplication.translate("ThemeEditor", "Top bar text"),
        "text": QCoreApplication.translate("ThemeEditor", "Text"),
        "title": QCoreApplication.translate("ThemeEditor", "Sidebar title"),
        "muted": QCoreApplication.translate("ThemeEditor", "Secondary text"),
        "subtle": QCoreApplication.translate("ThemeEditor", "Disabled text"),
        "accent": QCoreApplication.translate("ThemeEditor", "Accent text and links"),
        "accent_strong": QCoreApplication.translate("ThemeEditor", "Accent buttons"),
        "accent_hover": QCoreApplication.translate(
            "ThemeEditor", "Accent buttons on hover"
        ),
        "accent_disabled": QCoreApplication.translate(
            "ThemeEditor", "Accent buttons when disabled"
        ),
        "focus": QCoreApplication.translate("ThemeEditor", "Focus and highlights"),
        "badge_text": QCoreApplication.translate("ThemeEditor", "Badge text"),
        "accent_soft": QCoreApplication.translate("ThemeEditor", "Accent tint"),
        "selection": QCoreApplication.translate("ThemeEditor", "Text selection"),
        "accent_border": QCoreApplication.translate("ThemeEditor", "Accent border"),
        "on_accent": QCoreApplication.translate(
            "ThemeEditor", "Text on the top bar and accent buttons"
        ),
        "good": QCoreApplication.translate("ThemeEditor", "Healthy text"),
        "good_bg": QCoreApplication.translate("ThemeEditor", "Healthy background"),
        "warning": QCoreApplication.translate("ThemeEditor", "Warning text"),
        "warning_bg": QCoreApplication.translate("ThemeEditor", "Warning background"),
        "bad": QCoreApplication.translate("ThemeEditor", "Failing text"),
        "bad_bg": QCoreApplication.translate("ThemeEditor", "Failing background"),
        "idle": QCoreApplication.translate("ThemeEditor", "Idle text"),
        "idle_bg": QCoreApplication.translate("ThemeEditor", "Idle background"),
        "problem_row": QCoreApplication.translate("ThemeEditor", "Row with a problem"),
        "young_row": QCoreApplication.translate("ThemeEditor", "Row of a young Pod"),
        "chunk_warning": QCoreApplication.translate(
            "ThemeEditor", "Usage bar, getting full"
        ),
        "chunk_high": QCoreApplication.translate(
            "ThemeEditor", "Usage bar, nearly full"
        ),
        "bar_ok": QCoreApplication.translate("ThemeEditor", "Health bar, healthy"),
        "bar_warning": QCoreApplication.translate("ThemeEditor", "Health bar, warning"),
        "bar_bad": QCoreApplication.translate("ThemeEditor", "Health bar, failing"),
    }


def _readable_on(color: QColor) -> str:
    return "#000000" if color.lightness() > 128 else "#ffffff"


class ThemeEditor(QDialog):
    """Name a theme, pick the theme to start from, and choose its colors."""

    def __init__(
        self,
        parent: QWidget | None,
        *,
        name: str,
        base: str,
        tokens: dict[str, str],
        new: bool,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(
            self.tr("New theme")
            if new
            else self.tr("Edit theme: {name}").format(name=name)
        )
        self.resize(480, 620)
        self._tokens = dict(tokens)
        self._swatches: dict[str, QPushButton] = {}

        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText(self.tr("Theme name"))
        self.base_combo = QComboBox()
        self.base_combo.addItem(self.tr("Light"), LIGHT)
        self.base_combo.addItem(self.tr("Dark"), DARK)
        self.base_combo.setCurrentIndex(max(self.base_combo.findData(base), 0))
        # the base of a saved theme is fixed; a new one can restart from either
        self.base_combo.setEnabled(new)
        self.base_combo.currentIndexChanged.connect(self._restart_from_base)

        header = QFormLayout()
        header.addRow(QLabel(self.tr("Name")), self.name_edit)
        header.addRow(QLabel(self.tr("Starts from")), self.base_combo)

        colors = QWidget()
        form = QFormLayout(colors)
        for token, label in token_labels().items():
            swatch = QPushButton()
            swatch.setMinimumWidth(110)
            swatch.clicked.connect(
                lambda _checked=False, token=token: self._pick(token)
            )
            self._swatches[token] = swatch
            form.addRow(QLabel(label), swatch)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(colors)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.name_edit.textChanged.connect(self._validate)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(QLabel(self.tr("Colors")))
        layout.addWidget(scroll, 1)
        layout.addWidget(self.buttons)
        self._refresh_swatches()
        self._validate()

    def _validate(self) -> None:
        save = self.buttons.button(QDialogButtonBox.StandardButton.Save)
        save.setEnabled(bool(self.name_edit.text().strip()))

    def _refresh_swatches(self) -> None:
        for token, swatch in self._swatches.items():
            color = QColor(self._tokens[token])
            swatch.setText(self._tokens[token].lower())
            swatch.setStyleSheet(
                f"background: {color.name()}; color: {_readable_on(color)};"
                " border: 1px solid #8a919c; border-radius: 4px; padding: 5px 10px;"
            )

    def _restart_from_base(self) -> None:
        self._tokens = theme_tokens(BUILTIN[self.base_combo.currentData()])
        self._refresh_swatches()

    def _pick(self, token: str) -> None:
        chosen = QColorDialog.getColor(
            QColor(self._tokens[token]), self, token_labels()[token]
        )
        if chosen.isValid():
            self._tokens[token] = chosen.name()
            self._refresh_swatches()

    def values(self) -> tuple[str, str, dict[str, str]]:
        """The name, the base theme and the color of every role."""
        return (
            self.name_edit.text().strip(),
            self.base_combo.currentData(),
            dict(self._tokens),
        )
