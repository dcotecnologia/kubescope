"""`kubescope chat`: the conversation with Gabi on the terminal.

It is the chat of the window without the window: the same program
(Claude Code or Codex, started with no tools), the same instructions,
the same reads of the cluster and, with the write mode on, the same
changes, each one confirmed first. What the window would show on screen
does not exist here, so the actions that only move the window are told
to the person and nothing else.
"""

import argparse
import importlib
import sys
from collections.abc import Callable

from kubescope import cluster, integrations
from kubescope.assistant import ASSISTANTS, actions, executor, runner
from kubescope.assistant import installed as installed_assistants
from kubescope.assistant.actions import Invalid, Request
from kubescope.assistant.dispatch import write_call
from kubescope.assistant.history import Entry, History
from kubescope.assistant.knowledge import system_prompt
from kubescope.assistant.runner import COMPANY, NAME, Assistant, AssistantError
from kubescope.assistant.session import ChatSession, Message
from kubescope.cli_cluster import _confirm, _context
from kubescope.cluster import ClusterError
from kubescope.settings import Settings, config_directory
from kubescope.utils import ansi

MAX_FOLLOW_UPS = 5  # reads the assistant may ask for after one question
EXIT_WORDS = ("/exit", "/quit", "exit", "quit")
HELP = (
    "/clear  forget this conversation\n"
    "/exit   leave (Ctrl-D does too)\n"
    "/help   show this"
)
CONSENT = (
    "What you type, and what the assistant reads from the cluster to answer "
    "(resource documents and log lines), are sent to {name}, the program of this "
    "computer, and from it to its service. Secret values are hidden and tokens "
    "and keys are redacted, but other text of a log can still go. Changes to the "
    "cluster are asked of you before they run, and only with the write mode on."
)
_FENCE_OPEN = f"```{actions.FENCE}"


try:  # line editing and the history of what was typed, where the system has it
    importlib.import_module("readline")
    _READLINE = True
except ImportError:  # pragma: no cover - there is no readline on Windows
    _READLINE = False


def _prompt() -> str:
    """The prompt, in color; readline needs the escape codes marked, so it does
    not count them as width."""
    text = ansi.paint("you>", "bold", "green", on=ansi.enabled(sys.stdout))
    if _READLINE and text.startswith("\x1b"):
        text = text.replace("\x1b[1;32m", "\x01\x1b[1;32m\x02").replace(
            "\x1b[0m", "\x01\x1b[0m\x02"
        )
    return text + " "


def _note_style(text: str) -> str:
    return ansi.paint(f"[{_clean(text)}]", "dim", "yellow", on=ansi.enabled(sys.stderr))


def _error(text: str) -> None:
    print(ansi.paint(text, "red", on=ansi.enabled(sys.stderr)), file=sys.stderr)


class _Writer:
    """Prints the answer as it comes: line by line, painted, on a terminal; as
    it is, piece by piece, anywhere else."""

    def __init__(self) -> None:
        self.on = ansi.enabled(sys.stdout)
        self.markdown = ansi.Markdown(self.on)
        self.pending = ""
        if self.on:
            print(ansi.paint(NAME, "bold", "magenta"))

    def write(self, text: str) -> None:
        text = _clean(text)
        if not self.on:
            print(text, end="", flush=True)
            return
        self.pending += text
        *lines, self.pending = self.pending.split("\n")
        for line in lines:
            print(self.markdown.line(line), flush=True)

    def finish(self) -> None:
        if self.on:
            print(self.markdown.line(self.pending) if self.pending else "")
        else:
            print()


def _clean(text: str) -> str:
    """Text for the terminal, without the escape character a program could use
    to move or paint it."""
    return text.replace("\x1b", "")


def _sync_choices(settings: Settings) -> None:
    """Tell the runner the program, the model and the effort of each assistant:

    the ones in the settings, or else the ones its program is set to
    use.
    """
    runner.CUSTOM_PROGRAMS.clear()
    runner.CUSTOM_PROGRAMS.update(settings.assistant_programs)
    runner.CUSTOM_MODELS.clear()
    runner.CUSTOM_EFFORTS.clear()
    for one in ASSISTANTS.values():
        model, effort = one.defaults() if one.defaults else ("", "")
        model = settings.assistant_models.get(one.key, model)
        effort = settings.assistant_efforts.get(one.key, effort)
        if model:
            runner.CUSTOM_MODELS[one.key] = model
        if effort:
            runner.CUSTOM_EFFORTS[one.key] = effort


