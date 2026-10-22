from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QLabel,
    QLayout,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QWidget,
)


def get_application() -> QApplication:
    """The one QApplication of the run, created on first use."""
    application = QApplication.instance()
    if isinstance(application, QApplication):
        return application
    return QApplication([])


def present[T](value: T | None) -> T:
    """Narrow a Qt accessor that may return None to what the test expects."""
    assert value is not None
    return value


def cell(table: QTableWidget, row: int, column: int) -> QTableWidgetItem:
    return present(table.item(row, column))


def tab_at[T: QWidget](tabs: QTabWidget, index: int, kind: type[T]) -> T:
    widget = tabs.widget(index)
    assert isinstance(widget, kind)
    return widget


def current_tab[T: QWidget](tabs: QTabWidget, kind: type[T]) -> T:
    widget = tabs.currentWidget()
    assert isinstance(widget, kind)
    return widget


def text_at(layout: QLayout, index: int) -> str:
    """The text of the label or button laid out at `index`."""
    widget = present(layout.itemAt(index)).widget()
    assert isinstance(widget, (QLabel, QAbstractButton))
    return widget.text()
