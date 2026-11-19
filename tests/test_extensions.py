import logging
import os
from pathlib import Path
from typing import Any

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kubescope.extensions.cluster_access import ClusterBridge
from kubescope.extensions.context import ExtensionContext, Host
from kubescope.extensions.registries import CommandRegistry, EventBus
from kubescope.extensions.window_ui import WindowUi
from kubescope.sdk import (
    CONTEXT_CHANGED,
    CommandError,
    DockContribution,
    PermissionDenied,
    WriteModeOff,
)

CLUSTER = ClusterBridge()


def make_host(write_mode: bool = False) -> tuple[Host, dict[str, dict[str, Any]], list]:
    stores: dict[str, dict[str, Any]] = {}
    saved: list[bool] = []
    host = Host(
        cluster=CLUSTER,
        snapshot=lambda: "the overview",
        current_context=lambda: "dev",
        write_mode=lambda: write_mode,
        settings_data=lambda name: stores.setdefault(name, {}),
        save_settings=lambda: saved.append(True),
    )
    return host, stores, saved


def make_context(*permissions: str, write_mode: bool = False) -> ExtensionContext:
    host, _, _ = make_host(write_mode)
    return ExtensionContext("dco.test", frozenset(permissions), host)


def test_window_ui_delegates_every_extension_callback() -> None:
    from PySide6.QtWidgets import QApplication, QWidget

    calls: list[tuple] = []
    application = QApplication.instance() or QApplication([])
    ui = WindowUi(
        QWidget(),
        QWidget(),
        lambda *args: calls.append(args),
        lambda *_: None,
        lambda box: calls.append(("style", box)),
        lambda section: calls.append(("settings", section)),
        lambda owner, pixels: calls.append(("corner", owner, pixels)),
        lambda color, text: f"{color}:{text}",
        lambda *args: calls.append(("pick", *args)) or ("chosen", True),
        lambda *args: calls.append(("json", *args)),
        lambda *args: calls.append(("log", *args)),
    )

    ui.show_message("warning", "Title", "Text")
    ui.style_box("box")
    ui.show_settings("extensions")
    ui.reserve_corner("tool", 24)
    assert ui.themed("#fff", True) == "#fff:True"
    assert ui.pick_item("Pick", "One", ["a"]) == ("chosen", True)
    ui.show_json("Document", {"name": "api"})
    ui.open_log("Log", "api", lambda: "text")

    assert calls[0][1:] == ("Title", "Text")
    assert ("style", "box") in calls
    assert ("settings", "extensions") in calls
    assert ("corner", "tool", 24) in calls
    application.processEvents()


def test_event_reaches_every_handler_in_order() -> None:
    bus = EventBus()
    seen: list[tuple[str, str]] = []
    bus.on(CONTEXT_CHANGED, lambda context: seen.append(("a", context)))
    bus.on(CONTEXT_CHANGED, lambda context: seen.append(("b", context)))

    bus.emit(CONTEXT_CHANGED, context="prod")

    assert seen == [("a", "prod"), ("b", "prod")]


def test_event_handler_can_stop_listening() -> None:
    bus = EventBus()
    seen: list[str] = []
    off = bus.on(CONTEXT_CHANGED, lambda context: seen.append(context))

    off()
    off()  # stopping twice is harmless
    bus.emit(CONTEXT_CHANGED, context="prod")

    assert seen == []


def test_failing_handler_is_logged_and_does_not_stop_the_others(caplog) -> None:
    bus = EventBus()
    seen: list[str] = []

    def broken(context: str) -> None:
        raise RuntimeError("boom")

    bus.on(CONTEXT_CHANGED, broken)
    bus.on(CONTEXT_CHANGED, lambda context: seen.append(context))

    with caplog.at_level(logging.ERROR):
        bus.emit(CONTEXT_CHANGED, context="prod")

    assert seen == ["prod"]
    assert "an extension failed on the context_changed event" in caplog.text


