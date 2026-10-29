"""Run the coding assistant of the person's own system and stream its answer.

The app asks one question and shows the answer as it comes. It holds no
key and never sees the sign-in: the program uses the login the person
already has, and in a Flatpak the host runs it. These are coding agents,
so each one is started in its read-only mode, with no saved session and
from an empty folder, which leaves it unable to change a file or run a
command on the machine. What differs from one program to another, its
options and the shape of its output, is an `Assistant` of its own.
"""

import os
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from kubescope.assistant.attachments import Attachment
from kubescope.utils.errors import first_line
from kubescope.utils.flatpak import host_has, in_flatpak, on_host

NAME = "Gabi"
COMPANY = "DCO Tecnologia"
BORN = date(1992, 6, 6)
HOMETOWN = "São Paulo, Brazil"
SYSTEM_PROMPT = (
    f"Your name is {NAME}. You work for {COMPANY}, the makers of KubeScope, and you "
    "are an expert in Kubernetes and in KubeScope. You are an AI assistant: say "
    f"so if asked, and introduce yourself as {NAME} when someone greets you or "
    "asks who you are. If asked what powers you, say that you use the assistant "
    "program installed on the person's computer, and do not claim to be anything "
    "else. You help a person read a Kubernetes cluster. You get what they selected "
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
    # for a program that takes images: its options for a question that comes
    # with them, and the message to write to it, with the images in it
    image_options: Callable[[str | None, str], list[str]] | None = None
    image_payload: Callable[[str, Sequence[Attachment]], str] | None = None
    # a program with no option for its instructions gets them before the question
    compose: Callable[[str, str], str] | None = None
    # a program that reads images from files: its options for the files
    image_files: Callable[[Sequence[str]], list[str]] | None = None

    @property
    def takes_images(self) -> bool:
        by_message = self.image_options is not None and self.image_payload is not None
        return by_message or self.image_files is not None


# where the person says a program is, by the key of its assistant, for the ones the
# system does not find on its path
CUSTOM_PROGRAMS: dict[str, str] = {}


def program_of(assistant: Assistant) -> str:
    """The program to run: the path the person gave, or the name on the
    path."""
    custom = CUSTOM_PROGRAMS.get(assistant.key)
    return str(Path(custom).expanduser()) if custom else assistant.program


def is_runnable(path: str) -> bool:
    """Whether a path is a file that can be run, on this computer or, in a
    Flatpak, on the host."""
    if in_flatpak():
        return host_has(path)
    return os.path.isfile(path) and os.access(path, os.X_OK)


def is_available(assistant: Assistant) -> bool:
    """Whether the system has the program."""
    program = program_of(assistant)
    if assistant.key in CUSTOM_PROGRAMS:
        return is_runnable(program)
    if in_flatpak():
        return host_has(program)
    return shutil.which(program) is not None


def command(
    assistant: Assistant,
    model: str | None = None,
    system: str = SYSTEM_PROMPT,
    with_images: bool = False,
) -> list[str]:
    """The program and the options that keep it from acting on the machine."""
    options = assistant.image_options if with_images else assistant.options
    assert options is not None
    return on_host([program_of(assistant), *options(model, system)])


def ask(
    assistant: Assistant,
    prompt: str,
    model: str | None = None,
    system: str = SYSTEM_PROMPT,
    images: Sequence[Attachment] = (),
) -> Generator[str]:
    """Send the question, with the images that came with it, and yield the
    answer in pieces.

    Closing the generator before the end stops the program.
    """
    if images and not assistant.takes_images:
        raise AssistantError(f"{assistant.name} does not take images")
    folder = tempfile.TemporaryDirectory() if images and assistant.image_files else None
    try:
        yield from _run(assistant, prompt, model, system, images, folder)
    finally:
        if folder is not None:
            folder.cleanup()


def _run(
    assistant: Assistant,
    prompt: str,
    model: str | None,
    system: str,
    images: Sequence[Attachment],
    folder: tempfile.TemporaryDirectory[str] | None,
) -> Generator[str]:
    """Start the program and read its answer; the images it reads from files
    are written to `folder`."""
    arguments = command(assistant, model, system, bool(images) and folder is None)
    if folder is not None and assistant.image_files is not None:
        paths = []
        for number, image in enumerate(images, start=1):
            path = Path(folder.name) / f"image-{number}{Path(image.name).suffix}"
            path.write_bytes(image.data)
            paths.append(str(path))
        arguments += assistant.image_files(paths)
    try:
        process = subprocess.Popen(
            arguments,
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
            payload = assistant.image_payload
            if images and folder is None and payload is not None:
                text = payload(prompt, images)
            elif assistant.compose is not None:
                text = assistant.compose(system, prompt)
            else:
                text = prompt
            process.stdin.write(text)
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
