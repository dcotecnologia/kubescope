import os

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
