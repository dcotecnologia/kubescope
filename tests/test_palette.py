import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from kubescope.sdk.models import SearchHit, match_rank
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget

from kubescope.extensions.palette import Palette, SearchEntry, style
from tests.qt import get_application

application = get_application()


def test_every_word_must_match_in_any_order() -> None:
    assert match_rank("api prod", "prod-api Deployment") is not None
    assert match_rank("api db", "prod-api Deployment") is None


def _key(dialog: Palette, key: Qt.Key) -> bool:
    event = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    return dialog.eventFilter(dialog.input, event)


def _labels(dialog: Palette) -> list[str]:
    return [
        dialog.results.item(row).text().split("    ")[0]
        for row in range(dialog.results.count())
    ]


def test_the_style_is_written_in_the_colors_the_theme_gives() -> None:
    sheet = style(lambda color, text: f"<{color}:{'text' if text else 'fill'}>")

    assert "background: <#ffffff:fill>" in sheet
    assert "color: <#20232a:text>" in sheet


def test_it_lists_the_screens_then_the_resources_that_match() -> None:
    dialog = Palette()
    dialog.open_with(
        [
            SearchEntry("Pods", "Screen", lambda: None),
            SearchEntry("Settings", "", lambda: None),
        ]
    )
    assert _labels(dialog) == ["Pods", "Settings"]  # nothing typed: the screens
    assert dialog.note.text()  # the resources are still loading

    dialog.set_resources(
        [SearchHit("Pod", "ns", "api-pods"), SearchHit("Node", "", "pods-node")],
        lambda hit: None,
    )
    assert dialog.note.text() == ""
    dialog.input.setText("pods")
    assert _labels(dialog) == ["Pods", "pods-node", "api-pods"]  # best match first
    assert "Pod · ns" in dialog.results.item(2).text()
    assert dialog.results.item(1).text().endswith("Node")  # a kind with no namespace

    dialog.input.setText("zzz")
    assert dialog.results.count() == 0


def test_a_resource_that_is_chosen_is_opened() -> None:
    opened = []
    dialog = Palette()
    dialog.open_with([])
    dialog.set_resources([SearchHit("Pod", "ns", "api")], opened.append)

    dialog.input.setText("api")
    dialog._choose(dialog.results.item(0))

    assert opened == [SearchHit("Pod", "ns", "api")]


def test_at_most_fifty_results_are_shown() -> None:
    dialog = Palette()
    dialog.open_with([SearchEntry(f"e{n}", "", lambda: None) for n in range(80)])

    assert dialog.results.count() == 50


def test_the_arrows_move_and_enter_goes_to_the_chosen_one() -> None:
    went = []
    dialog = Palette()
    dialog.open_with(
        [SearchEntry(name, "", lambda name=name: went.append(name)) for name in "ab"]
    )

    assert _key(dialog, Qt.Key.Key_Down)
    assert _key(dialog, Qt.Key.Key_Down)  # stays on the last
    assert _key(dialog, Qt.Key.Key_Up)
    assert _key(dialog, Qt.Key.Key_Up)  # stays on the first
    assert not _key(dialog, Qt.Key.Key_A)
    assert _key(dialog, Qt.Key.Key_Return)
    assert went == ["a"]
    assert not dialog.isVisible()

    dialog.input.setText("zzz")  # nothing to go to: Enter does nothing
    assert _key(dialog, Qt.Key.Key_Enter)
    assert went == ["a"]


def test_the_components_make_it_with_the_texts_of_the_extension() -> None:
    from kubescope.extensions.components import UiComponents

    made = UiComponents().palette(None, "Find", "Type here", "Waiting")
    assert made.windowTitle() == "Find"
    assert made.input.placeholderText() == "Type here"
    made.open_with([])
    assert made.note.text() == "Waiting"


def test_a_failure_is_told_and_leaving_the_window_closes_it() -> None:
    dialog = Palette()
    dialog.open_with([])
    dialog.resources_failed("could not read")
    assert dialog.note.text() == "could not read"

    dialog.event(QEvent(QEvent.Type.WindowDeactivate))
    assert not dialog.isVisible()
    dialog.event(QEvent(QEvent.Type.WindowDeactivate))  # already closed

    window = QWidget()
    window.resize(800, 600)
    inside = Palette(window)
    inside.open_with([])
    assert inside.y() >= 0
