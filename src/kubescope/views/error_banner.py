from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFrame, QLabel, QPushButton


class ErrorBanner(QObject):
    """Drives a red banner of the window: a short line that says what went
    wrong, with the original error one click away and a button to dismiss it.

    The widgets come from a `.ui` file; this only knows what they do.
    """

    def __init__(
        self,
        frame: QFrame,
        label: QLabel,
        details_button: QPushButton,
        dismiss_button: QPushButton,
        details_label: QLabel,
    ) -> None:
        super().__init__(frame)
        self._frame = frame
        self._label = label
        self._details_button = details_button
        self._details_label = details_label
        self._words = ("Details", "Hide")
        dismiss_button.clicked.connect(self.dismiss)
        details_button.clicked.connect(self.toggle_details)

    def show_error(
        self, text: str, details: str, words: tuple[str, str] = ("Details", "Hide")
    ) -> None:
        """Show the banner with a line and the original text of the error; the
        button that opens it is named by `words` (its closed and open
        names)."""
        self._words = words
        self._label.setText(text)
        self._details_label.setText(details)
        self._details_label.hide()
        self._details_button.setText(words[0])
        self._details_button.setVisible(bool(details) and details != text)
        self._frame.show()

    def dismiss(self) -> None:
        self._frame.hide()

    def toggle_details(self) -> None:
        showing = not self._details_label.isHidden()
        self._details_label.setVisible(not showing)
        self._details_button.setText(self._words[0] if showing else self._words[1])
