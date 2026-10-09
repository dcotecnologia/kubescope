import logging

from kubescope import app


def test_debug_is_off_by_default(monkeypatch) -> None:
    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    calls = []
    monkeypatch.setattr(logging, "basicConfig", lambda **kwargs: calls.append(kwargs))

    assert app.configure_debug() is False
    assert calls == []


def test_debug_logs_at_debug_level_when_enabled(monkeypatch) -> None:
    monkeypatch.setenv(app.DEBUG_ENV, "1")
    calls = []
    monkeypatch.setattr(logging, "basicConfig", lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(app.faulthandler, "enable", lambda: None)

    assert app.configure_debug() is True
    assert calls[0]["level"] == logging.DEBUG
