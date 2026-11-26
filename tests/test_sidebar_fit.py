import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from kubescope import window as window_module
from tests.test_window_flows import _ready_window


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    shown.show()
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def test_the_side_menu_is_as_wide_as_its_longest_name_needs(window) -> None:
    window.settings.sidebar_width = 0
    window._fit_sidebar()
    needed = window._menu_width()
    assert window_module.SIDEBAR_WIDTH <= needed <= window_module.SIDEBAR_MAX
    assert window.ui.sidebar.width() == needed == window.sidebar_resizer.default

    longest = window.nav_workloads.__class__(
        "Validating Webhook Configurations Of The Cluster"
    )
    longest.setProperty("nav", "true")
    longest.setParent(window.ui.sidebarNav)
    assert window._menu_width() > needed  # a longer name makes it wider
    longest.deleteLater()


def test_a_width_the_person_gave_is_kept_and_the_usual_one_is_stored_as_none(
    window,
) -> None:
    window.settings.sidebar_width = 0
    window._fit_sidebar()
    window._keep_sidebar_width(window.sidebar_resizer.default)
    assert window.settings.sidebar_width == 0  # the fitted width is no choice

    window._keep_sidebar_width(200)
    assert window.settings.sidebar_width == 200
    window.sidebar_resizer.set_width(200)
    window._fit_sidebar()  # chosen by hand: left alone
    assert window.ui.sidebar.width() == 200


def test_the_side_menu_never_scrolls_sideways(window) -> None:
    bar = window.ui.sidebarScroll.horizontalScrollBar()
    bar.setRange(0, 80)
    bar.setValue(40)  # what revealing an entry did before
    assert bar.value() == 0
