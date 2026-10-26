import os
import sys

import pytest


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Never read or write the real user settings during tests."""
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path / "config"))


# What the offscreen platform says about things a desktop has: it reports a system
# tray (the window in a test has no icon for it) and cannot raise a window or
# connect the tray signal or propagate size hints. Nothing in these lines is
# about the code under test.
_OFFSCREEN_NOISE = (
    "QSystemTrayIcon::setVisible: No Icon set",
    "No such signal QPlatformNativeInterface::systemTrayWindowChanged",
    "This plugin does not support raise()",
    "This plugin does not support propagateSizeHints()",
)


@pytest.fixture(scope="session", autouse=True)
def quiet_offscreen_platform():
    """Leave out the messages the offscreen platform always prints; every other
    message of Qt still reaches the log."""
    from PySide6.QtCore import qInstallMessageHandler

    def handler(_mode, _context, message):
        if not any(noise in message for noise in _OFFSCREEN_NOISE):
            print(message, file=sys.stderr)

    previous = qInstallMessageHandler(handler)
    yield
    qInstallMessageHandler(previous)


@pytest.fixture(autouse=True)
def no_cached_namespaces():
    """Namespaces, Pod metrics and failed sign-ins are kept for a while; a test
    starts without."""
    from kubescope import cluster

    cluster._namespaces.clear()
    cluster._metrics.clear()
    cluster._sign_in_failures.clear()
    yield
    cluster._namespaces.clear()
    cluster._metrics.clear()
    cluster._sign_in_failures.clear()


@pytest.fixture(autouse=True)
def no_blocking_dialogs(monkeypatch):
    """A modal dialog nobody can answer would hang the run; fail fast instead.

    Tests that exercise a dialog replace `exec` themselves.
    """
    from PySide6.QtWidgets import QDialog, QMessageBox

    def refuse(*_args, **_kwargs):
        running = os.environ.get("PYTEST_CURRENT_TEST", "no test")
        raise AssertionError(f"a test opened a real modal dialog ({running})")

    monkeypatch.setattr(QDialog, "exec", refuse)
    monkeypatch.setattr(QMessageBox, "exec", refuse)


@pytest.fixture(autouse=True)
def light_theme():
    """The theme is process-wide state; every test starts and ends on light."""
    from kubescope import theme

    theme.set_theme("light")
    yield
    theme.set_theme("light")


@pytest.fixture(autouse=True)
def no_update_check_network(monkeypatch):
    """Tests never ask GitHub for a release; they fake the answer when they
    need it."""

    def offline(*_args, **_kwargs):
        raise OSError("the network is off in tests")

    monkeypatch.setattr("kubescope.utils.updates._get", offline)
    monkeypatch.setattr("kubescope.window.UPDATE_SEARCH_MS", 0)


@pytest.fixture(autouse=True)
def default_cluster_settings():
    """The kubeconfig files and sign-in commands are process-wide state."""
    from kubescope import cluster

    cluster.configure()
    yield
    cluster.configure()


@pytest.fixture(autouse=True)
def finish_workers_with_the_test(monkeypatch):
    """A worker thread a test started ends with that test.

    A window that a test leaves open keeps its workers running, and what
    they answer would reach a window, or a dialog, of the next test; one
    still running when the process ends can abort it. Their signals are
    cut, the threads are waited for, and the answers already queued for
    a window are dropped.
    """
    from PySide6.QtCore import QCoreApplication, QEvent, QThread
    from PySide6.QtWidgets import QApplication

    started: list[QThread] = []
    original = QThread.start

    def start(self, *args, **kwargs):
        started.append(self)
        return original(self, *args, **kwargs)

    monkeypatch.setattr(QThread, "start", start)
    yield
    for worker in started:
        worker.blockSignals(True)
    for worker in started:
        worker.wait(10_000)
    # a signal sent before the signals were cut waits in the queue of the window
    for widget in QApplication.allWidgets():
        QCoreApplication.removePostedEvents(widget, QEvent.Type.MetaCall.value)