def test_unknown_event_is_refused() -> None:
    bus = EventBus()

    with pytest.raises(ValueError, match="unknown event: nope"):
        bus.on("nope", lambda: None)
    with pytest.raises(ValueError, match="unknown event: nope"):
        bus.emit("nope")


def test_command_runs_with_keyword_arguments() -> None:
    registry = CommandRegistry()
    registry.register("select_context", lambda name: f"on {name}")

    assert registry.has("select_context")
    assert registry.names() == ["select_context"]
    assert registry.invoke("select_context", name="prod") == "on prod"


def test_command_name_belongs_to_one_command() -> None:
    registry = CommandRegistry()
    registry.register("open_tab", lambda: None)

    with pytest.raises(CommandError, match="already registered"):
        registry.register("open_tab", lambda: None)


def test_unknown_command_is_refused_and_unregister_forgets() -> None:
    registry = CommandRegistry()
    registry.register("open_tab", lambda: None)

    registry.unregister("open_tab")
    registry.unregister("open_tab")  # forgetting twice is harmless

    with pytest.raises(CommandError, match="there is no command open_tab"):
        registry.invoke("open_tab")


def test_removing_an_extension_removes_only_its_entries() -> None:
    host, _, _ = make_host()
    other = ExtensionContext("dco.b", frozenset({"ui.dock"}), host)
    entries = host.contributions
    mine = ExtensionContext(
        "dco.a", frozenset({"ui.dock", "ui.tab", "ui.settings", "cli"}), host
    )
    mine.add_dock("chat", object)
    mine.add_tab_kind("chat", object)
    mine.add_settings_section("Chat", object)
    mine.add_cli_command("chat", lambda arguments: 0)
    other.add_dock("other", object)

    entries.remove_extension("dco.a")

    assert [one.extension for one in entries.docks] == ["dco.b"]
    assert entries.tab_kinds == []
    assert entries.settings_sections == []
    assert entries.cli_commands == []


def test_contributions_keep_what_the_extension_gave() -> None:
    host, _, _ = make_host()
    context = ExtensionContext(
        "dco.test", frozenset({"ui.dock", "ui.tab", "ui.settings", "cli"}), host
    )
    context.add_dock("chat", object, shortcut="assistant")
    context.add_tab_kind("chat", object)
    context.add_settings_section("Chat", object)

    def run(arguments: list[str]) -> int:
        return 0

    context.add_cli_command("chat", run)

    assert host.contributions.docks == [
        DockContribution("dco.test", "chat", object, "assistant")
    ]
    assert host.contributions.tab_kinds[0].key == "chat"
    assert host.contributions.settings_sections[0].title == "Chat"
    assert host.contributions.cli_commands[0].run is run


def test_unknown_permission_is_refused() -> None:
    host, _, _ = make_host()

    with pytest.raises(ValueError, match="unknown permissions: teleport"):
        ExtensionContext("dco.test", frozenset({"teleport"}), host)


@pytest.mark.parametrize(
    "use",
    [
        lambda context: context.cluster,
        lambda context: context.writes,
        lambda context: context.add_dock("a", object),
        lambda context: context.add_tab_kind("a", object),
        lambda context: context.add_settings_section("a", object),
        lambda context: context.add_cli_command("a", lambda arguments: 0),
    ],
)
def test_what_was_not_asked_for_is_denied(use) -> None:
    context = make_context()

    with pytest.raises(PermissionDenied, match="dco.test did not ask for"):
        use(context)


def test_cluster_read_paths_are_what_the_host_lends() -> None:
    context = make_context("cluster.read")

    assert context.cluster is CLUSTER
    assert context.cluster.LOG_WINDOW_BYTES == ClusterBridge.LOG_WINDOW_BYTES


def test_writes_need_the_write_mode(monkeypatch) -> None:
    called: list = []
    monkeypatch.setattr(
        "kubescope.writes.scale_deployment", lambda *a: called.append(a)
    )
    context = make_context("cluster.write", write_mode=False)

    with pytest.raises(WriteModeOff):
        context.writes.scale_deployment("dev", "ns", "web", 3)

    assert called == []


