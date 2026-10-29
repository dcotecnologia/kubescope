import json

from kubescope import assistant
from kubescope.assistant import codex, runner


def test_codex_runs_with_nothing_it_could_act_on_the_machine_with() -> None:
    arguments = runner.command(codex.CODEX)

    assert arguments[:2] == ["codex", "exec"]
    assert "--ephemeral" in arguments and "--ignore-user-config" in arguments
    assert arguments[arguments.index("--sandbox") + 1] == "read-only"
    assert "-m" not in arguments
    switched_off = {
        arguments[index + 1].split("=")[0]
        for index, value in enumerate(arguments)
        if value == "-c"
    }
    assert "features.shell_tool" in switched_off  # it cannot run a command
    assert "features.view_image" in switched_off  # nor look at a file of the disk
    assert 'web_search="disabled"' in arguments
    assert all(
        arguments[index + 1].endswith(("=false", '"disabled"'))
        for index, value in enumerate(arguments)
        if value == "-c"
    )
    assert runner.command(codex.CODEX, "big")[-2:] == ["-m", "big"]


def test_the_instructions_go_before_the_conversation() -> None:
    assert codex.compose("be brief", "User: hi") == (
        "[Instructions]\nbe brief\n\n[Conversation]\nUser: hi"
    )


def test_images_are_given_as_files() -> None:
    assert codex.image_files(["/a/1.png", "/a/2.png"]) == [
        "--image",
        "/a/1.png",
        "--image",
        "/a/2.png",
    ]
    assert codex.CODEX.takes_images and codex.CODEX.image_options is None


def test_a_line_gives_the_message_of_the_agent_or_the_error_of_the_turn() -> None:
    message = json.dumps(
        {"type": "item.completed", "item": {"type": "agent_message", "text": "ok"}}
    )
    assert codex.parse_line(message) == ("ok\n\n", "")

    failed = json.dumps({"type": "turn.failed", "error": {"message": "Not logged in"}})
    assert codex.parse_line(failed) == ("", "Not logged in")
    unknown = json.dumps({"type": "turn.failed", "error": {}})
    assert codex.parse_line(unknown) == ("", "The assistant failed")


def test_the_other_events_and_notices_add_nothing() -> None:
    notice = json.dumps(
        {"type": "item.completed", "item": {"type": "error", "message": "warning"}}
    )
    command = json.dumps(
        {"type": "item.completed", "item": {"type": "command_execution"}}
    )
    empty = json.dumps(
        {"type": "item.completed", "item": {"type": "agent_message", "text": ""}}
    )
    for line in (
        "Reading prompt from stdin...\n",
        "[1]\n",
        notice,
        command,
        empty,
        '{"type": "turn.started"}',
        '{"type": "item.completed", "item": {"type": "agent_message", "text": 3}}',
    ):
        assert codex.parse_line(line) == ("", "")


def test_codex_is_one_of_the_assistants_to_choose_from(monkeypatch) -> None:
    assert assistant.ASSISTANTS["codex"] is codex.CODEX

    monkeypatch.setattr(assistant, "is_available", lambda one: one.key == "codex")
    assert assistant.installed() == [codex.CODEX]
