import datetime
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QDialog, QWidget

from kubescope.dialogs.pick_row_dialog import PickRowDialog
from kubescope.extensions.components import UiComponents

application = QApplication.instance() or QApplication([])
KEEP = []  # the parent of a dialog must outlive it

TEXTS = {"search": "s", "from": "From", "to": "To", "cancel": "No", "ok": "Yes"}
ROWS = [["a.log", "1 KiB"], ["b.log", "2 KiB"], ["c.err", "3 KiB"]]
DAYS = [datetime.datetime(2026, 11, day, 10, tzinfo=datetime.UTC) for day in (1, 5, 9)]


def parent():
    KEEP.append(QWidget())
    return KEEP[-1]


def shown(dialog):
    return [dialog.table.item(i, 0).text() for i in range(dialog.table.rowCount())]


def test_the_table_narrows_by_text_and_by_a_range_of_dates() -> None:
    dialog = PickRowDialog(
        parent(), UiComponents(), "T", "L", ["File", "Size"], ROWS, DAYS, TEXTS
    )
    assert shown(dialog) == ["a.log", "b.log", "c.err"]
    assert dialog.count.text() == "3 / 3"

    dialog.search.setText("LOG")
    assert shown(dialog) == ["a.log", "b.log"]
    dialog.last.setText("2026-11-03")
    dialog.first.setText("2026-1")  # not a date yet: no lower limit
    assert shown(dialog) == ["a.log"]
    dialog.search.setText("nothing")
    assert shown(dialog) == [] and not dialog.ok.isEnabled()


def test_the_row_picked_is_the_index_in_the_whole_list() -> None:
    dialog = PickRowDialog(
        parent(), UiComponents(), "T", "L", ["File", "Size"], ROWS, DAYS, TEXTS
    )
    dialog.search.setText("err")
    dialog.ok.click()
    assert dialog.result() == QDialog.DialogCode.Accepted
    assert dialog.picked == 2


def test_without_dates_there_is_no_range_and_nothing_picked_when_empty() -> None:
    dialog = PickRowDialog(
        parent(), UiComponents(), "T", "L", ["File", "Size"], ROWS, None, TEXTS
    )
    assert shown(dialog) == ["a.log", "b.log", "c.err"]
    dialog.search.setText("zzz")
    dialog._accept()
    assert dialog.picked == -1


def test_a_click_on_a_header_sorts_and_a_second_one_reverses() -> None:
    rows = [["a", "10 KiB"], ["b", "9 KiB"], ["c", "100 KiB"]]
    dialog = PickRowDialog(
        parent(), UiComponents(), "T", "L", ["F", "S"], rows, None, TEXTS
    )
    dialog.sorter.clicked(1)
    assert shown(dialog) == ["b", "a", "c"]
    dialog.sorter.clicked(1)
    assert shown(dialog) == ["c", "a", "b"]
    dialog.table.selectRow(0)
    dialog.ok.click()
    assert dialog.picked == 2  # still the index in the whole list
