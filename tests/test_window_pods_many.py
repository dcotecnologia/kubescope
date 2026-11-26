from kubescope.sdk.models import PodInfo, Workload
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from kubescope import window as window_module
from tests.test_window_write import _fake_menu, _window

PODS = [PodInfo("ns", f"p{n}", "Running", 1, 1, "1h", ("app",)) for n in range(3)]
NAME = 2  # the column of the name in the Pods list, the first one it shows


def _pods_window(monkeypatch, pods=PODS):
    window, ran = _window(monkeypatch)
    window.show()
    monkeypatch.setattr(window, "_context", lambda: "prod")
    window._open_list_view("pods")
    window._show_pods(["ns"], list(pods))
    return window, ran


def _item(window, row: int) -> QTableWidgetItem:
    item = window.table.item(row, NAME)
    assert item is not None
    return item


def _check(window, *rows: int, checked: bool = True) -> None:
    """What the person does: check (or uncheck) the box of these rows."""
    state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
    for row in rows:
        _item(window, row).setCheckState(state)


def _names(window) -> list[str]:
    return [pod.name for pod in window._checked_rows()]


def test_the_pods_have_a_box_and_a_list_with_nothing_for_many_does_not(
    monkeypatch,
) -> None:
    window, _ran = _pods_window(monkeypatch)

    assert _item(window, 0).flags() & Qt.ItemFlag.ItemIsUserCheckable
    assert _item(window, 0).checkState() == Qt.CheckState.Unchecked
    assert window.check_header.column == NAME
    assert window.table.selectionMode() == QTableWidget.SelectionMode.SingleSelection

    monkeypatch.setitem(window_module.WRITE_VIEWS, "statefulsets", ("forward",))
    window._open_list_view("statefulsets")  # Forward is not for many
    window._apply_view_buttons()
    assert window.check_header.column == -1
    assert window._checked_rows() == []  # no boxes, nothing to act on
    window.close()


def test_checking_boxes_chooses_the_pods_in_the_order_they_are_shown(
    monkeypatch,
) -> None:
    window, _ran = _pods_window(monkeypatch)

    _check(window, 2, 0)
    assert _names(window) == ["p0", "p2"]

    _check(window, 0, checked=False)
    assert _names(window) == ["p2"]

    window.table.setRowHidden(2, True)  # filtered out: it is not chosen any more
    assert _names(window) == []
    window.close()


