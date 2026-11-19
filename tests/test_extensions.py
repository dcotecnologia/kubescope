import logging
from typing import Any

import pytest

from kubescope.extensions.context import ExtensionContext, Host
from kubescope.extensions.registries import CommandRegistry, EventBus
from kubescope.sdk import (
    CONTEXT_CHANGED,
    CommandError,
    DockContribution,
    PermissionDenied,
    WriteModeOff,
)


class FakeCluster:
    def __getattr__(self, name: str):
        return lambda *arguments: (name, arguments)


CLUSTER = FakeCluster()


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
    assert context.cluster.list_pods("dev") == ("list_pods", ("dev",))


def test_writes_need_the_write_mode() -> None:
    context = make_context("cluster.write", write_mode=False)

    with pytest.raises(WriteModeOff):
        context.writes.run(lambda: None)


def test_writes_run_when_the_write_mode_is_on() -> None:
    context = make_context("cluster.write", write_mode=True)

    assert context.writes.run(lambda a, b: a + b, 1, 2) == 3


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
