import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QFrame

from kubescope.views import sidebar_resizer
from kubescope.views.sidebar_resizer import SidebarResizer

application = QApplication.instance() or QApplication([])
_SIDEBARS: list[QFrame] = []


@pytest.fixture(autouse=True)
def clear():
    yield
    for sidebar in _SIDEBARS:
        sidebar.close()
        sidebar.deleteLater()
    _SIDEBARS.clear()
    application.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def _sidebar() -> QFrame:
    sidebar = QFrame()
    _SIDEBARS.append(sidebar)
    sidebar.resize(320, 500)
    sidebar.show()
    return sidebar


def _event(kind: QEvent.Type, x: int) -> QMouseEvent:
    return QMouseEvent(
        kind,
        QPointF(1, 1),
        QPointF(x, 100),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_the_edge_of_the_menu_is_dragged_to_give_it_a_width() -> None:
    sidebar = _sidebar()
    resizer = SidebarResizer(sidebar, 320)
    chosen: list[int] = []
    resizer.width_changed.connect(chosen.append)
    grip = resizer.grip

    assert sidebar.width() == 320
    assert grip.geometry().right() + 1 == sidebar.width()  # on its right edge
    grip.mouseMoveEvent(_event(QEvent.Type.MouseMove, 900))  # no press: nothing
    assert sidebar.width() == 320

    grip.mousePressEvent(_event(QEvent.Type.MouseButtonPress, 500))
    grip.mouseMoveEvent(_event(QEvent.Type.MouseMove, 580))  # 80 to the right
    assert sidebar.width() == 400
    grip.mouseMoveEvent(_event(QEvent.Type.MouseMove, 420))  # 80 to the left
    assert sidebar.width() == 240
    grip.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, 420))
    assert chosen == [240]

    grip.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, 420))  # again
    assert chosen == [240]  # nothing was pressed


def test_the_menu_never_gets_too_narrow_or_too_wide() -> None:
    sidebar = _sidebar()
    resizer = SidebarResizer(sidebar, 320)
    grip = resizer.grip

    grip.mousePressEvent(_event(QEvent.Type.MouseButtonPress, 500))
    grip.mouseMoveEvent(_event(QEvent.Type.MouseMove, -2000))
    assert sidebar.width() == sidebar_resizer.MIN_WIDTH
    grip.mouseMoveEvent(_event(QEvent.Type.MouseMove, 5000))
    assert sidebar.width() == sidebar_resizer.MAX_WIDTH
    grip.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, 5000))


def test_a_double_click_on_the_edge_brings_back_the_usual_width() -> None:
    sidebar = _sidebar()
    resizer = SidebarResizer(sidebar, 320)
    chosen: list[int] = []
    resizer.width_changed.connect(chosen.append)
    resizer.set_width(450)
    assert sidebar.width() == 450

    resizer.grip.mouseDoubleClickEvent(_event(QEvent.Type.MouseButtonDblClick, 450))

    assert sidebar.width() == 320 and chosen == [320]


def test_the_edge_follows_the_height_and_the_width_of_the_menu() -> None:
    sidebar = _sidebar()
    resizer = SidebarResizer(sidebar, 320)

    resizer.set_width(400)
    sidebar.resize(400, 700)
    application.processEvents()

    geometry = resizer.grip.geometry()
    assert geometry.right() + 1 == 400 and geometry.height() == 700
    assert resizer.eventFilter(sidebar, QEvent(QEvent.Type.Show)) is False
