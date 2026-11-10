from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget

from kubescope.dialogs.global_search import GlobalSearch, SearchEntry
from kubescope.models import SearchHit, match_rank
from tests.qt import get_application

application = get_application()


def test_every_word_must_match_in_any_order():
    assert match_rank("api prod", "prod-api Deployment") is not None
    assert match_rank("api db", "prod-api Deployment") is None


def test_ranks_prefix_then_word_then_inside():
    assert match_rank("api", "api-server") == 0
    assert match_rank("api", "prod-api") == 1
    assert match_rank("pi", "prod-api") == 2


def test_empty_query_has_no_rank():
    assert match_rank("  ", "x") is None


def _key(dialog: GlobalSearch, key: Qt.Key) -> bool:
    event = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    return dialog.eventFilter(dialog.input, event)


def _labels(dialog: GlobalSearch) -> list[str]:
    return [
        dialog.results.item(row).text().split("    ")[0]
        for row in range(dialog.results.count())
    ]


def test_it_lists_the_screens_then_the_resources_that_match() -> None:
    went = []
    dialog = GlobalSearch()
    dialog.open_with(
        [
            SearchEntry("Pods", "Screen", lambda: went.append("pods")),
            SearchEntry("Settings", "", lambda: went.append("settings")),
        ]
    )
    assert _labels(dialog) == ["Pods", "Settings"]  # nothing typed: the screens
    assert dialog.note.text()  # the resources are still loading

    opened = []
    dialog.set_resources(
        [SearchHit("Pod", "ns", "api-pods"), SearchHit("Node", "", "pods-node")],
        opened.append,
    )
    assert dialog.note.text() == ""
    dialog.input.setText("pods")
    assert _labels(dialog) == ["Pods", "pods-node", "api-pods"]  # best match first

    dialog.input.setText("zzz")
    assert dialog.results.count() == 0


def test_the_arrows_move_and_enter_goes_to_the_chosen_one() -> None:
    went = []
    dialog = GlobalSearch()
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


def test_a_failure_is_told_and_leaving_the_window_closes_it() -> None:
    dialog = GlobalSearch()
    dialog.open_with([])
    dialog.resources_failed("could not read")
    assert dialog.note.text() == "could not read"

    dialog.event(QEvent(QEvent.Type.WindowDeactivate))
    assert not dialog.isVisible()
    dialog.event(QEvent(QEvent.Type.WindowDeactivate))  # already closed

    window = QWidget()
    window.resize(800, 600)
    inside = GlobalSearch(window)
    inside.open_with([])
    assert inside.y() >= 0
