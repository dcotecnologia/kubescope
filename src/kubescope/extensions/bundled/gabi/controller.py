"""The controller of Gabi: the chat, its panel and what it asks of the window.

It opens and closes the chat, keeps its history, tells the assistant
what the window shows and runs what it asks (navigation by the commands
of the window, changes to the cluster only after the person confirmed
them, and only in the write mode). Everything it needs from the app
comes through the `GabiPort`, never from the window itself.
"""

from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QWidget

from kubescope.cluster import describe_kube
from kubescope.extensions.bundled.gabi import ASSISTANTS, runner
from kubescope.extensions.bundled.gabi import actions as assistant_actions
from kubescope.extensions.bundled.gabi import installed as installed_assistants
from kubescope.extensions.bundled.gabi.dispatch import write_call
from kubescope.extensions.bundled.gabi.history import History
from kubescope.extensions.bundled.gabi.knowledge import system_prompt
from kubescope.extensions.bundled.gabi.panel import BUBBLE, MARGIN, AssistantDock
from kubescope.extensions.bundled.gabi.runner import NAME, Assistant
from kubescope.extensions.bundled.gabi.runner import (
    is_available as is_available_assistant,
)
from kubescope.extensions.bundled.gabi.session import ChatSession
from kubescope.extensions.bundled.gabi.tab import AssistantTab
from kubescope.extensions.registries import CommandRegistry
from kubescope.i18n import language_name, resolve_language
from kubescope.settings import Settings, config_directory
from kubescope.utils.errors import first_line


@dataclass
class GabiPort:
    """What the app lends to Gabi; every call is looked up when it is made."""

    settings: Settings
    parent: QWidget  # the window: the parent of the boxes it shows
    central: QWidget  # where the panel and the button of the corner sit
    commands: CommandRegistry
    context: Callable[[], str]  # the cluster context the window is on
    screen: Callable[[], str]  # what the window shows, in words
    save_settings: Callable[[], None]
    show_message: Callable[[QMessageBox.Icon, str, str], None]
    run_action: Callable[..., None]  # a function off the UI thread
    style_box: Callable[[QMessageBox], None]  # the window's own buttons
    show_settings: Callable[[], None]  # the Settings, on the section of Gabi
    reserve_corner: Callable[[int], None]  # keep this many pixels of the corner clear


