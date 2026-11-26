import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from kubescope.sdk.models import ClusterOverview

from kubescope.views.health_dot import COLORS, HealthDot
from tests.qt import get_application
from tests.test_window_flows import _ready_window

application = get_application()


def test_the_dot_has_a_color_and_a_words_for_each_state() -> None:
    dot = HealthDot()
    for state, color in COLORS.items():
        dot.set_state(state, f"is {state}")
        assert dot.state == state and dot.color.name() == color
        assert dot.toolTip() == dot.accessibleName() == f"is {state}"
    dot.set_state("nonsense", "?")
    assert dot.state == "unknown"  # a state that is not known is shown as unknown
    dot.resize(16, 16)
    assert not dot.grab().isNull()


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def test_the_dot_follows_what_the_cluster_answers(window, monkeypatch) -> None:
    monkeypatch.setattr(window, "_check_login", lambda *_a: None)
    assert window.health_dot.state == "unknown"

    window._show_overview("prod", ClusterOverview())
    assert window.health_dot.state == "ok"

    window._show_error("Unable to connect to the server: dial tcp: i/o timeout")
    assert window.health_dot.state == "error"
    assert "i/o timeout" in window.health_dot.toolTip()

    window._show_overview_error(
        "error: You must be logged in to the server (Unauthorized)"
    )
    assert window.health_dot.state == "auth"

    window._answered("prod", None, "deployments", [], [])
    assert window.health_dot.state == "ok"
    window._answered("elsewhere", None, "deployments", [], [])  # not the one on screen
    assert window.health_dot.state == "ok"

    window._context_changed()  # another cluster: asked again
    assert window.health_dot.state == "unknown"


def test_the_dot_goes_with_the_selector_of_contexts(window) -> None:
    window.show()
    window._apply_connections()
    assert window.health_dot.isVisibleTo(window) == window.context_combo.isVisibleTo(
        window
    )
