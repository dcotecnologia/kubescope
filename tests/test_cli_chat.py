import sys
from typing import cast

import pytest

from kubescope import cli, cli_chat, cluster, writes
from kubescope.assistant import runner
from kubescope.assistant.actions import FENCE
from kubescope.assistant.history import History
from kubescope.assistant.runner import Assistant, AssistantError
from kubescope.assistant.session import ChatSession
from kubescope.cluster import ClusterError
from kubescope.settings import Settings


class FakeSettings:
    assistant_enabled = True
    assistant_consent = True
    assistant = ""
    write_mode = False
    language = "auto"
    kubeconfig_files: list[str] = []
    sign_in_commands: dict[str, str] = {}
    assistant_programs: dict[str, str] = {}
    assistant_models: dict[str, str] = {}
    assistant_efforts: dict[str, str] = {}
    saved = 0

    def save(self):
        FakeSettings.saved += 1


def _fake() -> Settings:
    return cast(Settings, FakeSettings())


def _assistant(key="claude", defaults=None):
    return Assistant(
        key, key.title(), key, lambda m, s: [], lambda line: ("", ""), defaults=defaults
    )


class Brain:
    """Stands in for the program: answers each question with the next reply."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts = []

    def __call__(self, assistant, prompt, model, system, images):
        self.prompts.append(prompt)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        yield from reply


def block(**fields):
    import json

    return f"```{FENCE}\n{json.dumps(fields)}\n```\n"


@pytest.fixture(autouse=True)
def world(monkeypatch, tmp_path):
    FakeSettings.assistant_enabled = True
    FakeSettings.assistant_consent = True
    FakeSettings.assistant = ""
    FakeSettings.write_mode = False
    FakeSettings.saved = 0
    monkeypatch.setattr(cli_chat, "Settings", FakeSettings)
    monkeypatch.setattr(cli_chat, "config_directory", lambda: tmp_path)
    monkeypatch.setattr(cluster, "configure", lambda *_: None)
    monkeypatch.setattr(cluster, "list_contexts", lambda: (["a"], "a"))
    monkeypatch.setattr(cli_chat, "installed_assistants", lambda: [_assistant()])
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    yield
    runner.CUSTOM_PROGRAMS.clear()
    runner.CUSTOM_MODELS.clear()
    runner.CUSTOM_EFFORTS.clear()


def _brain(monkeypatch, *replies):
    brain = Brain(*replies)
    monkeypatch.setattr(runner, "ask", brain)
    return brain


def _typed(monkeypatch, *lines):
    given = iter(lines)

    def read(_prompt):
        line = next(given)
        if isinstance(line, BaseException):
            raise line
        return line

    monkeypatch.setattr("builtins.input", read)


def _chat(tmp_path, write_mode=False, read=None):
    session = ChatSession(_assistant())
    chat = cli_chat.Chat(
        session, "a", write_mode, History(tmp_path / "h.json"), read or (lambda *_: "R")
    )
    return chat


def test_one_shot_message(monkeypatch, capsys):
    brain = _brain(monkeypatch, ["Hello ", "there"])
    assert cli.run(["chat", "--context", "a", "how", "are", "you"]) == 0
    assert capsys.readouterr().out == "Hello there\n"
    assert "User: how are you" in brain.prompts[0]


def test_assistant_is_an_alias(monkeypatch, capsys):
    _brain(monkeypatch, ["hi"])
    assert cli.run(["assistant", "--context", "a", "hey"]) == 0
    assert "hi" in capsys.readouterr().out


def test_the_conversation(monkeypatch, capsys, tmp_path):
    _brain(monkeypatch, ["one"], ["two"])
    _typed(monkeypatch, "", "/help", "q1", KeyboardInterrupt(), "/clear", "q2", "/exit")
    assert cli.run(["chat", "--context", "a"]) == 0
    captured = capsys.readouterr()
    assert "/clear" in captured.out and "one" in captured.out and "two" in captured.out
    assert "Forgotten" in captured.err and "Hi, I'm Gabi" in captured.err


def test_the_conversation_ends_with_ctrl_d(monkeypatch):
    _typed(monkeypatch, EOFError())
    assert cli.run(["chat", "--context", "a"]) == 0


def test_the_conversation_is_resumed(monkeypatch, tmp_path):
    History(tmp_path / "assistant_history.json").set(
        "a", [("user", "before"), ("assistant", "yes"), ("app", "note")]
    )
    brain = _brain(monkeypatch, ["ok"])
    assert cli.run(["chat", "--context", "a", "now"]) == 0
    assert "User: before" in brain.prompts[0] and "App" not in brain.prompts[0]
    kept = History(tmp_path / "assistant_history.json").entries("a")
    assert kept[-2:] == [("user", "now"), ("assistant", "ok")]


def test_stopping_an_answer(monkeypatch, capsys):
    def stop(*_):
        raise KeyboardInterrupt
        yield

    monkeypatch.setattr(runner, "ask", stop)
    _typed(monkeypatch, "q", "/exit")
    assert cli.run(["chat", "--context", "a"]) == 0
    assert "[stopped]" in capsys.readouterr().err


def test_a_failed_answer(monkeypatch, capsys, tmp_path):
    _brain(monkeypatch, AssistantError("no sign in"))
    assert cli.run(["chat", "--context", "a", "q"]) == 0
    assert "could not answer: no sign in" in capsys.readouterr().err
    assert History(tmp_path / "assistant_history.json").entries("a") == []


def test_the_assistant_is_off(capsys):
    FakeSettings.assistant_enabled = False
    assert cli.run(["chat", "--context", "a", "q"]) == 1
    assert "assistant is off" in capsys.readouterr().err


def test_no_program_installed(monkeypatch, capsys):
    monkeypatch.setattr(cli_chat, "installed_assistants", lambda: [])
    assert cli.run(["chat", "--context", "a", "q"]) == 1
    assert "installed and signed in" in capsys.readouterr().err


def test_choosing_the_program(monkeypatch, capsys):
    both = [_assistant("claude"), _assistant("codex")]
    monkeypatch.setattr(cli_chat, "installed_assistants", lambda: both)
    settings = _fake()
    assert cli_chat._choose(settings, None).key == "claude"
    assert cli_chat._choose(settings, "codex").key == "codex"
    FakeSettings.assistant = "codex"
    assert cli_chat._choose(settings, None).key == "codex"
    FakeSettings.assistant = "gone"
    assert cli_chat._choose(settings, None).key == "claude"
    monkeypatch.setattr(cli_chat, "installed_assistants", lambda: both[:1])
    with pytest.raises(ClusterError, match="codex is not installed"):
        cli_chat._choose(settings, "codex")


def test_consent_needs_a_terminal(capsys):
    FakeSettings.assistant_consent = False
    assert cli.run(["chat", "--context", "a", "q"]) == 1
    assert "once on a terminal" in capsys.readouterr().err


def test_consent_given_and_refused(monkeypatch, capsys):
    FakeSettings.assistant_consent = False
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(cli_chat, "_confirm", lambda *_: False)
    assert cli.run(["chat", "--context", "a", "q"]) == 1
    assert "not allowed" in capsys.readouterr().err
    monkeypatch.setattr(cli_chat, "_confirm", lambda *_: True)
    settings = _fake()
    cli_chat._consent(settings, _assistant())
    assert settings.assistant_consent is True and FakeSettings.saved == 1


def test_consent_that_cannot_be_saved(monkeypatch, capsys):
    FakeSettings.assistant_consent = False
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(cli_chat, "_confirm", lambda *_: True)

    def fail(self):
        raise OSError(13, "denied")

    monkeypatch.setattr(FakeSettings, "save", fail)
    cli_chat._consent(_fake(), _assistant())
    assert "Could not save the settings" in capsys.readouterr().err


def test_no_context_without_terminal(capsys):
    assert cli.run(["chat", "q"]) == 1
    assert "Pass --context" in capsys.readouterr().err


def test_interrupted_at_the_start(monkeypatch):
    def stop(*_):
        raise KeyboardInterrupt

    monkeypatch.setattr(cli_chat, "_context", stop)
    assert cli.run(["chat"]) == 130


def test_the_choices_of_the_program_are_given_to_the_runner():
    FakeSettings.assistant_programs = {"claude": "/x/claude"}
    FakeSettings.assistant_models = {"claude": "big"}
    FakeSettings.assistant_efforts = {}
    cli_chat._sync_choices(_fake())
    assert runner.CUSTOM_PROGRAMS == {"claude": "/x/claude"}
    assert runner.CUSTOM_MODELS["claude"] == "big"
    FakeSettings.assistant_programs = {}
    FakeSettings.assistant_models = {}


def test_the_defaults_of_the_program(monkeypatch):
    one = _assistant("claude", defaults=lambda: ("small", "high"))
    monkeypatch.setattr(cli_chat, "ASSISTANTS", {"claude": one})
    cli_chat._sync_choices(_fake())
    assert runner.CUSTOM_MODELS == {"claude": "small"}
    assert runner.CUSTOM_EFFORTS == {"claude": "high"}


def test_the_language_falls_back_to_english(monkeypatch):
    assert cli_chat._language(_fake())
    monkeypatch.setattr(
        "kubescope.i18n.language_name", lambda _c: (_ for _ in ()).throw(KeyError)
    )
    assert cli_chat._language(_fake()) == "English"


def test_the_action_blocks_are_not_shown(monkeypatch, capsys):
    _brain(
        monkeypatch,
        ["Look ", "```kubescope", "-action\n", '{"action": "bad"}\n', "```\n", "done"],
    )
    assert cli.run(["chat", "--context", "a", "q"]) == 0
    captured = capsys.readouterr()
    assert captured.out.split() == ["Look", "done"]
    assert "Ignored an action" in captured.err


def test_an_unclosed_block_is_held_back(tmp_path):
    visible = cli_chat.Chat._visible
    assert visible("Hi ```kubescope-action\n{", final=False) == "Hi "
    assert visible("Hi ``", final=False) == "Hi "
    assert visible("Hi there  ", final=True) == "Hi there"


def test_the_escape_character_never_reaches_the_terminal(monkeypatch, capsys):
    _brain(monkeypatch, ["a\x1b[31mred"])
    cli.run(["chat", "--context", "a", "q"])
    assert "\x1b" not in capsys.readouterr().out


def test_navigation_is_only_told(monkeypatch, capsys):
    _brain(monkeypatch, [block(action="open_view", view="pods")])
    cli.run(["chat", "--context", "a", "q"])
    assert "no meaning on the command line" in capsys.readouterr().err


def test_a_read_goes_back_to_the_assistant(monkeypatch, tmp_path, capsys):
    brain = _brain(
        monkeypatch,
        [block(action="list", view="pods", namespace="ns")],
        ["Found it"],
    )
    reads = []
    chat = _chat(tmp_path, read=lambda request, ctx: reads.append(ctx) or "THE-LIST")
    chat.ask("what runs?")
    assert reads == ["a"] and "THE-LIST" in brain.prompts[1]
    assert "Found it" in capsys.readouterr().out
    assert any(role == "app" for role, _ in chat.entries)


def test_too_many_reads(monkeypatch, tmp_path, capsys):
    reply = [block(action="list", view="pods", namespace="")]
    _brain(monkeypatch, *([reply] * (cli_chat.MAX_FOLLOW_UPS + 1)))
    chat = _chat(tmp_path)
    chat.ask("loop")
    assert "too many reads" in capsys.readouterr().err


def test_a_failed_follow_up_stops(monkeypatch, tmp_path):
    _brain(
        monkeypatch,
        [block(action="list", view="pods", namespace="")],
        AssistantError("gone"),
    )
    chat = _chat(tmp_path)
    chat.ask("q")
    assert [role for role, _ in chat.entries] == ["user", "assistant"]


WRITE = block(action="scale", namespace="ns", name="api", replicas=2)


def test_a_write_in_read_only_mode(monkeypatch, tmp_path, capsys):
    _brain(monkeypatch, [WRITE])
    _chat(tmp_path).ask("scale it")
    assert "Read-only mode" in capsys.readouterr().err


def test_a_write_needs_a_terminal(monkeypatch, tmp_path, capsys):
    _brain(monkeypatch, [WRITE])
    _chat(tmp_path, write_mode=True).ask("scale it")
    assert "without a terminal" in capsys.readouterr().err


def test_a_write_confirmed_cancelled_and_failed(monkeypatch, tmp_path, capsys):
    calls = []
    monkeypatch.setattr(writes, "scale_deployment", lambda *a: calls.append(a))
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    answers = iter([True, False, True])
    monkeypatch.setattr(cli_chat, "_confirm", lambda *_: next(answers))
    _brain(monkeypatch, [WRITE], [WRITE], [WRITE])
    chat = _chat(tmp_path, write_mode=True)
    chat.ask("1")
    assert calls == [("a", "ns", "api", 2)]
    chat.ask("2")
    assert len(calls) == 1

    def refuse(*_):
        raise ClusterError("forbidden")

    monkeypatch.setattr(writes, "scale_deployment", refuse)
    chat.ask("3")
    err = capsys.readouterr().err
    assert "Ran scale" in err and "Cancelled scale" in err and "forbidden" in err


def test_the_answer_is_painted_on_a_terminal(monkeypatch, capsys):
    monkeypatch.setenv("FORCE_COLOR", "1")
    _brain(monkeypatch, ["Use **kubectl**\n- `get`", " pods\ndone"])
    assert cli.run(["chat", "--context", "a", "q"]) == 0
    out = capsys.readouterr().out
    assert "\x1b[1;35mGabi\x1b[0m" in out and "\x1b[1mkubectl\x1b[0m" in out
    assert "•" in out and "done" in out


def test_the_answer_painted_ends_with_its_last_line(monkeypatch, capsys):
    monkeypatch.setenv("FORCE_COLOR", "1")
    _brain(monkeypatch, ["one\n"])
    cli.run(["chat", "--context", "a", "q"])
    assert capsys.readouterr().out.endswith("one\n")


def test_the_prompt_is_painted_for_readline(monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setattr(cli_chat, "_READLINE", True)
    prompt = cli_chat._prompt()
    assert prompt == "\x01\x1b[1;32m\x02you>\x01\x1b[0m\x02 "
    monkeypatch.setattr(cli_chat, "_READLINE", False)
    assert cli_chat._prompt() == "\x1b[1;32myou>\x1b[0m "
    monkeypatch.delenv("FORCE_COLOR")
    assert cli_chat._prompt() == "you> "


def test_the_contexts_are_painted(monkeypatch, capsys):
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _p: "")
    assert cli_chat._context(None) == "a"
    assert "\x1b[32m(current)\x1b[0m" in capsys.readouterr().out
