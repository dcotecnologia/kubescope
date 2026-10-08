import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QTableWidgetItem

from kubectl_gui import window as window_module
from kubectl_gui.models import Workload

application = QApplication.instance() or QApplication([])


def test_workload_actions_dispatch_and_follow_visible_selection(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    workload = Workload("arquitteh", "Deployment", "api", 1, 1, "1h")
    window._workloads = [workload]
    window.table.setRowCount(1)
    window.table.setItem(0, 0, QTableWidgetItem(workload.name))
    window.table.selectRow(0)

    dispatched = []

    def capture_action(operation, _callback, *arguments) -> None:
        dispatched.append((operation.__name__, arguments))

    monkeypatch.setattr(window, "_run_action", capture_action)
    window.pods_button.click()
    window.details_button.click()
    window.logs_button.click()

    assert [operation for operation, _arguments in dispatched] == [
        "get_workload_pods",
        "get_resource_details",
        "get_workload_pods",
    ]
    assert dispatched[1][1] == ("", "Deployment", "arquitteh", "api")

    window.search_input.setText("no-match")

    assert window.table.isRowHidden(0)
    assert all(
        not button.isEnabled()
        for button in (window.pods_button, window.details_button, window.logs_button)
    )
    window.close()