def _choose(settings: Settings, wanted: str | None) -> Assistant:
    found = installed_assistants()
    if not found:
        names = " or ".join(one.name for one in ASSISTANTS.values())
        raise ClusterError(f"The assistant needs {names} installed and signed in")
    key = wanted or settings.assistant
    chosen = next((one for one in found if one.key == key), None)
    if wanted and chosen is None:
        raise ClusterError(f"{wanted} is not installed")
    return chosen or found[0]


def _consent(settings: Settings, assistant: Assistant) -> None:
    """Ask once whether what the assistant is told may leave this computer."""
    if settings.assistant_consent:
        return
    if not sys.stdin.isatty():
        raise ClusterError(
            "Run `kubescope chat` once on a terminal to agree to what the "
            "assistant sends"
        )
    print(CONSENT.format(name=assistant.name), file=sys.stderr)
    if not _confirm("Use the assistant?", False):
        raise ClusterError("The assistant was not allowed")
    settings.assistant_consent = True
    try:
        settings.save()
    except OSError as error:
        print(f"Could not save the settings: {error.strerror}", file=sys.stderr)


def _language(settings: Settings) -> str:
    try:
        from kubescope.i18n import language_name

        return language_name(settings.language)
    except Exception:  # the language is a courtesy; English is always right
        return "English"


class Chat:
    def __init__(
        self,
        session: ChatSession,
        context: str,
        write_mode: bool,
        history: History,
        read: Callable[[Request, str], str] = executor.fetch,
    ) -> None:
        self.session = session
        self.context = context
        self.write_mode = write_mode
        self.history = history
        self.read = read
        self.entries: list[Entry] = history.entries(context)
        for role, text in self.entries:
            if role in ("user", "assistant"):
                session.messages.append(Message(role, text))  # type: ignore[arg-type]

    def keep(self) -> None:
        self.history.set(self.context, self.entries)

    def clear(self) -> None:
        self.session.messages.clear()
        self.entries.clear()
        self.history.clear(self.context)

    def note(self, text: str) -> None:
        print(_note_style(text), file=sys.stderr)
        self.entries.append(("app", text))

    def say(self, text: str, shown: str, role: str = "user") -> str | None:
        """Send a message and print the answer as it comes; None when it
        failed, else the answer with its action blocks."""
        self.entries.append((role, shown))
        printed = 0
        answer = ""
        writer = _Writer()
        try:
            for piece in self.session.send(text):
                answer += piece
                visible = self._visible(answer, final=False)
                writer.write(visible[printed:])
                printed = len(visible)
        except AssistantError as error:
            self.entries.pop()
            print(file=sys.stderr)
            _error(f"The assistant could not answer: {error}")
            return None
        visible = self._visible(answer, final=True)
        writer.write(visible[printed:])
        writer.finish()
        self.entries.append(("assistant", actions.strip(answer)))
        return answer

    @staticmethod
    def _visible(answer: str, final: bool) -> str:
        """The part of the answer to show: without its action blocks, and,
        while it still comes, without the start of a block that is not closed
        yet."""
        text = actions.strip(answer)
        cut = text.find(_FENCE_OPEN)
        if cut >= 0:
            text = text[:cut]
        if not final:
            for size in range(len(_FENCE_OPEN) - 1, 0, -1):
                if text.endswith(_FENCE_OPEN[:size]):
                    return text[:-size]
        return text.rstrip() if final else text

    def ask(self, question: str) -> None:
        """One question and everything it sets off: reads the assistant asked
        for, and changes the person confirms."""
        text, shown, role = question, question, "user"
        for _ in range(MAX_FOLLOW_UPS + 1):
            answer = self.say(text, shown, role)
            if answer is None:
                return
            reads = self._act_on(answer)
            if not reads:
                break
            request = reads[0]
            text = self.read(request, self.context)
            shown, role = f"(read) {actions.describe(request)}", "app"
            print(_note_style(shown), file=sys.stderr)
        else:
            self.note("Stopped reading: too many reads for one question.")
        self.keep()

    def _act_on(self, answer: str) -> list[Request]:
        reads: list[Request] = []
        for found in actions.parse(answer):
            if isinstance(found, Invalid):
                self.note(f"Ignored an action: {found.reason}")
            elif found.action.kind == "navigate":
                self.note(
                    f"{NAME} suggested {actions.describe(found)} in the window; "
                    "that has no meaning on the command line."
                )
            elif found.action.kind == "write" and not self.write_mode:
                self.note(
                    "Read-only mode: nothing was changed. Turn on the write mode "
                    f"in Settings to allow {actions.describe(found)}."
                )
            elif found.action.kind == "write":
                self._write(found)
            else:
                reads.append(found)
        return reads

    def _write(self, request: Request) -> None:
        what = actions.describe(request)
        if not sys.stdin.isatty():
            self.note(f"Cannot confirm {what} without a terminal; nothing was changed")
            return
        try:
            if not _confirm(f"Run {what} on {self.context}?", False):
                self.note(f"Cancelled {what}")
                return
            function, arguments = write_call(request, self.context)
            function(*arguments)
        except (ClusterError, ValueError) as error:
            self.note(f"Could not run {what}: {error}")
            return
        self.note(f"Ran {what}")