class GabiController(QObject):
    def __init__(self, port: GabiPort) -> None:
        super().__init__(port.parent)
        self.port = port
        runner.CUSTOM_PROGRAMS.clear()
        runner.CUSTOM_PROGRAMS.update(port.settings.assistant_programs)
        self.sync_choices()
        self.history = History(config_directory() / "assistant_history.json")
        self.tab: AssistantTab | None = None
        self._switching = False  # the assistant itself changes the context
        self.dock = AssistantDock(port.central)
        self.dock.bubble.clicked.connect(self.toggle)
        self.dock.panel.closed.connect(self.dock.close)
        self.dock.panel.clear_requested.connect(self.clear_chat)
        self.dock.panel.settings_requested.connect(port.show_settings)
        self.dock.bubble.setVisible(port.settings.assistant_enabled)
        self.make_room()
        self.dock.restore(port.settings.assistant_panel)
        self.dock.state_changed.connect(self._keep_panel)

    def sync_choices(self) -> None:
        """Tell the runner the model and the effort of each assistant: the ones
        in the settings, or else the ones its program is set to use."""
        runner.CUSTOM_MODELS.clear()
        runner.CUSTOM_EFFORTS.clear()
        for one in ASSISTANTS.values():
            model, effort = one.defaults() if one.defaults else ("", "")
            model = self.port.settings.assistant_models.get(one.key, model)
            effort = self.port.settings.assistant_efforts.get(one.key, effort)
            if model:
                runner.CUSTOM_MODELS[one.key] = model
            if effort:
                runner.CUSTOM_EFFORTS[one.key] = effort

    def apply_settings(
        self,
        enabled: bool,
        assistant: str,
        programs: dict[str, str],
        models: dict[str, str],
        efforts: dict[str, str],
    ) -> None:
        """Keep the settings of the assistant and make the window follow
        them."""
        settings = self.port.settings
        settings.assistant_programs = programs
        runner.CUSTOM_PROGRAMS.clear()
        runner.CUSTOM_PROGRAMS.update(programs)
        settings.assistant_models = models
        settings.assistant_efforts = efforts
        self.sync_choices()
        settings.assistant_enabled = enabled
        settings.assistant = assistant
        self.dock.bubble.setVisible(enabled)
        self.make_room()
        if not enabled:
            self.dock.close()
        self.show_engine()

    def restyle(self) -> None:
        """The theme changed."""
        self.dock.restyle()
        if self.tab is not None:
            self.tab.restyle()

    def retranslate(self) -> None:
        """The language changed."""
        self.dock.retranslate()

    def context_changed(self) -> None:
        """The window moved to another context: a chat belongs to one cluster,
        unless the assistant itself moved it."""
        tab = self.tab
        if (
            tab is not None
            and tab.context != self.port.context()
            and not self._switching
        ):
            self.end_chat()
            self.dock.close()

    def shutdown(self) -> None:
        """Stop what the chat runs."""
        if self.tab is not None:
            self.tab.shutdown()

    def program(self) -> Assistant | None:
        """The assistant the person chose, or the first one the system has."""
        found = installed_assistants()
        chosen = next(
            (one for one in found if one.key == self.port.settings.assistant), None
        )
        return chosen or (found[0] if found else None)

    def _consent(self, assistant: Assistant) -> bool:
        """Ask once whether what the assistant is told may leave this
        computer."""
        answer = QMessageBox.question(
            self.port.parent,
            self.tr("Assistant"),
            self.tr(
                "What you type and attach, and what the assistant reads from the "
                "cluster to answer (resource documents and log lines), are sent to "
                "{name}, "
                "the program of this computer, and from it to its service. Secret "
                "values are hidden and tokens and keys are redacted, but other "
                "text of a log can still go. Changes to the cluster are asked of "
                "you before they run, and only with the write mode on.\n\n"
                "Use the assistant?"
            ).format(name=assistant.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return False
        self.port.settings.assistant_consent = True
        self.port.save_settings()
        return True

    def shortcut(self) -> None:
        """Ctrl+G opens the chat and puts the cursor in it; when it is open and
        has the cursor already, it puts it away.

        Nothing happens while the assistant is off in Settings.
        """
        if not self.port.settings.assistant_enabled:
            return
        tab = self.tab
        if self.dock.is_open and tab is not None:
            if tab.input.hasFocus():
                self.dock.close()
                return
        else:
            self.open()
            tab = self.tab
        if tab is not None and self.dock.is_open:
            tab.input.window().activateWindow()  # it may be in a window of its own
            tab.input.setFocus()

    def toggle(self) -> None:
        """The button of the corner: open the chat, or put it away."""
        if self.dock.is_open:
            self.dock.close()
        else:
            self.open()

    def open(self) -> None:
        """Open the chat with the assistant of the system, for this context."""
        assistant = self.program()
        if assistant is None:
            self._guide_setup()
            return
        if not self.port.context():
            self.port.show_message(
                QMessageBox.Icon.Information,
                self.tr("Assistant"),
                self.tr("Choose a context first."),
            )
            return
        if not self.port.settings.assistant_consent and not self._consent(assistant):
            return
        tab = self.tab
        if tab is None:
            session = ChatSession(assistant, system=self._system())
            tab = AssistantTab(
                session,
                self.port.context(),
                lambda: self.port.settings.write_mode,
                screen=self.port.screen,
                history=self.history.entries(self.port.context()),
                takes_images=assistant.takes_images,
            )
            tab.debug_report = self.debug_report
            tab.kube_requested.connect(lambda: self._kube_report(tab))
            tab.changed.connect(lambda: self._keep_chat(tab))
            tab.navigate.connect(lambda request: self._navigate(tab, request))
            tab.write.connect(lambda request: self._write(tab, request))
            self.tab = tab
            self.dock.panel.show_chat(tab)
            self.show_engine()
        self.dock.open()
        tab.input.setFocus()

    def engine(self, assistant: Assistant, model: str | None) -> str:
        """What answers, in words: the program, its model and its effort."""
        chosen = model or runner.CUSTOM_MODELS.get(assistant.key)
        effort = runner.CUSTOM_EFFORTS.get(assistant.key)
        if assistant.effort_options is None:
            effort = None
        return " · ".join(
            (
                assistant.name,
                chosen or self.tr("unknown model"),
                effort or self.tr("unknown effort"),
            )
        )

    def debug_report(self) -> str:
        """What the /debug command says: the program that answers and all of
        its configuration, from the settings and the program itself.

        No credentials are in it, and neither is the long instruction
        sent with each question.
        """
        tab = self.tab
        assert tab is not None
        assistant = tab.session.assistant
        settings = self.port.settings
        default_model, default_effort = (
            assistant.defaults() if assistant.defaults else ("", "")
        )

        def source(chosen: str, default: str) -> str:
            if chosen:
                return f"{chosen} (set in Settings)"
            if default:
                return f"{default} (what {assistant.name} is set to use)"
            return "not told: the program decides"

        arguments = runner.command(assistant, tab.session.model, tab.session.system)
        shown = [
            f"<{len(arguments[index])} characters>"
            if index and arguments[index - 1] == "--system-prompt"
            else argument
            for index, argument in enumerate(arguments)
        ]
        path = runner.program_of(assistant)
        installed = ", ".join(one.name for one in installed_assistants()) or "none"
        efforts = ", ".join(assistant.efforts) or "none"
        models = ", ".join(assistant.models) or "none listed"
        lines = [
            "/debug",
            f"Assistant: {NAME}",
            f"Program: {assistant.name} ({assistant.key})",
            f"Program file: {path}"
            + (" (set in Settings)" if assistant.key in runner.CUSTOM_PROGRAMS else ""),
            f"Chosen in Settings: {settings.assistant or 'automatic, the first found'}",
            f"Installed: {installed}",
            "Model: "
            + source(settings.assistant_models.get(assistant.key, ""), default_model),
            "Effort: "
            + (
                source(
                    settings.assistant_efforts.get(assistant.key, ""), default_effort
                )
                if assistant.effort_options
                else "this program cannot be told"
            ),
            f"Models it lists: {models}",
            f"Efforts it allows: {efforts}",
            f"Takes images: {'yes' if assistant.takes_images else 'no'}",
            f"Write mode: {'on' if settings.write_mode else 'off'}",
            f"Language: {resolve_language(settings.language)}",
            f"Command: {' '.join(shown)}",
        ]
        return "\n".join(lines)

    def _kube_report(self, tab: AssistantTab) -> None:
        """What /kube says, read off the UI thread, and put in the chat."""
        self.port.run_action(
            describe_kube,
            lambda text: tab.note(f"/kube\n{text}"),
            quiet=True,
            on_error=lambda message: tab.note(f"/kube\n{first_line(message)}"),
        )

    def show_engine(self) -> None:
        """Keep the header of the chat telling what answers it."""
        tab = self.tab
        if tab is None:
            return
        found = self.program()
        if found is not None and found is not tab.session.assistant:
            tab.use(found)  # the program chosen in the settings takes over
        self.dock.panel.set_engine(
            self.engine(tab.session.assistant, tab.session.model)
        )

    def _system(self) -> str:
        """What the assistant is told: the language of the app and the mode it
        is in, since with the write mode off it has nothing that changes a
        cluster."""
        return system_prompt(
            language_name(self.port.settings.language), self.port.settings.write_mode
        )

    def refresh_system(self) -> None:
        """Tell the open chat about a change of language or of mode."""
        if self.tab is not None:
            self.tab.session.system = self._system()

    def end_chat(self) -> None:
        """Drop the conversation, stopping what it runs."""
        tab, self.tab = self.tab, None
        self.dock.panel.show_chat(None)
        self.dock.panel.set_engine("")
        if tab is not None:
            tab.shutdown()
            tab.deleteLater()

    def make_room(self) -> None:
        """Keep what is at the right of the footer and of the note under the
        lists clear of the button of the assistant, which sits in that
        corner."""
        gutter = BUBBLE + MARGIN if self.port.settings.assistant_enabled else 0
        self.port.reserve_corner(gutter)

    def _keep_panel(self) -> None:
        """Write down the size and the place of the chat panel."""
        self.port.settings.assistant_panel = self.dock.state()
        self.port.save_settings()

    def _keep_chat(self, tab: AssistantTab) -> None:
        """Write the conversation down, to find it again."""
        self.history.set(tab.context, tab.entries())

    def _forget(self, context: str | None, text: str) -> None:
        """Ask, then forget the conversation of a context, or all of them."""
        answer = QMessageBox.question(
            self.port.parent,
            self.tr("Assistant"),
            text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.end_chat()
        self.history.clear(context)
        if self.dock.is_open:
            self.open()

    def clear_chat(self) -> None:
        """Forget the conversation of this context."""
        self._forget(
            self.port.context(),
            self.tr("Forget the conversation with the assistant in this context?"),
        )

    def clear_history(self) -> None:
        """Forget every conversation, from the settings."""
        self._forget(None, self.tr("Forget every conversation with the assistant?"))

    def _guide_setup(self) -> None:
        """There is no program to run Gabi on: say what to install, offer the
        settings where its place is told, and the instructions."""
        broken = [
            one.name
            for one in ASSISTANTS.values()
            if self.port.settings.assistant_programs.get(one.key)
            and not is_available_assistant(one)
        ]
        steps = self.tr(
            "KubeScope found neither of them on this computer. They are programs "
            "that you install and sign in to yourself, as you would in a terminal; "
            "KubeScope asks for no credentials and stores none.\n\n"
            "1. Install the Claude Code CLI (claude) or the Codex CLI (codex) and sign "
            "in.\n"
            "2. If it is installed where the system does not look, tell KubeScope "
            "where in Settings.\n"
            "3. Open this button again."
        )
        if broken:
            steps += "\n\n" + self.tr(
                "The path set for {names} is not a program that can be run."
            ).format(names=", ".join(broken))
        box = QMessageBox(self.port.parent)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle(NAME)
        box.setText(self.tr("{name} needs Claude Code or Codex.").format(name=NAME))
        box.setInformativeText(steps)
        settings = box.addButton(
            self.tr("Open Settings"), QMessageBox.ButtonRole.AcceptRole
        )
        language = resolve_language(self.port.settings.language)
        for one in ASSISTANTS.values():
            if one.guide is not None:
                address = one.guide(language)
                button = box.addButton(
                    self.tr("{name} guide").format(name=one.name),
                    QMessageBox.ButtonRole.ActionRole,
                )
                button.clicked.connect(
                    lambda _checked=False, url=address: QDesktopServices.openUrl(
                        QUrl(url)
                    )
                )
        box.addButton(self.tr("Close"), QMessageBox.ButtonRole.RejectRole)
        settings.clicked.connect(self.port.show_settings)
        self.port.style_box(box)
        box.exec()

    def _navigate(self, tab: AssistantTab, request: assistant_actions.Request) -> None:
        """Do in the window what the assistant asked, as the person would."""
        name = request.action.name
        if name != "switch_context":
            self.port.commands.invoke(name, report=tab.note, **request.args)
            return
        self._switching = True
        try:
            if self.port.commands.invoke(name, report=tab.note, **request.args):
                tab.context = self.port.context()  # the chat follows
        finally:
            self._switching = False

    def _write(self, tab: AssistantTab, request: assistant_actions.Request) -> None:
        """Run a change the person confirmed on a card of the chat."""
        what = assistant_actions.describe(request)
        if not self.port.settings.write_mode:
            tab.note(
                self.tr("Not run, the write mode is off: {what}").format(what=what)
            )
            return
        function, arguments = write_call(request, tab.context)
        self.port.run_action(
            function,
            lambda _result: tab.note(self.tr("Done: {what}").format(what=what)),
            *arguments,
            on_error=lambda message: tab.note(
                self.tr("Failed: {what}\n{message}").format(what=what, message=message)
            ),
        )
