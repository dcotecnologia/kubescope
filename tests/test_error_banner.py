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


def test_a_failed_load_offers_to_try_again() -> None:
    host = QWidget()
    layout = QVBoxLayout(host)
    frame, label, text = QFrame(), QLabel(), QLabel()
    details, dismiss, retry = QPushButton(), QPushButton(), QPushButton()
    for widget in (frame, label, details, dismiss, retry, text):
        layout.addWidget(widget)
    host.show()
    controller = ErrorBanner(frame, label, details, dismiss, text, retry_button=retry)
    asked: list[int] = []
    controller.retry_requested.connect(lambda: asked.append(1))

    controller.show_error("Timed out.", "original", retry=True)
    assert retry.isVisible()
    retry.click()
    assert asked == [1] and not frame.isVisible()

    controller.show_error("Access denied.", "original")
    assert not retry.isVisible()
    host.close()


def test_a_list_that_failed_to_load_is_tried_again_from_the_banner(monkeypatch) -> None:
    from tests.test_window_flows import _ready_window

    window = _ready_window(monkeypatch)
    tried: list[int] = []
    monkeypatch.setattr(window, "refresh", lambda *_a, **_k: tried.append(1))
    window.error_banner.retry_requested.disconnect()
    window.error_banner.retry_requested.connect(window.refresh)

    window._show_error("Unable to connect to the server: timed out")
    assert not window.ui.permissionRetry.isHidden()
    window.ui.permissionRetry.click()
    assert tried == [1]

    window._show_action_error("forbidden")
    assert window.ui.permissionRetry.isHidden()
    window.close()


def test_a_missing_sign_in_program_is_told_once_and_not_again_when_dismissed(
    monkeypatch,
) -> None:
    from kubescope.cluster import KubeProblem
    from tests.test_window_flows import _ready_window

    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window, "_save_settings", lambda: None)
    problems = [
        KubeProblem("login_missing", "aws", ("prod", "stage")),
        KubeProblem("login_missing", "az", ("blue",)),
    ]
    window.error_banner.dismiss()
    window._show_kube_problems(problems)
    assert (
        window.error_banner.frame.isVisibleTo(window)
        or not window.error_banner.frame.isHidden()
    )
    assert (
        "“aws” signs you in to 2 of your clusters" in window.error_banner.label.text()
    )
    assert window.error_banner.details_label.text() == "prod, stage"

    window.ui.permissionDismiss.click()  # the person says no
    assert window.settings.check_dismissed("login_missing:aws")
    window._show_kube_problems(problems)  # the next one is told, not the dismissed
    assert "“az”" in window.error_banner.label.text()

    window._show_error("Unable to connect to the server")  # an error takes the banner
    window.ui.permissionDismiss.click()
    assert not window.settings.check_dismissed("login_missing:az")
    window._show_kube_problems(problems)  # another banner is showing... it stays
    window.close()