def _loop(chat: Chat) -> int:
    on = ansi.enabled(sys.stderr)
    print(
        f"Hi, I'm {ansi.paint(NAME, 'bold', 'magenta', on=on)}, from {COMPANY}. "
        f"Ask me about {ansi.paint(chat.context, 'cyan', on=on)}.\n"
        + ansi.paint("/help lists the commands.", "dim", on=on),
        file=sys.stderr,
    )
    while True:
        try:
            line = input(_prompt()).strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            continue
        if not line:
            continue
        if line in EXIT_WORDS:
            return 0
        if line == "/help":
            print(HELP)
        elif line == "/clear":
            chat.clear()
            print("Forgotten", file=sys.stderr)
        else:
            try:
                chat.ask(line)
            except KeyboardInterrupt:
                print("\n" + _note_style("stopped"), file=sys.stderr)
            print()


def run(namespace: argparse.Namespace) -> int:
    try:
        settings = Settings()
        if not settings.assistant_enabled:
            raise ClusterError("The assistant is off; turn it on in Settings")
        _sync_choices(settings)
        assistant = _choose(settings, namespace.assistant)
        _consent(settings, assistant)
        integrations.load(settings.integration_accounts)
        cluster.configure(
            settings.kubeconfig_files,
            settings.sign_in_commands,
            integrations.kubeconfig_files(),
        )
        context = _context(namespace.context)
        session = ChatSession(
            assistant,
            system=system_prompt(_language(settings), settings.write_mode),
        )
        chat = Chat(
            session,
            context,
            settings.write_mode,
            History(config_directory() / "assistant_history.json"),
        )
        if namespace.message:
            chat.ask(" ".join(namespace.message))
            return 0
        return _loop(chat)
    except (ClusterError, ValueError) as error:
        _error(str(error))
        return 1
    except KeyboardInterrupt, EOFError:
        print(file=sys.stderr)
        return 130


def add_command(commands: argparse._SubParsersAction) -> None:
    for name in ("chat", "assistant"):
        parser = commands.add_parser(
            name,
            help=f"talk to {NAME}, the assistant, about a cluster"
            + (" (same as chat)" if name == "assistant" else ""),
        )
        parser.add_argument(
            "--context", metavar="NAME", help="the kubeconfig context (asked if absent)"
        )
        parser.add_argument(
            "--assistant",
            choices=tuple(ASSISTANTS),
            help="the program to ask (default: the one of Settings)",
        )
        parser.add_argument(
            "message",
            nargs="*",
            help="ask this once and leave, instead of opening the conversation",
        )