def test_writes_run_when_the_write_mode_is_on(monkeypatch) -> None:
    called: list = []
    monkeypatch.setattr(
        "kubescope.writes.scale_deployment", lambda *a: called.append(a)
    )
    context = make_context("cluster.write", write_mode=True)

    context.writes.scale_deployment("dev", "ns", "web", 3)

    assert called == [("dev", "ns", "web", 3)]


def test_context_reads_the_app() -> None:
    host, _, _ = make_host()
    host.commands.register("select_context", lambda name: name.upper())
    context = ExtensionContext("dco.test", frozenset(), host)

    assert context.current_context == "dev"
    assert context.snapshot() == "the overview"
    assert context.invoke("select_context", name="prod") == "PROD"


def test_settings_are_kept_apart_per_extension_and_saved() -> None:
    host, stores, saved = make_host()
    mine = ExtensionContext("dco.a", frozenset(), host)
    other = ExtensionContext("dco.b", frozenset(), host)

    mine.settings.set("model", "x")

    assert mine.settings.get("model") == "x"
    assert mine.settings.get("missing", "fallback") == "fallback"
    assert other.settings.get("model") is None
    assert stores == {"dco.a": {"model": "x"}, "dco.b": {}}
    assert saved == [True]


def test_settings_refuse_what_the_file_cannot_hold() -> None:
    context = make_context()

    with pytest.raises(TypeError):
        context.settings.set("bad", object())


def test_an_extension_hears_the_events_until_it_is_closed() -> None:
    host, _, _ = make_host()
    context = ExtensionContext("dco.test", frozenset({"ui.dock"}), host)
    heard: list[str] = []
    context.events.on(CONTEXT_CHANGED, lambda context: heard.append(context))
    context.add_dock("chat", object)

    host.events.emit(CONTEXT_CHANGED, context="a")
    context.close()
    host.events.emit(CONTEXT_CHANGED, context="b")

    assert heard == ["a"]
    assert host.contributions.docks == []


class FakeUi:
    window = "the window"
    central = "the central widget"

    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def show_message(self, icon, title, text) -> None:
        self.calls.append(("message", icon, title, text))

    def run_action(self, function, on_success, *arguments, on_error=None, quiet=False):
        self.calls.append(("run", function, arguments, quiet))

    def style_box(self, box) -> None:
        self.calls.append(("style", box))

    def themed(self, color, text=False) -> str:
        return color

    def show_settings(self, section="") -> None:
        self.calls.append(("settings", section))

    def reserve_corner(self, owner, pixels) -> None:
        self.calls.append(("corner", owner, pixels))

    def pick_item(self, title, label, items):
        return "", False

    def show_json(self, title, document) -> None:
        self.calls.append(("json", title))

    def open_log(self, title, name, read) -> None:
        self.calls.append(("log", title, name))


def test_the_window_is_lent_only_to_an_extension_that_asked_for_it() -> None:
    host, _, _ = make_host()
    host.ui = FakeUi()

    with pytest.raises(PermissionDenied, match="did not ask for ui.window"):
        _ = ExtensionContext("dco.test", frozenset(), host).ui

    ui = ExtensionContext("dco.test", frozenset({"ui.window"}), host).ui
    assert ui is host.ui and ui is not None and ui.window == "the window"


def test_without_a_window_the_ui_is_none() -> None:
    host, _, _ = make_host()

    assert ExtensionContext("dco.test", frozenset({"ui.window"}), host).ui is None


def test_the_app_tells_the_write_mode_and_the_language_as_they_are_now() -> None:
    state = {"write": False, "language": "pt_BR"}
    host, _, _ = make_host()
    host.write_mode = lambda: state["write"]
    host.language = lambda: state["language"]
    app = ExtensionContext("dco.test", frozenset(), host).app

    assert (app.write_mode, app.language) == (False, "pt_BR")
    state.update(write=True, language="de")
    assert (app.write_mode, app.language) == (True, "de")


def test_the_language_is_auto_until_the_app_says_otherwise() -> None:
    host, _, _ = make_host()

    assert ExtensionContext("dco.test", frozenset(), host).app.language == "auto"