def test_the_box_of_the_header_says_none_some_or_all(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    header = window.check_header
    assert header.check_state == Qt.CheckState.Unchecked

    _check(window, 0)
    assert header.check_state == Qt.CheckState.PartiallyChecked
    _check(window, 1, 2)
    assert header.check_state == Qt.CheckState.Checked

    window.table.setRowHidden(0, True)  # what shows is what counts
    window._sync_checks()
    assert header.check_state == Qt.CheckState.Checked
    window.table.setRowHidden(1, True)
    window.table.setRowHidden(2, True)
    window._sync_checks()
    assert header.check_state == Qt.CheckState.Unchecked  # nothing shown
    window.close()


def test_the_box_of_the_header_checks_and_unchecks_what_shows(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    window.table.setRowHidden(1, True)

    window.check_header.toggled.emit(True)
    assert _names(window) == ["p0", "p2"]
    assert _item(window, 0).checkState() == Qt.CheckState.Checked
    assert _item(window, 1).checkState() == Qt.CheckState.Unchecked
    assert window.check_header.check_state == Qt.CheckState.Checked

    window.check_header.toggled.emit(False)
    assert _names(window) == []
    assert window.check_header.check_state == Qt.CheckState.Unchecked
    window.close()


def test_the_boxes_survive_a_new_read_and_go_with_the_pods_that_leave(
    monkeypatch,
) -> None:
    window, _ran = _pods_window(monkeypatch)
    _check(window, 0, 2)

    window._show_pods(["ns"], list(PODS))  # the same Pods again
    assert _names(window) == ["p0", "p2"]
    assert _item(window, 2).checkState() == Qt.CheckState.Checked

    window._show_pods(["ns"], [PODS[1], PODS[2]])  # p0 is gone
    assert _names(window) == ["p2"]
    assert window._checked == {("Pod", "ns", "p2")}
    window.close()


def test_with_pods_checked_only_evict_and_delete_are_offered(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    assert window.details_button not in window._offered  # no row picked
    assert window.write_buttons["shell"] not in window._offered
    window.table.selectRow(0)  # one row: its menu and keys offer the actions
    assert window.details_button in window._offered
    assert window.write_buttons["shell"] in window._offered
    for button in (window.details_button, window.write_buttons["shell"]):
        assert not button.isVisibleTo(window)  # the bar is for many rows

    _check(window, 0, 1)

    for button in (window.pods_button, window.details_button, window.logs_button):
        assert button not in window._offered and not button.isVisibleTo(window)
    assert not window.write_buttons["shell"].isVisibleTo(window)
    assert not window.write_buttons["forward"].isVisibleTo(window)
    for shape in ("evict", "delete"):
        assert window.write_buttons[shape].isVisibleTo(window)  # the bar shows
        assert window.write_buttons[shape].isEnabled()

    _check(window, 0, 1, checked=False)  # none checked: the bar goes
    window.table.selectRow(0)
    assert not window.write_buttons["delete"].isVisibleTo(window)
    assert window.details_button in window._offered
    assert window.write_buttons["shell"] in window._offered
    window.close()


def test_the_buttons_follow_what_the_cluster_allows_in_every_namespace(
    monkeypatch,
) -> None:
    pods = [PODS[0], PodInfo("other", "q", "Running", 1, 1, "1h", ("app",))]
    window, _ran = _pods_window(monkeypatch, pods)
    allowed = {"ns": frozenset({"evict", "delete"}), "other": frozenset({"delete"})}
    monkeypatch.setattr(window, "_allowed_shapes", lambda namespace: allowed[namespace])

    _check(window, 0, 1)

    assert window.write_buttons["delete"].isVisibleTo(window)
    assert not window.write_buttons["evict"].isVisibleTo(window)  # not in "other"
    assert [shape for shape, _t, _c in window._bulk_entries(pods)] == ["delete"]
    window.close()


def test_the_cluster_not_having_answered_offers_both(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    monkeypatch.setattr(window, "_allowed_shapes", lambda namespace: None)

    assert [s for s, _t, _c in window._bulk_entries(PODS)] == ["evict", "delete"]
    window.close()


def test_evicting_many_pods_asks_once_naming_them_and_runs_them_together(
    monkeypatch,
) -> None:
    window, ran = _pods_window(monkeypatch)
    asked: list[tuple] = []
    monkeypatch.setattr(
        window,
        "_confirm",
        lambda title, text, action: asked.append((title, text, action)) or True,
    )
    _check(window, 0, 2)

    window.write_buttons["evict"].click()

    assert asked == [
        ("Evict Pods", "Evict the 2 selected Pods?\n\nns/p0\nns/p2", "Evict")
    ]
    ((name, args, kwargs),) = ran
    assert name == "for_each"
    assert args[0] is window_module.evict_pod
    assert args[1:] == ("prod", [("ns", "p0"), ("ns", "p2")])
    assert kwargs["on_error"] == window._show_write_error
    window.close()


def test_deleting_many_pods_and_cancelling(monkeypatch) -> None:
    window, ran = _pods_window(monkeypatch)
    answer = {"yes": False}
    monkeypatch.setattr(window, "_confirm", lambda *_a: answer["yes"])
    _check(window, 0, 1)

    window.write_buttons["delete"].click()
    assert ran == []

    answer["yes"] = True
    window.write_buttons["delete"].click()
    assert ran[0][1][0] is window_module.delete_pod
    window.close()


def test_one_pod_checked_goes_the_way_of_one_pod(monkeypatch) -> None:
    window, ran = _pods_window(monkeypatch)
    asked: list[str] = []
    monkeypatch.setattr(
        window, "_confirm", lambda title, text, action: asked.append(text) or True
    )
    _check(window, 1)

    window.write_buttons["evict"].click()
    window.write_buttons["delete"].click()

    assert asked == ["Evict the Pod p1 in ns?", "Delete the Pod p1 in ns?"]
    assert [(name, args[1:]) for name, args, _k in ran] == [
        ("evict_pod", ("ns", "p1")),
        ("delete_pod", ("ns", "p1")),
    ]
    window.close()


def test_a_button_that_is_not_for_many_pods_does_nothing_with_many(monkeypatch) -> None:
    window, ran = _pods_window(monkeypatch)
    _check(window, 0, 1)

    window._write_button_clicked("shell")

    assert ran == []
    window.close()


def test_the_confirmation_names_the_first_pods_only(monkeypatch) -> None:
    many = [PodInfo("ns", f"p{n}", "Running", 1, 1, "1h", ()) for n in range(12)]
    window, _ran = _pods_window(monkeypatch, many)
    texts: list[str] = []
    monkeypatch.setattr(
        window, "_confirm", lambda title, text, action: texts.append(text) or False
    )

    window._delete_many(many)

    assert texts[0].count("ns/p") == window_module.POD_NAMES_SHOWN
    assert texts[0].endswith("…")
    window.close()


def test_a_run_says_how_many_went_and_what_failed(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    banner: list[str] = []
    status: list[str] = []
    monkeypatch.setattr(window, "_show_write_error", banner.append)
    monkeypatch.setattr(window, "_write_done", status.append)

    window._many_done("evicted", 3, [])
    window._many_done("deleted", 3, [(("ns", "p1"), "forbidden\nmore")])
    window._many_done("evicted", 2, [(("ns", "p0"), "budget"), (("ns", "p1"), "x")])

    assert status == [
        "Evicted 3 of 3 Pods",
        "Deleted 2 of 3 Pods",
        "Evicted 0 of 2 Pods",
    ]
    assert banner == [
        "1 Pods could not be deleted: ns/p1: forbidden",
        "2 Pods could not be evicted: ns/p0: budget",
    ]
    window.close()


def test_the_menu_of_a_checked_pod_is_for_all_the_checked(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)
    seen: list = []
    _fake_menu(monkeypatch, seen)

    def on(row: int) -> QPoint:
        return QPoint(5, window.table.rowViewportPosition(row) + 2)

    _check(window, 0, 1)
    window._show_row_menu(on(1))  # a Pod with its box checked: only what is for many
    assert seen[-1] == ["Evict", "Delete"]
    assert _names(window) == ["p0", "p1"]

    window._show_row_menu(on(2))  # one that is not: its own menu, as always
    assert "Shell command" in seen[-1]

    window.settings.write_mode = False
    count = len(seen)
    window._show_row_menu(on(0))  # read-only: nothing to offer on many
    assert len(seen) == count
    window.close()


def test_deployments_have_no_boxes(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    window._show_workloads(["ns"], [Workload("ns", "Deployment", "a", 1, 1, "1d")])

    assert window._checked_rows() == []
    item = window.table.item(0, NAME)
    assert item is not None
    assert item.data(Qt.ItemDataRole.CheckStateRole) is None  # no box is drawn
    window._item_changed(item)  # not the Pods: nothing happens
    window.close()


def test_a_change_of_a_box_that_is_not_one_is_ignored(monkeypatch) -> None:
    window, _ran = _pods_window(monkeypatch)

    first = window.table.item(0, 0)
    assert first is not None
    window._item_changed(first)  # another column

    plain = window.table.item(0, NAME)
    assert plain is not None
    plain.setData(Qt.ItemDataRole.CheckStateRole, None)
    window._item_changed(plain)  # a cell with no box

    window.table.setRowCount(5)  # a row the list does not have, with a box
    stray = QTableWidgetItem("x")
    stray.setCheckState(Qt.CheckState.Unchecked)
    window.table.setItem(4, NAME, stray)
    window._item_changed(stray)

    assert window._checked == set()
    window.close()


def test_a_row_without_a_cell_gets_no_box_and_no_column_means_no_boxes(
    monkeypatch,
) -> None:
    window, _ran = _pods_window(monkeypatch)

    window.table.takeItem(1, NAME)  # a row that has no cell where the box goes
    window._stamp_checks()
    assert _item(window, 0).checkState() == Qt.CheckState.Unchecked

    for column in range(window.table.columnCount()):
        window.table.setColumnHidden(column, True)
    assert window._check_column() == -1  # nothing shows: nowhere to put a box
    window.close()


DEPLOYMENTS = [Workload("ns", "Deployment", f"d{n}", 1, 1, "1d") for n in range(3)]


def _workloads_window(monkeypatch, view="deployments", rows=DEPLOYMENTS):
    window, ran = _window(monkeypatch)
    window.show()
    monkeypatch.setattr(window, "_context", lambda: "prod")
    window._open_list_view(view)
    window._apply_view_buttons()  # as the app does when the write mode goes on
    window._show_workloads(["ns"], list(rows))
    return window, ran


def _first_column(window) -> int:
    return window._check_column()


def test_every_list_that_can_act_on_many_has_boxes_in_its_first_column(
    monkeypatch,
) -> None:
    window, _ran = _workloads_window(monkeypatch)

    column = _first_column(window)
    assert column >= 0 and window.check_header.column == column
    item = window.table.item(0, column)
    assert item is not None and item.checkState() == Qt.CheckState.Unchecked

    for view in ("statefulsets", "daemonsets"):  # others have Delete, so boxes
        window._open_list_view(view)
        window._show_workloads(["ns"], [Workload("ns", "StatefulSet", "s", 1, 1, "1d")])
        assert window.check_header.column == _first_column(window) >= 0
    window.close()


def test_a_list_has_no_boxes_when_nothing_works_on_many(monkeypatch) -> None:
    window, _ran = _workloads_window(monkeypatch)
    window.settings.write_mode = False
    window._apply_checks()  # without the write mode there is nothing to do to many

    assert window.check_header.column == -1
    assert window._checked_rows() == []
    item = window.table.item(0, _first_column(window))
    assert item is not None
    assert item.data(Qt.ItemDataRole.CheckStateRole) is None
    window.close()


def test_the_boxes_leave_a_column_that_is_hidden_and_go_to_the_next(
    monkeypatch,
) -> None:
    window, _ran = _workloads_window(monkeypatch)
    first = _first_column(window)

    window._set_column_visible(first, False)

    second = _first_column(window)
    assert second != first and window.check_header.column == second
    old = window.table.item(0, first)
    assert old is not None and old.data(Qt.ItemDataRole.CheckStateRole) is None
    new = window.table.item(0, second)
    assert new is not None and new.checkState() == Qt.CheckState.Unchecked
    window.close()


def test_checked_deployments_offer_restart_and_delete_only(monkeypatch) -> None:
    window, ran = _workloads_window(monkeypatch)
    asked: list[tuple[str, str]] = []
    monkeypatch.setattr(
        window,
        "_confirm",
        lambda title, text, action: asked.append((title, text)) or True,
    )
    column = _first_column(window)
    for row in (0, 2):
        item = window.table.item(row, column)
        assert item is not None
        item.setCheckState(Qt.CheckState.Checked)

    assert [row.name for row in window._checked_rows()] == ["d0", "d2"]
    assert not window.write_buttons["scale"].isVisibleTo(window)  # not for many
    assert window.write_buttons["reload"].isVisibleTo(window)
    assert window.write_buttons["delete"].isVisibleTo(window)
    assert [s for s, _t, _c in window._bulk_entries(window._checked_rows())] == [
        "reload",
        "delete",
    ]

    window.write_buttons["reload"].click()
    window.write_buttons["delete"].click()

    assert asked == [
        (
            "Restart Deployments",
            "Restart the 2 selected Deployments?\n\nns/d0\nns/d2",
        ),
        ("Delete resources", "Delete the 2 selected resources?\n\nns/d0\nns/d2"),
    ]
    restart, delete = ran
    assert restart[1][0] is window_module.restart_deployment
    assert restart[1][1:] == ("prod", [("ns", "d0"), ("ns", "d2")])
    assert delete[1][0] is window_module.delete_resource
    assert delete[1][1:] == (
        "prod",
        [("Deployment", "ns", "d0"), ("Deployment", "ns", "d2")],
    )
    window.close()


def test_one_row_checked_goes_the_way_of_one_row(monkeypatch) -> None:
    window, ran = _workloads_window(monkeypatch)
    asked: list[str] = []
    monkeypatch.setattr(
        window, "_confirm", lambda title, text, action: asked.append(text) or True
    )
    item = window.table.item(1, _first_column(window))
    assert item is not None
    item.setCheckState(Qt.CheckState.Checked)

    window.write_buttons["reload"].click()
    window.write_buttons["delete"].click()

    assert len(asked) == 2 and "d1" in asked[0] and "d1" in asked[1]
    assert [name for name, _a, _k in ran] == ["restart_deployment", "delete_resource"]
    window.close()


def test_the_run_of_resources_says_how_many_went_and_what_failed(
    monkeypatch,
) -> None:
    window, _ran = _workloads_window(monkeypatch)
    banner: list[str] = []
    status: list[str] = []
    monkeypatch.setattr(window, "_show_write_error", banner.append)
    monkeypatch.setattr(window, "_write_done", status.append)

    window._many_done("removed", 3, [(("Deployment", "ns", "d1"), "forbidden\nx")])
    window._many_done("restarted", 2, [(("ns", "d0"), "nope")])
    window._many_done("removed", 1, [(("Node", "", "n1"), "busy")])  # cluster-wide

    assert status == [
        "Deleted 2 of 3 resources",
        "Restarted 1 of 2 Deployments",
        "Deleted 0 of 1 resources",
    ]
    assert banner == [
        "1 resources could not be deleted: ns/d1: forbidden",
        "1 Deployments could not be restarted: ns/d0: nope",
        "1 resources could not be deleted: n1: busy",
    ]
    window.close()


def test_the_menu_of_a_checked_row_of_any_list_is_for_all_the_checked(
    monkeypatch,
) -> None:
    window, _ran = _workloads_window(monkeypatch)
    seen: list = []
    _fake_menu(monkeypatch, seen)
    column = _first_column(window)
    for row in (0, 1):
        item = window.table.item(row, column)
        assert item is not None
        item.setCheckState(Qt.CheckState.Checked)

    def on(row: int) -> QPoint:
        return QPoint(5, window.table.rowViewportPosition(row) + 2)

    window._show_row_menu(on(0))
    assert seen[-1] == ["Restart", "Delete"]  # not Scale, and nothing of the row
    window._show_row_menu(on(2))  # a row that is not checked: its own menu
    assert "Scale" in seen[-1]
    window.close()


def test_checked_rows_are_forgotten_when_the_list_changes(monkeypatch) -> None:
    window, _ran = _workloads_window(monkeypatch)
    item = window.table.item(0, _first_column(window))
    assert item is not None
    item.setCheckState(Qt.CheckState.Checked)
    assert window._checked

    window._open_list_view("statefulsets")  # another list: other rows
    assert window._checked == set()
    window.close()


def test_enter_opens_the_details_and_delete_and_ctrl_e_act_on_the_row(
    monkeypatch,
) -> None:
    pressed: list[str] = []
    monkeypatch.setattr(
        window_module.WorkloadWindow,
        "_write_button_clicked",
        lambda _self, shape: pressed.append(shape),  # the real one asks first
    )
    window, _ran = _pods_window(monkeypatch)
    window.details_button.clicked.connect(lambda: pressed.append("details"))
    window.settings.write_mode = False
    window._update_write_buttons()

    keys = {
        action: window._shortcuts[action]
        for action in ("row_details", "row_details_alt", "row_edit", "row_delete")
    }
    assert [shortcut.key().toString() for shortcut in keys.values()] == [
        "Return",
        "Enter",
        "Ctrl+E",
        "Del",
    ]
    for shortcut in keys.values():  # only while the list has the focus
        assert shortcut.context() == Qt.ShortcutContext.WidgetShortcut
        assert shortcut.parent() is window.table

    keys["row_details"].activated.emit()  # no row picked: nothing is offered
    keys["row_delete"].activated.emit()
    assert pressed == []

    window.table.selectRow(1)
    keys["row_details"].activated.emit()
    keys["row_details_alt"].activated.emit()
    assert pressed == ["details", "details"]

    keys["row_delete"].activated.emit()  # the write mode is off: no Delete button
    keys["row_edit"].activated.emit()
    assert pressed == ["details", "details"]

    window.settings.write_mode = True
    window._update_write_buttons()
    keys["row_delete"].activated.emit()
    assert pressed == ["details", "details", "delete"]
    window.close()
