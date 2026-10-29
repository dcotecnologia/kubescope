import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

import pytest
from PySide6.QtWidgets import QApplication

from kubescope.models import (
    ClusterOverview,
    ClusterResource,
    EventInfo,
    KindSummary,
    NodeInfo,
    WorkloadsOverview,
)
from kubescope.views import motion
from tests.test_window_flows import _ready_window

application = QApplication.instance() or QApplication([])


@pytest.fixture(autouse=True)
def moving(monkeypatch):
    monkeypatch.setattr(motion, "ENABLED", True)
    monkeypatch.setattr(motion, "DURATION_MS", 60)


def _wait(condition, seconds: float = 3.0) -> None:
    deadline = time.monotonic() + seconds
    while not condition() and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    assert condition()


def _rising(widget) -> bool:
    return isinstance(widget.graphicsEffect(), motion.SlideUpEffect)


def test_the_window_rises_into_place_the_first_time_it_shows(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    central = window.centralWidget()
    assert central is not None

    window.show()
    assert _rising(central)
    _wait(lambda: central.graphicsEffect() is None)

    window.hide()
    window.show()  # not again
    assert central.graphicsEffect() is None
    window.close()


def test_a_list_rises_when_its_rows_first_arrive_and_not_when_they_refresh(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("services")
    rows = [ClusterResource("ns", "Service", "web", ("ClusterIP",), "1d")]

    window._show_resources(["ns"], [])
    assert not _rising(window.table)  # nothing to show yet

    window._show_resources(["ns"], rows)
    assert _rising(window.table)
    _wait(lambda: window.table.graphicsEffect() is None)

    window._show_resources(["ns"], rows)  # the periodic refresh
    assert window.table.graphicsEffect() is None
    window.close()


def test_the_other_lists_rise_too(monkeypatch) -> None:
    from kubescope.models import PodInfo, Workload

    window = _ready_window(monkeypatch)
    window.show()

    window._open_list_view("pods")
    window._show_pods(["ns"], [PodInfo("ns", "p", "Running", 1, 1, "1m", ("app",))])
    assert _rising(window.table)
    _wait(lambda: window.table.graphicsEffect() is None)

    window._open_list_view("deployments")
    window._show_workloads(["ns"], [Workload("ns", "Deployment", "api", 1, 1, "1d")])
    _wait(lambda: window.table.graphicsEffect() is None)

    window._render_events(
        WorkloadsOverview(
            {"Pod": KindSummary(1, 1)},
            (EventInfo("Warning", "kubelet", "ns", "Pod: p", "crash", 1, "1m", "1m"),),
        )
    )
    assert _rising(window.workloads_table)

    window._view = "nodegroups"
    node = NodeInfo("n1", True, "worker", "v1", "1d", 2.0, 2**30, 10)
    window._show_nodes(window._context(), ClusterOverview(nodes=(node,)))
    assert _rising(window.nodes_table)
    window.close()


def test_the_animations_follow_the_setting(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    form = window.settings_ui
    assert form.animationsCheck.isChecked()

    form.animationsCheck.setChecked(False)
    window._save_preferences()

    assert window.settings.animations is False and motion.ENABLED is False
    window._open_list_view("services")
    window._show_resources(
        ["ns"], [ClusterResource("ns", "Service", "web", ("ClusterIP",), "1d")]
    )
    assert not _rising(window.table)

    form.animationsCheck.setChecked(True)
    window._save_preferences()
    assert motion.ENABLED is True
    window.close()
