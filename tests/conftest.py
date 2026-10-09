import pytest


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Never read or write the real user settings during tests."""
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path / "config"))


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
