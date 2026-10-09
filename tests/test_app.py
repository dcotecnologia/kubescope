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


def test_main_builds_the_window_and_runs_the_event_loop(monkeypatch) -> None:
    events = []

    class FakeApplication:
        def __init__(self, _arguments) -> None:
            events.append("application")

        def setApplicationName(self, name) -> None:  # noqa: N802
            events.append(("name", name))

        def setWindowIcon(self, _icon) -> None:  # noqa: N802
            events.append("icon")

        def exec(self) -> int:
            events.append("exec")
            return 7

    class FakeWindow:
        def __init__(self, settings) -> None:
            events.append(("window", settings))

        def show(self) -> None:
            events.append("show")

    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "load_app_icon", lambda: "icon")
    monkeypatch.setattr(app, "apply_light_theme", lambda _app: events.append("theme"))
    monkeypatch.setattr(
        app, "apply_language", lambda code: events.append(("lang", code))
    )
    monkeypatch.setattr(app, "WorkloadWindow", FakeWindow)

    assert app.main() == 7
    assert ("name", "KubeScope") in events
    assert ("lang", "auto") in events
    assert events[-2:] == ["show", "exec"]
