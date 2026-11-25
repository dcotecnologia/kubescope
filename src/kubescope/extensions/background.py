"""Work an extension runs off the UI thread and hears from on it
(`kubescope.sdk.Components.background`): a function that gives one answer, or a
generator whose pieces come as they are made."""

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QThread, Signal


class Background(QThread):
    """Runs `function` in a thread.

    With `stream`, `function` is a generator and each of its pieces is
    handed over as it comes, until it is `stopped`; the generator is
    closed when it ends, so what it keeps (a program that runs) is
    stopped with it.
    """

    piece = Signal(object)
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, function: Callable[[], Any], stream: bool = False) -> None:
        super().__init__()
        self.function = function
        self.stream = stream
        self.stopped = False  # asked to stop: what is made is still handed over

    def run(self) -> None:
        try:
            if not self.stream:
                self.done.emit(self.function())
                return
            pieces = self.function()
            try:
                for piece in pieces:
                    if self.stopped:
                        break
                    self.piece.emit(piece)
            finally:
                pieces.close()
        except Exception as error:  # never let a thread die silently
            self.failed.emit(str(error))


def start(
    function: Callable[[], Any],
    on_piece: Callable[[Any], None] | None,
    on_done: Callable[[Any], None] | None,
    on_error: Callable[[str], None] | None,
    on_finished: Callable[[], None] | None,
    stream: bool,
) -> Background:
    """Run `function` and call back on the UI thread."""
    worker = Background(function, stream)
    if on_piece is not None:
        worker.piece.connect(on_piece)
    if on_done is not None:
        worker.done.connect(on_done)
    if on_error is not None:
        worker.failed.connect(on_error)
    if on_finished is not None:
        worker.finished.connect(on_finished)
    worker.start()
    return worker
