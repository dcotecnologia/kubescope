import ctypes
from pathlib import Path
from types import SimpleNamespace

from kubescope import app
from kubescope.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


def _capture_logging(monkeypatch) -> list:
    calls = []
    monkeypatch.setattr(app, "configure_logging", lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(app.crashreport, "install", lambda: None)
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


class FakeInstance:
    running = False

    class activated:
        @staticmethod
        def connect(_slot) -> None:
            pass

    def notify_running(self) -> bool:
        return self.running

    def listen(self) -> bool:
        return True


def test_main_builds_the_window_and_runs_the_event_loop(monkeypatch) -> None:
    events = []

    class FakeApplication:
        def __init__(self, _arguments) -> None:
            events.append("application")

        def setApplicationName(self, name) -> None:
            events.append(("name", name))

        def installEventFilter(self, _filter) -> None:
            events.append("dialog slide")

        def setWindowIcon(self, _icon) -> None:
            events.append("icon")

        def exec(self) -> int:
            events.append("exec")
            return 7

    class FakeWindow:
        def __init__(self, settings) -> None:
            events.append(("window", settings))

        def bring_to_front(self) -> None:
            pass

        def show(self) -> None:
            events.append("show")

        def start_update_check(self) -> None:
            events.append("update check")

        def show_welcome(self) -> None:
            events.append("welcome")

    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    _capture_logging(monkeypatch)
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "install_wheel_guard", lambda _app: None)
    monkeypatch.setattr(app, "SingleInstance", FakeInstance)
    monkeypatch.setattr(app, "load_app_icon", lambda: "icon")
    monkeypatch.setattr(app, "apply_fonts", lambda _app: events.append("fonts"))
    monkeypatch.setattr(
        app, "apply_theme", lambda _app, name: events.append(("theme", name))
    )
    monkeypatch.setattr(
        app, "apply_language", lambda code: events.append(("lang", code))
    )
    monkeypatch.setattr(
        app, "install_bundled_themes", lambda: events.append("bundled themes")
    )
    monkeypatch.setattr(app, "WorkloadWindow", FakeWindow)

    assert app.main() == 7
    # the shipped themes are installed first, so a saved choice of one can apply
    assert events.index("bundled themes") < events.index(("theme", "dark"))
    assert events.index("fonts") < events.index(("theme", "dark"))  # before widgets
    assert ("name", "KubeScope") in events
    assert "dialog slide" in events  # every dialog rises as it opens
    assert ("lang", "auto") in events
    assert events[-4:] == ["show", "update check", "welcome", "exec"]


def test_old_logs_are_purged_on_a_thread_that_spares_the_open_files(
    monkeypatch, tmp_path
) -> None:
    calls = []
    monkeypatch.setattr(app, "purge_old_logs", lambda **kw: calls.append(kw))
    settings = Settings(tmp_path / "s.json")

    app.start_log_purge(settings).join()
    settings.debug_logging = True
    thread = app.start_log_purge(settings)
    thread.join()

    assert calls == [{"keep": ()}, {"keep": ("kubescope.log", "crash.log")}]
    assert thread.daemon and thread.name == "log-purge"


def test_main_records_the_runtime_and_the_input_when_debugging(monkeypatch) -> None:
    events = []

    class FakeApplication:
        def __init__(self, _arguments) -> None:
            pass

        def setApplicationName(self, _name) -> None:
            pass

        def installEventFilter(self, _filter) -> None:
            pass

        def setWindowIcon(self, _icon) -> None:
            pass

        def exec(self) -> int:
            return 0

    class FakeWindow:
        def __init__(self, _settings) -> None:
            pass

        def bring_to_front(self) -> None:
            pass

        def show(self) -> None:
            pass

        def start_update_check(self) -> None:
            pass

        def show_welcome(self) -> None:
            pass

    monkeypatch.setenv(app.DEBUG_ENV, "1")
    _capture_logging(monkeypatch)
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "install_wheel_guard", lambda _app: None)
    monkeypatch.setattr(app, "SingleInstance", FakeInstance)
    monkeypatch.setattr(app, "load_app_icon", lambda: "icon")
    monkeypatch.setattr(app, "apply_fonts", lambda _app: None)
    monkeypatch.setattr(app, "apply_theme", lambda _app, _name: None)
    monkeypatch.setattr(app, "apply_language", lambda _code: None)
    monkeypatch.setattr(app, "install_bundled_themes", lambda: None)
    monkeypatch.setattr(app, "WorkloadWindow", FakeWindow)
    monkeypatch.setattr(app, "record_runtime", lambda: events.append("runtime"))
    monkeypatch.setattr(app, "trace_input", lambda _app: events.append("input"))

    app.main()

    assert events == ["runtime", "input"]


