import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QMessageBox

from kubescope import window as window_module
from kubescope.assistant import actions
from kubescope.assistant.runner import Assistant
from kubescope.views.assistant_tab import AssistantTab
from tests.test_window_flows import _ready_window

ONE = Assistant("one", "One", "one-ai", lambda m, s: [], lambda line: ("", ""))
TWO = Assistant("two", "Two", "two-ai", lambda m, s: [], lambda line: ("", ""))


def _request(action: str, **args) -> actions.Request:
    return actions.Request(actions.BY_NAME[action], args)


def _open(monkeypatch, found=(ONE,), consent=True):
    monkeypatch.setattr(window_module, "installed_assistants", lambda: list(found))
    window = _ready_window(monkeypatch)
    window.settings.assistant_consent = consent
    messages: list[tuple[str, str]] = []
    monkeypatch.setattr(
        window.__class__,
        "_show_message",
        lambda self, icon, title, text, *rest: messages.append((title, text)),
    )
    return window, messages


def _tab(window) -> AssistantTab:
    tab = window._assistant_tab
    assert isinstance(tab, AssistantTab)
    return tab


def test_the_corner_button_opens_and_puts_away_the_chat(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window.show()
    dock = window.assistant_dock
    assert dock.bubble.isVisible() and not dock.is_open

    dock.bubble.click()
    assert dock.is_open and window._assistant_tab is not None

    tab = _tab(window)
    dock.bubble.click()  # the same button puts it away
    assert not dock.is_open

    dock.bubble.click()
    assert dock.is_open and _tab(window) is tab  # the conversation is kept

    dock.panel.close_button.click()
    assert not dock.is_open
    window.close()


def test_without_a_program_or_a_context_there_is_no_chat(monkeypatch) -> None:
    window, messages = _open(monkeypatch, found=())
    window._open_assistant()
    assert "No assistant program" in messages[-1][1]
    assert window._assistant_tab is None and not window.assistant_dock.is_open

    monkeypatch.setattr(window_module, "installed_assistants", lambda: [ONE])
    window.context_combo.clear()
    window._open_assistant()
    assert "Choose a context" in messages[-1][1] and window._assistant_tab is None
    window.close()


def test_the_chat_asks_once_before_anything_can_leave_the_computer(monkeypatch) -> None:
    window, _messages = _open(monkeypatch, consent=False)
    answers = [QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes]
    asked: list[str] = []

    def question(_parent, _title, text, *_rest):
        asked.append(text)
        return answers.pop(0)

    monkeypatch.setattr(window_module.QMessageBox, "question", question)
    monkeypatch.setattr(window, "_save_settings", lambda: None)

    window._open_assistant()
    assert window._assistant_tab is None and not window.settings.assistant_consent

    window._open_assistant()
    assert window.settings.assistant_consent
    assert window._assistant_tab is not None and "sent to One" in asked[0]
    assert "type and attach" in asked[0]

    window._open_assistant()  # agreed already: it does not ask again
    assert len(asked) == 2
    window.close()


def test_images_are_offered_only_to_a_program_that_takes_them(monkeypatch) -> None:
    from kubescope.assistant.claude import CLAUDE

    window, _messages = _open(monkeypatch, found=(ONE,))
    window._open_assistant()
    assert _tab(window)._takes_images is False
    window._end_assistant_chat()

    monkeypatch.setattr(window_module, "installed_assistants", lambda: [CLAUDE])
    window._open_assistant()
    assert _tab(window)._takes_images is True
    window.close()


def test_the_assistant_chosen_is_used_and_otherwise_the_first_one(monkeypatch) -> None:
    window, _messages = _open(monkeypatch, found=(ONE, TWO))

    window.settings.assistant = "two"
    assert window._assistant_program() is TWO
    window.settings.assistant = "gone"
    assert window._assistant_program() is ONE
    window.close()


def test_the_conversation_is_kept_and_found_again_in_the_same_context(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    first = _tab(window)
    first.note("a note worth keeping")
    window.assistant_dock.close()
    window._end_assistant_chat()  # as when the app is closed and opened again

    window._open_assistant()

    second = _tab(window)
    assert second is not first
    assert ("app", "a note worth keeping") in second.entries()
    assert window._assistant_history.entries("prod")[-1] == (
        "app",
        "a note worth keeping",
    )
    window.close()


def test_the_history_is_forgotten_only_after_the_person_agrees(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    _tab(window).note("old")
    answers = [QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes]
    monkeypatch.setattr(
        window_module.QMessageBox, "question", lambda *_a: answers.pop(0)
    )

    window.assistant_dock.panel.clear_button.click()
    assert ("app", "old") in _tab(window).entries()

    window.assistant_dock.panel.clear_button.click()
    assert window._assistant_history.entries("prod") == []
    assert _tab(window).entries() == [] and window.assistant_dock.is_open
    window.close()


def test_the_settings_turn_the_chat_on_or_off_and_choose_the_program(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch, found=(ONE, TWO))
    window._load_settings_form()
    form = window.settings_ui
    assert form.assistantCheck.isChecked() and window.assistant_dock.bubble.isVisibleTo(
        window
    )
    assert form.assistantCombo.itemData(0) == ""
    monkeypatch.setattr(window_module, "ASSISTANTS", {"two": TWO, "one": ONE})
    window._load_settings_form()
    assert [form.assistantCombo.itemText(i) for i in range(3)][1:] == ["Two", "One"]

    window._open_assistant()
    form.assistantCheck.setChecked(False)
    form.assistantCombo.setCurrentIndex(form.assistantCombo.findData("two"))
    window._save_preferences()

    assert not window.settings.assistant_enabled and window.settings.assistant == "two"
    assert not window.assistant_dock.bubble.isVisibleTo(window)
    assert not window.assistant_dock.is_open
    window.close()


def test_every_conversation_can_be_forgotten_from_the_settings(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    _tab(window).note("a")
    window.assistant_dock.close()
    monkeypatch.setattr(
        window_module.QMessageBox,
        "question",
        lambda *_a: QMessageBox.StandardButton.Yes,
    )

    window.settings_ui.assistantClearButton.click()

    assert (
        window._assistant_history.entries("prod") == []
        and window._assistant_tab is None
    )
    window.close()


def test_a_chat_belongs_to_its_cluster_unless_the_assistant_moves_it(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)
    window.context_combo.addItem("dev", "dev")
    window.context_combo.addItem("qa", "qa")
    window._open_assistant()
    tab = _tab(window)

    tab.navigate.emit(_request("switch_context", context="dev"))
    assert window._assistant_tab is tab and tab.context == "dev"
    assert window.assistant_dock.is_open

    window.context_combo.setCurrentIndex(window.context_combo.findData("qa"))
    assert window._assistant_tab is None and tab.closed
    assert not window.assistant_dock.is_open
    window.close()


def test_the_assistant_navigates_the_window_as_the_person_would(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    window.context_combo.addItem("dev", "dev")
    opened: list = []
    monkeypatch.setattr(window, "_press_refresh", lambda: opened.append("refresh"))
    monkeypatch.setattr(window, "_open_resource", lambda *a: opened.append(a))

    tab.navigate.emit(_request("open_view", view="pods"))
    assert window._view == "pods"

    monkeypatch.setattr(window, "_fill_namespaces", lambda _names: None)
    window.namespace_combo.addItem("ns", "ns")  # the list's answer brings them
    tab.navigate.emit(_request("set_namespace", namespace="ns"))
    assert window.namespace_combo.currentData() == "ns"
    tab.navigate.emit(_request("set_namespace", namespace="nope"))
    assert "There is no namespace nope" in tab.markdown()

    tab.navigate.emit(_request("search", text="web", regex=True, case=True))
    assert window.search_input.text() == "web"
    assert window.search_regex_button.isChecked()
    assert window.search_case_button.isChecked()
    tab.navigate.emit(_request("search", text=""))
    assert not window.search_regex_button.isChecked()

    tab.navigate.emit(_request("switch_context", context="dev"))
    assert window._context() == "dev" and tab.context == "dev"
    tab.navigate.emit(_request("switch_context", context="gone"))
    assert tab.context == "dev" and "There is no context gone" in tab.markdown()

    tab.navigate.emit(_request("refresh"))
    tab.navigate.emit(_request("show_details", kind="Pod", namespace="ns", name="p"))
    assert opened == ["refresh", ("Pod", "ns", "p")]
    window.close()


def test_a_list_of_eks_only_is_not_opened_in_another_context(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    window.ui.navNodeGroups.setVisible(False)

    tab.navigate.emit(_request("open_view", view="nodegroups"))

    assert "only in EKS contexts" in tab.markdown() and window._view != "nodegroups"
    window.close()


def test_a_confirmed_change_runs_only_with_the_write_mode_on(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    runs: list = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda function, ok, *args, on_error: runs.append(
            (function, ok, args, on_error)
        ),
    )
    scale = _request("scale", namespace="ns", name="web", replicas=2)

    window.settings.write_mode = False
    tab.write.emit(scale)
    assert runs == [] and "Not run, the write mode is off" in tab.markdown()

    window.settings.write_mode = True
    tab.write.emit(scale)
    function, succeed, arguments, fail = runs[0]
    assert function.__name__ == "scale_deployment"
    assert arguments == ("prod", "ns", "web", 2)
    succeed(None)
    fail("forbidden")
    assert "Done: scale(" in tab.markdown() and "Failed: scale(" in tab.markdown()
    window.close()


def test_closing_the_window_stops_the_chat_and_a_language_change_retitles_it(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)

    window._retranslate()
    assert window.assistant_dock.panel.title.text() == "Assistant"
    window.close()

    assert tab.closed


def test_the_assistant_sees_the_list_the_selection_and_the_open_tab(
    monkeypatch,
) -> None:
    from kubescope.models import ClusterResource

    window, _messages = _open(monkeypatch)
    window.show()
    assert "Page: Cluster overview" in window._screen_snapshot()

    window._open_list_view("services")
    window._show_resources(
        ["ns"],
        [
            ClusterResource("ns", "Service", "web", ("ClusterIP",), "1d"),
            ClusterResource("ns", "Service", "api", ("ClusterIP",), "2d"),
        ],
    )
    window.search_input.setText("web")
    window.table.selectRow(0)
    window.table.setColumnHidden(0, True)  # what is hidden is not seen

    seen = window._screen_snapshot()
    assert "Page: the services list" in seen and 'Search: "web"' in seen
    assert "Rows shown: 1" in seen and "Selected row: web | ClusterIP" in seen
    assert "api" not in seen and "NAME | TYPE" in seen and "NAMESPACE" not in seen

    window.table.clearSelection()
    assert "Selected row" not in window._screen_snapshot()

    window._show_json_dialog("Service: web", {"spec": {"type": "ClusterIP"}})
    assert "an open tab, Service: web" in window._screen_snapshot()
    assert '"type": "ClusterIP"' in window._screen_snapshot()
    window.close()


def test_the_assistant_sees_the_log_that_is_open(monkeypatch) -> None:
    from kubescope.models import PodInfo
    from kubescope.views.log_tab import LogTab

    window, _messages = _open(monkeypatch)
    tab = LogTab("prod", PodInfo("ns", "p", "Running", 1, 1, "1m", ("app",)), "app")
    tab.set_logs("line one\nline two")
    window._add_viewer_tab(tab, "Logs: p")

    seen = window._screen_snapshot()

    assert "an open tab, Logs: p" in seen and "line two" in seen
    window.close()


def test_the_chat_answers_in_the_language_of_the_app_and_follows_a_change(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)
    window.settings.language = "pt"
    window._open_assistant()
    tab = _tab(window)
    assert "Answer in Portuguese" in tab.session.system

    window._load_settings_form()
    form = window.settings_ui
    form.languageCombo.setCurrentIndex(form.languageCombo.findData("de"))
    window._save_preferences()

    assert "Answer in German" in tab.session.system
    window.close()


def test_the_assistant_sees_the_numbers_of_the_overviews(monkeypatch) -> None:
    from kubescope.models import (
        ClusterOverview,
        EventInfo,
        KindSummary,
        WorkloadsOverview,
    )

    window, _messages = _open(monkeypatch)
    window._overview = ClusterOverview(namespaces=4, pods_total=9)
    window._show_page(0)
    assert "Namespaces: 4" in window._screen_snapshot()
    assert "Pods: 9 total" in window._screen_snapshot()

    window._workloads_overview = WorkloadsOverview(
        {"Deployment": KindSummary(3, 2, 0, 1)},
        (EventInfo("Warning", "kubelet", "ns", "Pod: p", "crash", 2, "1h", "1m"),),
    )
    window._show_page(4)
    seen = window._screen_snapshot()
    assert "Page: Workloads overview" in seen
    assert "Deployment: 3 in all, 2 healthy" in seen and "Pod: p in ns: crash" in seen
    window.close()


def test_the_assistant_moves_to_a_page_an_open_tab_and_the_logs_of_a_pod(
    monkeypatch,
) -> None:
    from kubescope.models import PodInfo

    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)

    for page, index in (("settings", 2), ("workloads_overview", 4), ("overview", 0)):
        tab.navigate.emit(_request("open_page", page=page))
        assert window.pages.currentIndex() == index

    window._show_json_dialog("Pod: web", {"a": 1})
    window._show_json_dialog("Service: api", {"b": 2})
    window._show_page(1)
    tab.navigate.emit(_request("switch_tab", title="WEB"))
    assert window.pages.currentIndex() == 3
    assert window.viewer_tabs.tabText(window.viewer_tabs.currentIndex()) == "Pod: web"
    tab.navigate.emit(_request("switch_tab", title="nothing"))
    assert "There is no open tab nothing." in tab.markdown()

    pods = [
        PodInfo(
            "ns",
            "api-1",
            "Running",
            1,
            2,
            "1m",
            ("app", "side"),
            init_containers=("init",),
        )
    ]
    runs: list = []

    def run(function, ok, *args, on_error=None):
        runs.append((function.__name__, args))
        if function.__name__ == "get_pods":
            ok((["ns"], pods))
        elif function.__name__ == "get_pod_logs":
            ok("a line")
        elif on_error is not None:
            on_error("boom")

    shown: list = []
    monkeypatch.setattr(window, "_run_action", run)
    monkeypatch.setattr(window, "_show_logs_dialog", lambda *a: shown.append(a))

    tab.navigate.emit(_request("show_logs", namespace="ns", pod="api-1"))
    tab.navigate.emit(
        _request("show_logs", namespace="ns", pod="api-1", container="side")
    )
    tab.navigate.emit(_request("show_logs", namespace="ns", pod="ghost"))

    assert [(pod.name, container, text) for pod, container, text in shown] == [
        ("api-1", "init", "a line"),
        ("api-1", "side", "a line"),
    ]
    assert ("get_pod_logs", ("prod", "ns", "api-1", "side")) in runs
    assert "There is no Pod ghost." in tab.markdown()
    window.close()


def test_a_failed_search_for_the_pod_is_said_in_the_chat(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda function, ok, *args, on_error: on_error("forbidden"),
    )

    tab.navigate.emit(_request("show_logs", namespace="ns", pod="x"))

    assert "forbidden" in tab.markdown()
    window.close()


def test_the_assistant_is_told_which_tabs_are_open(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)
    assert "Open tabs" not in window._screen_snapshot()

    window._show_json_dialog("Pod: web", {"a": 1})
    window._show_json_dialog("Service: api", {"b": 2})
    assert "Open tabs: Pod: web | Service: api (shown)" in window._screen_snapshot()

    window._show_page(1)
    assert "Open tabs: Pod: web | Service: api" in window._screen_snapshot()
    assert "(shown)" not in window._screen_snapshot()
    window.close()
