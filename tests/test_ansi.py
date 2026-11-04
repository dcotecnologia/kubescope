import io
import sys

import pytest

from kubescope.utils import ansi


class Terminal(io.StringIO):
    def isatty(self):
        return True


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    for name in ("NO_COLOR", "FORCE_COLOR", "TERM", "WT_SESSION"):
        monkeypatch.delenv(name, raising=False)


def test_a_terminal_gets_colors():
    assert ansi.enabled(Terminal()) is True


def test_a_pipe_gets_none():
    assert ansi.enabled(io.StringIO()) is False


def test_no_color_and_a_dumb_terminal_turn_them_off(monkeypatch):
    monkeypatch.setenv("TERM", "dumb")
    assert ansi.enabled(Terminal()) is False
    monkeypatch.delenv("TERM")
    monkeypatch.setenv("NO_COLOR", "1")
    assert ansi.enabled(Terminal()) is False


def test_force_color_turns_them_on(monkeypatch):
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert ansi.enabled(io.StringIO()) is True


def test_the_default_stream_is_stdout(monkeypatch):
    monkeypatch.setattr(sys, "stdout", Terminal())
    assert ansi.enabled() is True
    monkeypatch.setattr(sys, "stdout", None)
    assert ansi.enabled() is False


def test_windows_needs_a_terminal_that_knows_them(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    assert ansi.enabled(Terminal()) is False
    monkeypatch.setenv("WT_SESSION", "x")
    assert ansi.enabled(Terminal()) is True


def test_paint():
    assert ansi.paint("x", "bold", "red") == "\x1b[1;31mx\x1b[0m"
    assert ansi.paint("x", "bold", on=False) == "x"
    assert ansi.paint("", "bold") == ""
    assert ansi.paint("x") == "x"


def test_markdown_off_leaves_the_text():
    assert ansi.Markdown(False).line("**x** `y`") == "**x** `y`"


def test_markdown_inline_and_blocks():
    markdown = ansi.Markdown()
    assert markdown.line("a **b** `c`") == "a \x1b[1mb\x1b[0m \x1b[36mc\x1b[0m"
    assert "Title" in markdown.line("## Title") and "\x1b[1;35m" in markdown.line("# T")
    assert "•" in markdown.line("  - item") and "•" in markdown.line("* item")
    assert markdown.line("1. keep") == "1. keep"
    assert "yaml" in markdown.line("```yaml") and markdown.in_code
    assert "kind: Pod" in markdown.line("kind: Pod") and "**" in markdown.line("**x**")
    assert "└" in markdown.line("```") and not markdown.in_code
    assert "┌" in markdown.line("```")
