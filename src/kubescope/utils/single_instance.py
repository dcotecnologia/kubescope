import getpass

from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QLocalServer, QLocalSocket

CONNECT_TIMEOUT_MS = 500


def server_name() -> str:
    """One name for each person on the machine, so two accounts can each run
    the app."""
    return f"kubescope-{getpass.getuser()}"


class SingleInstance(QObject):
    """Lets only one KubeScope run for a person: a second start asks the first
    to come forward and quits."""

    activated = Signal()  # another start asked this one to come forward

    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self.name = name or server_name()
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self._asked)

    def notify_running(self) -> bool:
        """Whether another instance is running; when it is, it is told to come
        forward."""
        socket = QLocalSocket()
        socket.connectToServer(self.name)
        if not socket.waitForConnected(CONNECT_TIMEOUT_MS):
            return False
        socket.write(b"show")
        socket.flush()
        socket.waitForBytesWritten(CONNECT_TIMEOUT_MS)
        socket.disconnectFromServer()
        return True

    def listen(self) -> bool:
        """Start answering other starts; a name left behind by a crash is taken
        over."""
        QLocalServer.removeServer(self.name)
        return self.server.listen(self.name)

    def _asked(self) -> None:
        while (socket := self.server.nextPendingConnection()) is not None:
            socket.close()
            socket.deleteLater()
            self.activated.emit()