def test_an_extension_offers_commands_under_its_own_name_and_they_go_with_it() -> None:
    host, _, _ = make_host()
    context = ExtensionContext("dco.test", frozenset(), host)

    context.register_command("dco.test.apply", lambda value: value * 2)

    assert host.commands.invoke("dco.test.apply", value=2) == 4
    with pytest.raises(CommandError, match="starts with dco.test."):
        context.register_command("open_tab", lambda: None)
    with pytest.raises(CommandError, match="already registered"):
        context.register_command("dco.test.apply", lambda: None)
    context.close()
    assert not host.commands.has("dco.test.apply")


def test_a_shortcut_is_a_contribution_that_goes_with_the_extension() -> None:
    host, _, _ = make_host()
    context = ExtensionContext("dco.test", frozenset({"ui.window"}), host)

    def handler() -> None:
        return None

    context.add_shortcut("dco.test.ask", "Ask", "Ctrl+G", handler)

    [shortcut] = host.contributions.shortcuts
    assert (shortcut.action, shortcut.label, shortcut.default) == (
        "dco.test.ask",
        "Ask",
        "Ctrl+G",
    )
    assert shortcut.handler is handler
    context.close()
    assert host.contributions.shortcuts == []
    with pytest.raises(PermissionDenied):
        ExtensionContext("dco.test", frozenset(), host).add_shortcut(
            "a", "A", "", handler
        )


class FakeCli:
    def choose_context(self, name) -> str:
        return name or "picked"

    def confirm(self, question) -> bool:
        return True


def test_the_terminal_is_lent_only_to_what_asked_for_it_and_only_while_it_runs() -> (
    None
):
    host, _, _ = make_host()
    asked = ExtensionContext("dco.test", frozenset({"cli"}), host)

    with pytest.raises(PermissionDenied, match="did not ask for cli"):
        _ = ExtensionContext("dco.test", frozenset(), host).cli
    assert asked.cli is None  # in the window
    host.cli = FakeCli()
    assert asked.cli is host.cli
    assert asked.cli is not None and asked.cli.choose_context(None) == "picked"


def test_an_extension_has_a_folder_of_its_own() -> None:
    host, _, _ = make_host()
    host.data_directory = lambda extension: Path("/data") / extension

    assert ExtensionContext("dco.a", frozenset(), host).data_directory == Path(
        "/data/dco.a"
    )
    assert ExtensionContext("dco.b", frozenset(), host).data_directory == Path(
        "/data/dco.b"
    )


def test_the_app_names_the_language_it_shows_and_the_ones_it_has() -> None:
    host, _, _ = make_host()
    host.resolved_language = lambda: "pt_BR"
    host.language_name = lambda: "Portuguese"
    host.language_names = lambda: ("English", "Portuguese")
    app = ExtensionContext("dco.test", frozenset(), host).app

    assert (app.resolved_language, app.language_name) == ("pt_BR", "Portuguese")
    assert app.language_names == ("English", "Portuguese")
    assert (
        ExtensionContext("dco.t", frozenset(), make_host()[0]).app.language_name
        == "English"
    )


def test_a_page_added_by_an_extension_keeps_what_the_refresh_button_does() -> None:
    host, _, _ = make_host()
    context = ExtensionContext("dco.a", frozenset({"ui.page"}), host)
    called: list[int] = []

    context.add_page(
        "AWS", "RDS", "Instances", object, refresh=lambda: called.append(1)
    )

    [page] = host.contributions.pages
    assert page.refresh is not None
    page.refresh()
    assert called == [1]


def test_an_extension_searches_the_resources_through_the_cluster_bridge(
    monkeypatch,
) -> None:
    from kubescope.sdk.models import SearchHit

    from kubescope import cluster
    from kubescope.extensions.cluster_access import ClusterBridge

    hits = [SearchHit("Pod", "ns", "api")]
    monkeypatch.setattr(cluster, "search_resources", lambda context: hits)

    assert ClusterBridge().search_resources("prod") == hits
