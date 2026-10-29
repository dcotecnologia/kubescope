"""Run the coding assistant of the person's own system and stream its answer.

The app asks one question and shows the answer as it comes. It holds no
key and never sees the sign-in: the program uses the login the person
already has, and in a Flatpak the host runs it. These are coding agents,
so each one is started in its read-only mode, with no saved session and
from an empty folder, which leaves it unable to change a file or run a
command on the machine. What differs from one program to another, its
options and the shape of its output, is an `Assistant` of its own.
"""

import shutil
import subprocess
import tempfile
from collections.abc import Callable, Generator
from dataclasses import dataclass

from kubescope.utils.errors import first_line
from kubescope.utils.flatpak import host_has, in_flatpak, on_host

SYSTEM_PROMPT = (
    "You help a person read a Kubernetes cluster. You get what they selected "
    "in a Kubernetes client, with every Secret value already hidden. Explain it, "
    "find what is wrong and suggest what to check or change. You cannot run "
    "anything, so give commands and YAML for the person to review and run. "
    "Say so when you are not sure."
)


class AssistantError(Exception):
    """The assistant could not answer; the message says why."""


@dataclass(frozen=True, slots=True)
class Assistant:
    key: str  # what the settings keep
    name: str  # what the person reads
    program: str
    # the options of the program for a read-only answer, from the model and the
    # instructions it follows
    options: Callable[[str | None, str], list[str]]
    # the text a line of its output adds, and the error it reports
    parse_line: Callable[[str], tuple[str, str]]


def is_available(assistant: Assistant) -> bool:
    """Whether the system has the program."""
    if in_flatpak():
        return host_has(assistant.program)
    return shutil.which(assistant.program) is not None


def command(
    assistant: Assistant, model: str | None = None, system: str = SYSTEM_PROMPT
) -> list[str]:
    """The program and the options that keep it from acting on the machine."""
    return on_host([assistant.program, *assistant.options(model, system)])


def ask(
    assistant: Assistant,
    prompt: str,
    model: str | None = None,
    system: str = SYSTEM_PROMPT,
) -> Generator[str]:
    """Send the question and yield the answer in pieces.

    Closing the generator before the end stops the program.
    """
    try:
        process = subprocess.Popen(
            command(assistant, model, system),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=tempfile.gettempdir(),  # no project files for it to read
        )
    except OSError as error:
        raise AssistantError(str(error)) from error
    assert process.stdin is not None and process.stdout is not None
    assert process.stderr is not None
    try:
        try:
            process.stdin.write(prompt)
            process.stdin.close()
        except OSError as error:
            raise AssistantError(str(error)) from error
        for line in process.stdout:
            text, error = assistant.parse_line(line)
            if error:
                raise AssistantError(error)
            if text:
                yield text
        if process.wait() != 0:
            reason = first_line(process.stderr.read())
            raise AssistantError(reason or "The assistant stopped without an answer")
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()
