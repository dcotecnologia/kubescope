import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QFrame, QPushButton

from kubescope.views.sidebar_toggle import SidebarToggle

application = QApplication.instance() or QApplication([])
_KEPT: list = []


@pytest.fixture(autouse=True)
def clear():
    yield
    for widget in _KEPT:
        widget.close()
        widget.deleteLater()
    _KEPT.clear()
    application.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def _toggle(animated=False, collapsed=False):
    sidebar = QFrame()
    sidebar.setFixedWidth(240)
    button = QPushButton()
    _KEPT.extend([sidebar, button])
    heard: list[bool] = []
    toggle = SidebarToggle(
        sidebar, button, lambda: 240, lambda: animated, collapsed=collapsed
    )
    toggle.toggled.connect(heard.append)
    return toggle, sidebar, button, heard


def test_the_button_hides_the_menu_and_brings_it_back() -> None:
    toggle, sidebar, button, heard = _toggle()
    sidebar.show()

    button.click()
    assert toggle.collapsed and sidebar.isHidden() and heard == [True]

    button.click()
    assert not toggle.collapsed and not sidebar.isHidden() and heard == [True, False]
    assert sidebar.width() == 240


def test_it_slides_by_its_width_while_the_animations_are_on() -> None:
    toggle, sidebar, _button, _heard = _toggle(animated=True)
    sidebar.show()

    toggle.collapse()
    toggle.animation.setCurrentTime(toggle.animation.duration() // 2)
    assert 0 < sidebar.width() < 240 and not sidebar.isHidden()  # on its way
    toggle.animation.setCurrentTime(toggle.animation.duration())
    assert sidebar.isHidden()

    toggle.expand()
    assert sidebar.width() == 0 and not sidebar.isHidden()  # it starts from nothing
    toggle.animation.setCurrentTime(toggle.animation.duration())
    assert sidebar.width() == 240


def test_a_menu_that_was_left_hidden_starts_hidden_and_comes_back() -> None:
    toggle, sidebar, _button, heard = _toggle(collapsed=True)
    assert sidebar.isHidden()

    toggle.collapse()  # already hidden: nothing happens
    toggle.expand()
    toggle.expand()  # already shown

    assert not sidebar.isHidden() and sidebar.width() == 240 and heard == [False]
