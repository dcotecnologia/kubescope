import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget

from kubescope.views import search_bar
from kubescope.views.search_bar import SearchBar, compile_query, find_spans

application = QApplication.instance() or QApplication([])

TEXT = "Error: disk full\nwarn: low disk\nerror: disk 42 gone"


_made: list[QWidget] = []


@pytest.fixture(autouse=True)
def dispose_widgets():
    """Delete the widgets a test made, in Qt's own way: one left to Python's
    garbage collector can abort the process when it ends."""
    yield
    for widget in _made:
        widget.deleteLater()
    _made.clear()
    QApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)


def _made_here[T: QWidget](widget: T) -> T:
    _made.append(widget)
    return widget


def _bar(text: str = TEXT) -> SearchBar:
    editor = _made_here(QPlainTextEdit())
    editor.setPlainText(text)
    return _made_here(SearchBar(editor))


def test_a_search_ignores_the_case_unless_asked() -> None:
    assert find_spans(TEXT, "error", False, False) == [(0, 5), (32, 37)]
    assert find_spans(TEXT, "error", True, False) == [(32, 37)]


def test_a_plain_search_takes_the_text_as_it_is_and_a_regex_as_a_pattern() -> None:
    assert find_spans("a.b axb", "a.b", False, False) == [(0, 3)]
    assert find_spans("a.b axb", "a.b", False, True) == [(0, 3), (4, 7)]
    assert find_spans("abc", r"\d*", False, True) == []  # empty matches do not count
    assert find_spans("abc", "", False, False) == []
    assert compile_query("", False, True) is None


def test_a_pattern_that_does_not_compile_raises() -> None:
    with pytest.raises(search_bar.re.error):
        find_spans("abc", "(", False, True)


def test_the_positions_follow_the_document_after_a_wide_character() -> None:
    spans = find_spans("😀 ok 😀 ok", "ok", False, False)

    assert search_bar._document_offsets("😀 ok 😀 ok", spans) == [(3, 5), (9, 11)]
    assert search_bar._document_offsets("plain", [(1, 2)]) == [(1, 2)]


def test_typing_marks_every_match_and_selects_the_first_one() -> None:
    bar = _bar()
    edited = []
    bar.edited.connect(lambda: edited.append(True))

    bar.input.setText("disk")

    assert edited
    assert bar.count_label.text() == "1 of 3"
    assert len(bar.editor.extraSelections()) == 3
    assert bar.editor.textCursor().selectedText() == "disk"
    bar.step(1)
    assert bar.count_label.text() == "2 of 3"
    bar.step(-1)
    bar.step(-1)
    assert bar.count_label.text() == "3 of 3"  # round the ends
    bar.step(1)
    assert bar.count_label.text() == "1 of 3"


def test_the_arrow_buttons_go_to_the_next_and_the_previous_match() -> None:
    bar = _bar()
    bar.input.setText("disk")

    bar.next_button.click()
    assert bar.count_label.text() == "2 of 3"
    bar.previous_button.click()
    bar.previous_button.click()
    assert bar.count_label.text() == "3 of 3"


def test_the_switches_change_the_matches() -> None:
    bar = _bar()
    bar.input.setText("error")
    assert bar.count_label.text() == "1 of 2"

    bar.case_button.setChecked(True)
    assert bar.count_label.text() == "1 of 1"

    bar.case_button.setChecked(False)
    bar.input.setText(r"disk \d+")
    assert bar.count_label.text() == "No results"
    bar.regex_button.setChecked(True)
    assert bar.count_label.text() == "1 of 1"


def test_a_bad_expression_says_so_and_marks_nothing() -> None:
    bar = _bar()
    bar.regex_button.setChecked(True)

    bar.input.setText("(")

    assert bar.count_label.text() == "Invalid expression"
    assert bar.input.toolTip()
    assert bar.editor.extraSelections() == []
    bar.input.setText("disk")
    assert bar.input.toolTip() == ""


def test_an_empty_search_clears_the_marks() -> None:
    bar = _bar()
    bar.input.setText("disk")

    bar.input.clear()

    assert bar.count_label.text() == ""
    assert bar.editor.extraSelections() == []
    bar.step(1)  # nothing to go to


