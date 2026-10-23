import pytest


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Never read or write the real user settings during tests."""
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path / "config"))


@pytest.fixture(autouse=True)
def no_cached_namespaces():
    """Namespaces and Pod metrics are kept for a while; a test starts
    without."""
    from kubescope import cluster

    cluster._namespaces.clear()
    cluster._metrics.clear()
    yield
    cluster._namespaces.clear()
    cluster._metrics.clear()


@pytest.fixture(autouse=True)
def no_blocking_dialogs(monkeypatch):
    """A modal dialog nobody can answer would hang the run; fail fast instead.

    Tests that exercise a dialog replace `exec` themselves.
    """
    from PySide6.QtWidgets import QDialog, QMessageBox

    def refuse(*_args, **_kwargs):
        raise AssertionError("a test opened a real modal dialog")

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
