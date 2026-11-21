from PySide6.QtCore import QEvent, QObject, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout, QWidget

from kubescope.views.nav_section import SectionFold
from tests.qt import get_application

application = get_application()


def make(folded=False, animated=False):
    window = QWidget()
    layout = QVBoxLayout(window)
    title = QLabel("AWS")
    body = QFrame()
    QVBoxLayout(body).addWidget(QLabel("RDS"))
    layout.addWidget(title)
    layout.addWidget(body)
    window.show()
    fold = SectionFold(title, body, folded, lambda: animated)
    heard: list[bool] = []
    fold.toggled.connect(heard.append)
    return window, fold, title, body, heard


def click(widget: QWidget, button=Qt.MouseButton.LeftButton, at=(3.0, 3.0)) -> None:
    event = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(*at),
        QPointF(*at),
        button,
        button,
        Qt.KeyboardModifier.NoModifier,
    )
    QApplication.sendEvent(widget, event)


def test_the_title_folds_the_block_and_brings_it_back() -> None:
    _window, fold, title, body, heard = make()
    open_arrow = fold.chevron.pixmap().toImage()

    click(title)
    assert fold.folded and body.isHidden() and heard == [True]
    assert fold.chevron.pixmap().toImage() != open_arrow

    click(title)
    assert not fold.folded and not body.isHidden() and heard == [True, False]


def test_only_a_click_of_the_left_button_inside_the_title_counts() -> None:
    _window, fold, title, _body, heard = make()

    click(title, Qt.MouseButton.RightButton)
    click(title, at=(5000.0, 3.0))  # released outside it
    assert not fold.folded and heard == []
    assert fold.eventFilter(QObject(), QEvent(QEvent.Type.MouseButtonRelease)) is False
    assert fold.eventFilter(title, QEvent(QEvent.Type.Show)) is False


def test_a_block_left_folded_starts_folded_and_an_unfold_may_not_be_kept() -> None:
    _window, fold, _title, body, heard = make(folded=True)
    assert body.isHidden()

    fold.set_folded(False, remember=False)  # a screen was reached by a shortcut
    fold.set_folded(False)  # already so

    assert not body.isHidden() and heard == []


def test_it_slides_while_the_animations_are_on() -> None:
    _window, fold, _title, body, _heard = make(animated=True)

    fold.toggle()
    fold.animation.setCurrentTime(fold.animation.duration() // 2)
    assert not body.isHidden() and 0 < body.maximumHeight() < 1000  # on its way
    fold.animation.setCurrentTime(fold.animation.duration())
    assert body.isHidden()

    fold.toggle()
    assert not body.isHidden() and body.maximumHeight() == 0  # starts from nothing
    fold.animation.setCurrentTime(fold.animation.duration())
    assert body.maximumHeight() == 16777215 and not body.isHidden()


def test_a_block_with_nothing_to_show_is_hidden_whole_and_a_fold_waits_for_it() -> None:
    _window, fold, title, body, _heard = make(animated=True)

    fold.set_available(False)
    assert title.isHidden() and body.isHidden()
    fold.toggle()  # folded while away: no slide, the state at once
    fold.set_available(True)
    assert not title.isHidden() and body.isHidden()
    fold.toggle()
    fold.animation.setCurrentTime(fold.animation.duration())
    assert not body.isHidden()


def test_the_header_of_a_group_is_a_button_that_clicks() -> None:
    from PySide6.QtWidgets import QPushButton

    window = QWidget()
    layout = QVBoxLayout(window)
    header = QPushButton("RDS")
    body = QFrame()
    QVBoxLayout(body).addWidget(QLabel("Instances"))
    layout.addWidget(header)
    layout.addWidget(body)
    window.show()
    fold = SectionFold(header, body, False, lambda: False)

    header.click()
    assert fold.folded and body.isHidden()
    header.click()
    assert not fold.folded and not body.isHidden()
    assert header.cursor().shape() != Qt.CursorShape.PointingHandCursor  # its own