def test_refresh_follows_new_text_without_moving_the_view() -> None:
    bar = _bar()
    bar.input.setText("disk")
    bar.step(1)
    selected = bar.editor.textCursor().selectionStart()

    bar.editor.appendPlainText("one more disk")
    bar.refresh()

    assert bar.count_label.text() == "2 of 4"
    assert bar.editor.textCursor().selectionStart() == selected
    bar.editor.setPlainText("nothing")
    bar.refresh()
    assert bar.count_label.text() == "No results"


def test_the_marks_are_capped_but_all_matches_are_counted(monkeypatch) -> None:
    monkeypatch.setattr(search_bar, "MAX_MARKED", 2)
    bar = _bar("a a a a")

    bar.input.setText("a")

    assert len(bar.editor.extraSelections()) == 2
    assert bar.count_label.text() == "1 of 4"


def test_enter_goes_to_the_next_match_and_shift_enter_to_the_previous(
    monkeypatch,
) -> None:
    bar = _bar()
    bar.input.setText("disk")
    shifted = []
    monkeypatch.setattr(
        search_bar.QApplication,
        "keyboardModifiers",
        lambda: (
            search_bar.Qt.KeyboardModifier.ShiftModifier
            if shifted
            else search_bar.Qt.KeyboardModifier.NoModifier
        ),
    )

    bar.input.returnPressed.emit()
    assert bar.count_label.text() == "2 of 3"
    shifted.append(True)
    bar.input.returnPressed.emit()
    assert bar.count_label.text() == "1 of 3"


def test_escape_clears_the_search_and_gives_the_text_the_focus() -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest

    bar = _bar()
    bar.input.setText("disk")

    QTest.keyClick(bar.input, Qt.Key.Key_Escape)
    assert bar.input.text() == ""

    QTest.keyClick(bar.input, Qt.Key.Key_A)  # any other key types as usual
    assert bar.input.text() == "a"
    bar.focus()


def test_the_log_tab_searches_its_text_and_keeps_up_with_new_lines() -> None:
    from kubescope.models import PodInfo
    from kubescope.views.log_tab import LogTab

    tab = _made_here(
        LogTab("ctx", PodInfo("ns", "api", "Running", 1, 1, "1d", ("app",)), "app")
    )
    tab.set_logs("INFO up\nERROR down\nINFO up again")

    tab.search.input.setText("info")
    assert tab.search.count_label.text() == "1 of 2"
    tab.add_logs("INFO third")
    assert tab.search.count_label.text() == "1 of 3"
    tab.set_logs("nothing here")
    assert tab.search.count_label.text() == "No results"
    tab.search.focus()


def test_the_details_search_opens_the_raw_json() -> None:
    from kubescope.views.detail_tab import DetailTab

    tab = _made_here(
        DetailTab(
            "pod", {"metadata": {"name": "api"}, "spec": {"nodeName": "api-node"}}
        )
    )
    assert not tab.showing_raw

    tab.search.input.setText("api")

    assert tab.showing_raw
    assert tab.search.count_label.text() == "1 of 2"


def test_the_list_filter_has_the_same_switches(monkeypatch) -> None:
    from kubescope.models import ClusterResource
    from tests.test_window_flows import _ready_window

    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("services")
    window._show_resources(
        ["ns"],
        [
            ClusterResource("ns", "Service", "Web", ("ClusterIP",), "1d"),
            ClusterResource("ns", "Service", "web-2", ("ClusterIP",), "1d"),
            ClusterResource("ns", "Service", "api", ("ClusterIP",), "1d"),
        ],
    )

    window.search_input.setText("WEB")
    assert window.summary_label.text() == "2 of 3 Services"
    window.search_case_button.setChecked(True)
    assert window.summary_label.text() == "0 of 3 Services"
    window.search_case_button.setChecked(False)
    window.search_input.setText(r"web-\d$")
    assert window.summary_label.text() == "0 of 3 Services"
    window.search_regex_button.setChecked(True)
    assert window.summary_label.text() == "1 of 3 Services"
    window.search_input.setText("(")  # does not compile: every row stays
    assert window.summary_label.text() == "3 of 3 Services"
    assert window.search_input.toolTip()
    window.search_input.setText("")
    assert window.search_input.toolTip() == ""
    window._retranslate()
    assert window.search_case_button.toolTip() == "Match case"
    window.close()
