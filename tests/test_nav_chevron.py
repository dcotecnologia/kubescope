from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QPushButton

from kubescope.views.nav_chevron import RIGHT, SIZE, NavChevron
from tests.qt import get_application

application = get_application()


def _chevron() -> tuple[QPushButton, NavChevron]:
    button = QPushButton("Network")
    button.resize(200, 30)
    button.show()  # a window that is not shown is sent no resize
    return button, NavChevron(button)


def test_the_arrow_sits_at_the_right_of_the_entry_and_follows_its_width() -> None:
    button, chevron = _chevron()
    assert chevron.x() == 200 - SIZE - RIGHT
    assert chevron.y() == (30 - SIZE) // 2

    button.resize(300, 40)
    assert chevron.x() == 300 - SIZE - RIGHT and chevron.y() == (40 - SIZE) // 2


def test_the_arrow_points_down_when_open_and_to_the_right_when_folded() -> None:
    _button, chevron = _chevron()
    opened = chevron.pixmap().toImage()
    chevron.set_open(False)
    folded = chevron.pixmap().toImage()
    assert opened != folded
    chevron.set_open(True)
    assert chevron.pixmap().toImage() == opened
    chevron.refresh()  # the theme changed: drawn again


def test_it_ignores_what_happens_to_other_objects_and_other_events() -> None:
    button, chevron = _chevron()
    assert chevron.eventFilter(QObject(), QEvent(QEvent.Type.Resize)) is False
    assert chevron.eventFilter(button, QEvent(QEvent.Type.Show)) is False
