import logging
from functools import partial

from PySide6.QtCore import QObject, QProcess, QProcessEnvironment, QTimer, Signal

from kubescope import forwards
from kubescope.forwards import FAILED, RUNNING, STARTING, STOPPED, Forward, status_of
from kubescope.utils.flatpak import on_host

logger = logging.getLogger(__name__)

STOP_WAIT_MS = 3000  # what a program has to end before it is killed
READY_MS = 8000  # a program that says nothing for this long is taken as running
WATCH_MS = 2000  # how often a forward found after a restart is looked at


class ForwardRunner(QObject):
    """Starts the forwards the person asks for, follows what each program says
    and stops them on request or when the app quits."""

    changed = Signal()
    failed = Signal(object)  # a forward that ended in an error

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.items: list[Forward] = []
        self._processes: dict[int, QProcess] = {}
        self._count = 0
        self._watch = QTimer(self)
        self._watch.setInterval(WATCH_MS)
        self._watch.timeout.connect(self._look_at_adopted)

    def adopt(self) -> None:
        """Take back the forwards a run before this one left running, so they
        are listed and can be stopped."""
        known = {item.pid for item in self.items}
        for forward in forwards.load():
            if forward.pid in known:
                continue  # already listed
            self._count += 1
            forward.number = self._count
            forward.detail = "started before the app was restarted"
            self.items.append(forward)
        if self.items:
            self._watch.start()
            self.changed.emit()

    def _look_at_adopted(self) -> None:
        for forward in self.items:
            if (
                forward.adopted
                and forward.active
                and not forwards.process_alive(forward.pid)
            ):
                forward.status = STOPPED
                forward.detail = "ended"
                self._keep()
                self.changed.emit()

    def _keep(self) -> None:
        forwards.save(self.items)

    def start(
        self,
        title: str,
        kind: str,
        command: list[str],
        env: dict[str, str],
        local: int,
        target: str,
    ) -> Forward:
        self._count += 1
        forward = Forward(self._count, title, kind, command, env, local, target)
        self.items.append(forward)
        process = QProcess(self)
        self._processes[forward.number] = process
        merged = QProcessEnvironment.systemEnvironment()
        for name, value in env.items():
            merged.insert(name, value)
        process.setProcessEnvironment(merged)
        process.readyReadStandardOutput.connect(partial(self._read, forward, False))
        process.readyReadStandardError.connect(partial(self._read, forward, True))
        process.finished.connect(partial(self._finished, forward))
        process.errorOccurred.connect(partial(self._error, forward))
        process.started.connect(partial(self._started, forward))
        program, *arguments = on_host(command, env)
        logger.info("Forward %d: starting %s", forward.number, command[0])
        process.start(program, arguments)
        QTimer.singleShot(READY_MS, self, partial(self._assume_running, forward))
        self.changed.emit()
        return forward

    def _started(self, forward: Forward) -> None:
        process = self._processes.get(forward.number)
        if process is not None:
            forward.pid = process.processId()
            self._keep()

    def _read(self, forward: Forward, errors: bool) -> None:
        process = self._processes.get(forward.number)
        if process is None:
            return
        data = (
            process.readAllStandardError()
            if errors
            else process.readAllStandardOutput()
        )
        for line in bytes(data.data()).decode("utf-8", "replace").splitlines():
            text = line.strip()
            if not text:
                continue
            forward.detail = text
            if forward.status == STARTING and (state := status_of(forward.kind, text)):
                forward.status = state
        self.changed.emit()

    def _assume_running(self, forward: Forward) -> None:
        if forward.status == STARTING:
            forward.status = RUNNING  # no news is the program still listening
            self.changed.emit()

    def _finished(
        self, forward: Forward, code: int, _status: QProcess.ExitStatus
    ) -> None:
        if forward.status != STOPPED:
            forward.status = FAILED if code else STOPPED
            if code and not forward.detail:
                forward.detail = f"exit code {code}"
        self._processes.pop(forward.number, None)
        self._keep()
        self.changed.emit()
        if forward.status == FAILED:
            self.failed.emit(forward)

    def _error(self, forward: Forward, error: QProcess.ProcessError) -> None:
        if error == QProcess.ProcessError.FailedToStart:
            forward.status = FAILED
            forward.detail = f"could not start {forward.command[0]}"
            self._processes.pop(forward.number, None)
            self._keep()
            self.changed.emit()
            self.failed.emit(forward)

    def stop(self, forward: Forward) -> None:
        """Ask the program to end, and kill it if it does not."""
        if not forward.active:
            return
        process = self._processes.get(forward.number)
        forward.status = STOPPED
        forward.detail = ""
        if process is not None:
            process.terminate()
            QTimer.singleShot(STOP_WAIT_MS, self, partial(self._kill, forward))
        elif forward.adopted:  # not started by this run: by its process number
            forwards.terminate(forward.pid)
        self._keep()
        self.changed.emit()

    def _kill(self, forward: Forward) -> None:
        process = self._processes.get(forward.number)
        if process is not None:
            process.kill()

    def stop_all(self) -> None:
        for forward in list(self.items):
            self.stop(forward)

    def wait(self) -> None:
        """Let the programs end, for the app to quit."""
        for process in list(self._processes.values()):
            if not process.waitForFinished(STOP_WAIT_MS):
                process.kill()
                process.waitForFinished(STOP_WAIT_MS)

    def clear_finished(self) -> None:
        self.items = [forward for forward in self.items if forward.active]
        self._keep()
        self.changed.emit()

    def active_count(self) -> int:
        return sum(forward.active for forward in self.items)
