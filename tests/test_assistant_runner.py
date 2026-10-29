import io
import subprocess

import pytest

from kubescope.assistant import runner
from kubescope.assistant.runner import Assistant, AssistantError


def _parse(line: str) -> tuple[str, str]:
    """A line of the fake program: `text:...` or `error:...`."""
    kind, _, rest = line.rstrip("\n").partition(":")
    if kind == "text":
        return rest, ""
    return ("", rest) if kind == "error" else ("", "")


def _delta(text: str) -> str:
    return f"text:{text}\n"


def _options(model: str | None, system: str) -> list[str]:
    return ["--read-only", f"--system={system}", *(["--model", model] if model else [])]


FAKE = Assistant("fake", "Fake", "fake-ai", _options, _parse)


class Input(io.StringIO):
    """What the program is written to: it keeps what was written, or fails."""

    def __init__(self, error: Exception | None = None) -> None:
        super().__init__()
        self.error = error
        self.written: list[str] = []

    def write(self, text: str) -> int:
        if self.error is not None:
            raise self.error
        self.written.append(text)
        return super().write(text)


class FakeProcess:
    def __init__(
        self, output="", stderr="", code=0, write_error: Exception | None = None
    ) -> None:
        self.stdin = Input(write_error)
        self.stdout = io.StringIO(output)
        self.stderr = io.StringIO(stderr)
        self.code = code
        self.running = True
        self.terminated = False

    def wait(self) -> int:
        self.running = False
        return self.code

    def poll(self):
        return None if self.running else self.code

    def terminate(self) -> None:
        self.terminated = True
        self.running = False


@pytest.fixture
def start(monkeypatch):
    """Make the next process the one given; the arguments it was started with
    are kept in `started`."""
    started: dict = {}

    def install(process) -> dict:
        def popen(arguments, **options):
            started.update(arguments=arguments, **options)
            return process

        monkeypatch.setattr(subprocess, "Popen", popen)
        return started

    return install


def test_the_program_runs_with_the_options_of_its_assistant() -> None:
    assert runner.command(FAKE, None, "be brief") == [
        "fake-ai",
        "--read-only",
        "--system=be brief",
    ]
    assert runner.command(FAKE, "big")[-2:] == ["--model", "big"]


def test_in_a_flatpak_the_host_runs_the_program(monkeypatch) -> None:
    monkeypatch.setattr("kubescope.utils.flatpak.in_flatpak", lambda: True)

    assert runner.command(FAKE)[:3] == ["flatpak-spawn", "--host", "fake-ai"]


def test_the_program_is_found_on_the_system_or_on_the_host(monkeypatch) -> None:
    monkeypatch.setattr(runner.shutil, "which", lambda name: "/bin/" + name)
    assert runner.is_available(FAKE)
    monkeypatch.setattr(runner.shutil, "which", lambda name: None)
    assert not runner.is_available(FAKE)

    monkeypatch.setattr(runner, "in_flatpak", lambda: True)
    monkeypatch.setattr(runner, "host_has", lambda name: name == "fake-ai")
    assert runner.is_available(FAKE)


def test_the_answer_comes_in_pieces_and_the_question_goes_in_by_stdin(start) -> None:
    process = FakeProcess("notice\n" + _delta("Hel") + _delta("lo"))
    started = start(process)

    assert list(runner.ask(FAKE, "why?", "big")) == ["Hel", "lo"]

    assert started["arguments"] == runner.command(FAKE, "big")
    assert process.stdin.closed
    assert not process.terminated


def test_an_error_of_the_program_is_raised(start) -> None:
    process = FakeProcess(_delta("a") + "error:Not logged in\n", code=1)
    start(process)

    pieces = runner.ask(FAKE, "why?")
    assert next(pieces) == "a"
    with pytest.raises(AssistantError, match="Not logged in"):
        next(pieces)
    assert process.terminated


def test_a_program_that_fails_without_an_event_reports_its_stderr(start) -> None:
    start(FakeProcess(stderr="\nboom\nmore\n", code=2))
    with pytest.raises(AssistantError, match="^boom$"):
        list(runner.ask(FAKE, "why?"))

    start(FakeProcess(code=2))
    with pytest.raises(AssistantError, match="without an answer"):
        list(runner.ask(FAKE, "why?"))


def test_a_program_that_cannot_start_or_be_written_to_is_reported(
    monkeypatch, start
) -> None:
    def missing(*_args, **_options):
        raise FileNotFoundError("no fake-ai")

    monkeypatch.setattr(subprocess, "Popen", missing)
    with pytest.raises(AssistantError, match="no fake-ai"):
        list(runner.ask(FAKE, "why?"))

    process = FakeProcess(write_error=BrokenPipeError("closed"))
    start(process)
    with pytest.raises(AssistantError, match="closed"):
        list(runner.ask(FAKE, "why?"))
    assert process.terminated


def test_closing_the_answer_early_stops_the_program(start) -> None:
    process = FakeProcess(_delta("a") + _delta("b"))
    start(process)

    pieces = runner.ask(FAKE, "why?")
    assert next(pieces) == "a"
    pieces.close()

    assert process.terminated


def test_images_go_to_a_program_that_takes_them_as_a_message(start) -> None:
    from kubescope.assistant.attachments import Attachment

    seen: list = []

    def payload(prompt, images) -> str:
        seen.append((prompt, [image.name for image in images]))
        return f"MESSAGE:{prompt}\n"

    takes = Assistant(
        "picky",
        "Picky",
        "picky-ai",
        _options,
        _parse,
        lambda model, system: ["--structured", f"--system={system}"],
        payload,
    )
    image = Attachment("a.png", "image", b"x", "image/png")
    process = FakeProcess(_delta("seen"))
    started = start(process)

    assert list(runner.ask(takes, "look", None, "rules", [image])) == ["seen"]

    assert started["arguments"] == ["picky-ai", "--structured", "--system=rules"]
    assert seen == [("look", ["a.png"])]
    assert process.stdin.written == ["MESSAGE:look\n"]


def test_images_are_refused_by_a_program_that_does_not_take_them(start) -> None:
    from kubescope.assistant.attachments import Attachment

    start(FakeProcess())
    image = Attachment("a.png", "image", b"x", "image/png")

    assert not FAKE.takes_images
    with pytest.raises(AssistantError, match="Fake does not take images"):
        list(runner.ask(FAKE, "look", None, "rules", [image]))
