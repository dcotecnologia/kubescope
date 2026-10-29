import json

from kubescope import assistant
from kubescope.assistant import claude, runner


def _delta(text: str) -> str:
    event = {
        "type": "content_block_delta",
        "delta": {"type": "text_delta", "text": text},
    }
    return json.dumps({"type": "stream_event", "event": event}) + "\n"


def test_claude_runs_with_nothing_it_could_act_on_the_machine_with() -> None:
    options = runner.command(claude.CLAUDE)

    assert options[:2] == ["claude", "-p"]
    assert options[options.index("--tools") + 1] == ""
    assert "--no-session-persistence" in options
    assert options[options.index("--system-prompt") + 1] == runner.SYSTEM_PROMPT
    assert "--model" not in options
    assert runner.command(claude.CLAUDE, "opus")[-2:] == ["--model", "opus"]


def test_a_line_gives_its_text_or_its_error() -> None:
    assert claude.parse_line(_delta("hi")) == ("hi", "")
    assert claude.parse_line("not json\n") == ("", "")
    assert claude.parse_line("[1]\n") == ("", "")
    assert claude.parse_line('{"type": "system"}\n') == ("", "")
    assert claude.parse_line('{"event": {"delta": {"text": 3}}}\n') == ("", "")
    failed = json.dumps({"type": "result", "is_error": True, "result": "Not logged in"})
    assert claude.parse_line(failed) == ("", "Not logged in")
    unknown = json.dumps({"type": "result", "is_error": True})
    assert claude.parse_line(unknown) == ("", "The assistant failed")
    done = json.dumps({"type": "result", "is_error": False, "result": "ok"})
    assert claude.parse_line(done) == ("", "")


def test_the_installed_assistants_are_the_known_ones_the_system_has(
    monkeypatch,
) -> None:
    assert assistant.ASSISTANTS["claude"] is claude.CLAUDE

    monkeypatch.setattr(assistant, "is_available", lambda one: one.key == "claude")
    assert assistant.installed() == [claude.CLAUDE]
    monkeypatch.setattr(assistant, "is_available", lambda one: False)
    assert assistant.installed() == []
