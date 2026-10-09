from kubescope import app
from kubescope.settings import Settings


def _capture_logging(monkeypatch) -> list:
    calls = []
    monkeypatch.setattr(app, "configure_logging", lambda **kwargs: calls.append(kwargs))
    return calls


def test_debug_is_off_by_default(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    calls = _capture_logging(monkeypatch)

    assert app.configure_debug(Settings(tmp_path / "s.json")) is False
    assert calls == [{"to_file": False, "to_console": False}]


def test_debug_follows_the_setting_and_the_environment(monkeypatch, tmp_path) -> None:
    calls = _capture_logging(monkeypatch)
    settings = Settings(tmp_path / "s.json")

    settings.debug_logging = True
    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    assert app.configure_debug(settings) is True
    assert calls[-1] == {"to_file": True, "to_console": False}

    settings.debug_logging = False
    monkeypatch.setenv(app.DEBUG_ENV, "1")
    assert app.configure_debug(settings) is True
    assert calls[-1] == {"to_file": False, "to_console": True}


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
    _capture_logging(monkeypatch)
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "load_app_icon", lambda: "icon")
    monkeypatch.setattr(
        app, "apply_theme", lambda _app, name: events.append(("theme", name))
    )
    monkeypatch.setattr(
        app, "apply_language", lambda code: events.append(("lang", code))
    )
    monkeypatch.setattr(
        app, "install_community_themes", lambda: events.append("community themes")
    )
    monkeypatch.setattr(app, "WorkloadWindow", FakeWindow)

    assert app.main() == 7
    # the shipped themes are installed first, so a saved choice of one can apply
    assert events.index("community themes") < events.index(("theme", "light"))
    assert ("name", "KubeScope") in events
    assert ("lang", "auto") in events
    assert events[-2:] == ["show", "exec"]
