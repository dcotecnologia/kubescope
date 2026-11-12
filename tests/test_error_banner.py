import pytest
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from kubescope.views.error_banner import ErrorBanner
from tests.qt import get_application

application = get_application()


@pytest.fixture
def banner():
    host = QWidget()
    layout = QVBoxLayout(host)
    frame = QFrame()
    layout.addWidget(frame)
    label, text = QLabel(), QLabel()
    details, dismiss = QPushButton(), QPushButton()
    for widget in (label, details, dismiss, text):
        layout.addWidget(widget)
    host.show()
    frame.hide()
    controller = ErrorBanner(frame, label, details, dismiss, text)
    yield controller, frame, label, details, dismiss, text
    host.close()
    host.deleteLater()


def test_the_banner_shows_a_line_and_keeps_the_original_one_click_away(banner) -> None:
    controller, frame, label, details, dismiss, text = banner

    controller.show_error(
        "Access denied.", "AccessDenied: original", ("Details", "Hide")
    )

    assert frame.isVisible() and label.text() == "Access denied."
    assert text.text() == "AccessDenied: original" and text.isHidden()
    assert details.isVisible() and details.text() == "Details"

    details.click()
    assert not text.isHidden() and details.text() == "Hide"
    details.click()
    assert text.isHidden() and details.text() == "Details"

    dismiss.click()
    assert not frame.isVisible()


def test_the_buttons_are_named_by_the_caller_and_a_banner_without_more_has_none(
    banner,
) -> None:
    controller, frame, _label, details, _dismiss, text = banner

    controller.show_error("Oops", "original", ("Detalhes", "Ocultar"))
    details.click()
    assert details.text() == "Ocultar"

    controller.show_error("Same line", "Same line")  # the original says no more
    assert not details.isVisible() and text.isHidden()
    controller.show_error("Nothing", "")
    assert not details.isVisible()

    controller.show_error("Again", "original")  # a new error closes the details
    assert details.isVisible() and text.isHidden() and details.text() == "Details"
    controller.dismiss()
    assert not frame.isVisible()
