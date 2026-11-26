import os
import re

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QAbstractButton,
    QLineEdit,
    QPushButton,
    QTableView,
    QWidget,
)

from kubescope.utils.accessibility import name_icon_buttons
from tests.qt import get_application
from tests.test_window_flows import _ready_window

application = get_application()


def test_a_button_without_text_is_named_by_its_tooltip() -> None:
    root = QWidget()
    one = QPushButton(root)
    one.setToolTip("Refresh")
    named = QPushButton(root)
    named.setToolTip("Tip")
    named.setAccessibleName("Own name")
    lonely = QPushButton(root)
    with_text = QPushButton("Save", root)
    with_text.setToolTip("Tip")

    assert name_icon_buttons(root) == [lonely]
    assert one.accessibleName() == "Refresh"
    assert named.accessibleName() == "Own name"
    assert with_text.accessibleName() == ""


def test_the_buttons_qt_makes_inside_a_widget_get_a_name() -> None:
    root = QWidget()
    search = QLineEdit(root)
    search.setClearButtonEnabled(True)
    QTableView(root)

    assert name_icon_buttons(root) == []
    names = {b.accessibleName() for b in root.findChildren(QAbstractButton)}
    assert {"Clear", "Select all"} <= names


def test_every_icon_button_of_the_window_has_a_name(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    assert [b.objectName() for b in name_icon_buttons(window)] == []
    window.close()


def test_the_text_size_is_chosen_in_the_preferences(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    combo = window.settings_ui.textSizeCombo
    assert combo.currentData() == 100

    combo.setCurrentIndex(combo.findData(130))
    window._save_preferences()
    assert window.settings.text_size == 130
    assert application.font().pointSize() == 12

    combo.setCurrentIndex(combo.findData(100))
    window._save_preferences()
    assert application.font().pointSize() == 9
    window.close()


def test_the_text_size_reaches_the_sizes_of_the_style_sheet(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    before = window.styleSheet()
    first = re.search(r'cardValue"\] \{[^}]*font-size: (\d+)px', before)
    assert first is not None and first.group(1) == "20"  # the value of a card

    window.settings_ui.textSizeCombo.setCurrentIndex(
        window.settings_ui.textSizeCombo.findData(150)
    )
    window._save_preferences()
    value = re.search(r'cardValue"\] \{[^}]*font-size: (\d+)px', window.styleSheet())
    assert value is not None and value.group(1) == "30"  # 20 px at 150%

    window.settings_ui.textSizeCombo.setCurrentIndex(
        window.settings_ui.textSizeCombo.findData(100)
    )
    window._save_preferences()
    assert window.styleSheet() == before
    window.close()