def test_main_installs_the_crash_hooks_and_offers_the_pending_report(
    monkeypatch,
) -> None:
    events = []

    class FakeApplication:
        def __init__(self, _arguments) -> None:
            pass

        def setApplicationName(self, _name) -> None:
            pass

        def installEventFilter(self, _filter) -> None:
            pass

        def setWindowIcon(self, _icon) -> None:
            pass

        def exec(self) -> int:
            return 0

    class FakeWindow:
        def __init__(self, _settings) -> None:
            pass

        def bring_to_front(self) -> None:
            pass

        def show(self) -> None:
            pass

        def start_update_check(self) -> None:
            pass

        def show_welcome(self) -> None:
            events.append("welcome")

    monkeypatch.delenv(app.DEBUG_ENV, raising=False)
    _capture_logging(monkeypatch)
    monkeypatch.setattr(app.crashreport, "install", lambda: events.append("hooks"))
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "install_wheel_guard", lambda _app: None)
    monkeypatch.setattr(app, "SingleInstance", FakeInstance)
    monkeypatch.setattr(app, "load_app_icon", lambda: "icon")
    monkeypatch.setattr(app, "apply_fonts", lambda _app: None)
    monkeypatch.setattr(app, "apply_theme", lambda _app, _name: None)
    monkeypatch.setattr(app, "apply_language", lambda _code: None)
    monkeypatch.setattr(app, "install_bundled_themes", lambda: None)
    monkeypatch.setattr(app, "WorkloadWindow", FakeWindow)
    monkeypatch.setattr(
        app, "show_pending_crash_report", lambda _window: events.append("report")
    )

    app.main()

    assert events == ["hooks", "report", "welcome"]


def test_a_second_start_asks_the_first_to_come_forward_and_quits(monkeypatch) -> None:
    class Second(FakeInstance):
        running = True

    class FakeApplication:
        def __init__(self, _arguments) -> None:
            pass

    started = []
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "SingleInstance", Second)
    monkeypatch.setattr(app, "WorkloadWindow", lambda *_a: started.append("window"))
    _capture_logging(monkeypatch)

    assert app.main() == 0
    assert started == []


def test_windows_is_told_which_application_this_is(monkeypatch) -> None:
    told = []
    shell32 = SimpleNamespace(
        SetCurrentProcessExplicitAppUserModelID=lambda app_id: told.append(app_id)
    )
    monkeypatch.setattr(
        ctypes, "windll", SimpleNamespace(shell32=shell32), raising=False
    )

    monkeypatch.setattr(app.sys, "platform", "linux")
    app.set_app_user_model_id()
    assert told == []  # only Windows has one

    monkeypatch.setattr(app.sys, "platform", "win32")
    app.set_app_user_model_id()
    assert told == [app.APP_ID]


def test_the_installer_gives_its_shortcuts_the_id_the_app_sets() -> None:
    script = (ROOT / "packaging/windows/kubescope.iss").read_text(encoding="utf-8")
    icons = script.split("[Icons]")[1].split("[Run]")[0]
    shortcuts = [line for line in icons.splitlines() if line.startswith("Name:")]

    assert shortcuts and all(f'AppUserModelID: "{app.APP_ID}"' in s for s in shortcuts)
