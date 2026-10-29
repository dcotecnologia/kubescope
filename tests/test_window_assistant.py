import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QMessageBox

from kubescope import window as window_module
from kubescope.assistant import actions
from kubescope.assistant.runner import Assistant
from kubescope.i18n import apply_language
from kubescope.views.assistant_tab import AssistantTab
from tests.test_window_flows import _ready_window

ONE = Assistant("one", "One", "one-ai", lambda m, s: [], lambda line: ("", ""))
TWO = Assistant("two", "Two", "two-ai", lambda m, s: [], lambda line: ("", ""))


@pytest.fixture(autouse=True)
def english_again():
    """A test that changes the language of the app leaves English behind."""
    yield
    apply_language("en")


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


def _answer_the_guide(monkeypatch, button: str) -> list:
    """Make the guide be answered with a click on one of its buttons; the boxes
    it showed are returned."""
    boxes: list = []

    def answer(box) -> int:
        boxes.append(box)
        for one in box.buttons():
            if one.text() == button:
                one.click()
        return 0

    monkeypatch.setattr(window_module.QMessageBox, "exec", answer)
    return boxes


def test_without_a_context_there_is_no_chat(monkeypatch) -> None:
    window, messages = _open(monkeypatch)
    window.context_combo.clear()

    window._open_assistant()

    assert "Choose a context" in messages[-1][1] and window._assistant_tab is None
    window.close()


def test_without_a_program_the_button_guides_to_the_setup(monkeypatch) -> None:
    window, _messages = _open(monkeypatch, found=())
    boxes = _answer_the_guide(monkeypatch, "Close")

    window.assistant_dock.bubble.click()  # the button is there, to be found

    (box,) = boxes
    assert window.assistant_dock.bubble.isVisibleTo(window)
    assert box.text() == "Gabi needs Claude Code or Codex."
    steps = box.informativeText()
    for phrase in (
        "found neither of them",
        "Install Claude Code (claude) or Codex (codex) and sign in",
        "tell KubeScope where in Settings",
        "asks for no credentials and stores none",
    ):
        assert phrase in steps
    assert {one.text() for one in box.buttons()} == {
        "Open Settings",
        "How to set it up",
        "Close",
    }
    assert window._assistant_tab is None and not window.assistant_dock.is_open
    assert window.pages.currentIndex() != 2
    window.close()


def test_the_guide_opens_the_settings_at_the_card_of_the_assistant(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch, found=())
    window.show()
    _answer_the_guide(monkeypatch, "Open Settings")

    window._open_assistant()
    for _ in range(5):
        window_module.QApplication.processEvents()

    assert window.pages.currentIndex() == 2
    card = window.settings_ui.assistantCard
    scroll = window.settings_ui.settingsScroll
    content = scroll.widget()
    assert content is not None
    top = card.mapTo(content, card.rect().topLeft()).y()
    assert scroll.verticalScrollBar().value() <= top  # the card is in view
    window.close()


def test_the_guide_links_to_the_instructions(monkeypatch) -> None:
    window, _messages = _open(monkeypatch, found=())
    opened: list[str] = []
    monkeypatch.setattr(
        window_module.QDesktopServices,
        "openUrl",
        lambda url: opened.append(url.toString()),
    )
    _answer_the_guide(monkeypatch, "How to set it up")

    window._open_assistant()

    assert opened == [f"{window_module.PROJECT_URL}#gabi-the-assistant"]
    window.close()


def test_the_guide_says_when_a_path_that_was_set_is_no_longer_a_program(
    monkeypatch, tmp_path
) -> None:
    from kubescope.assistant import runner

    monkeypatch.setattr(runner, "CUSTOM_PROGRAMS", {})
    window, _messages = _open(monkeypatch, found=())
    window.settings.assistant_programs = {"claude": str(tmp_path / "gone")}
    boxes = _answer_the_guide(monkeypatch, "Close")
    monkeypatch.setattr(window_module, "is_available_assistant", lambda one: False)

    window._open_assistant()

    assert "The path set for Claude is not a program that can be run." in (
        boxes[0].informativeText()
    )
    window.settings.assistant_programs = {}
    window._open_assistant()
    assert "The path set for" not in boxes[1].informativeText()
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
    assert window.assistant_dock.panel.title.text() == "Gabi"
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


def test_the_panel_state_is_read_at_the_start_and_written_when_it_changes(
    monkeypatch,
) -> None:
    from kubescope.settings import Settings

    saved = Settings()
    saved.assistant_panel = {"width": 500, "height": 520, "floating": True}
    saved.save()
    window, _messages = _open(monkeypatch)

    dock = window.assistant_dock
    assert dock.is_floating and dock._size.width() == 500

    dock.set_floating(False)
    assert "floating" not in window.settings.assistant_panel  # only "out" is kept
    assert Settings().assistant_panel.get("width") == 500
    window.close()


def test_the_settings_say_the_assistant_uses_the_client_of_the_computer(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)

    hint = window.settings_ui.assistantHint.text()

    assert "already installed on this computer" in hint
    assert "asks you for no credentials and stores none" in hint
    window.close()


def test_the_settings_take_the_path_of_a_program_the_system_does_not_find(
    monkeypatch, tmp_path
) -> None:
    from kubescope.assistant import runner

    monkeypatch.setattr(runner, "CUSTOM_PROGRAMS", {})
    program = tmp_path / "claude"
    program.write_text("#!/bin/sh\n")
    program.chmod(0o755)
    window, _messages = _open(monkeypatch)
    monkeypatch.setattr(window_module, "ASSISTANTS", {"one": ONE, "two": TWO})
    window._load_settings_form()
    paths = window._assistant_paths
    assert set(paths) == {"one", "two"}
    assert paths["one"].placeholderText().startswith("Not found")

    paths["one"].setText("/nowhere/one-ai")  # not a program
    window._save_preferences()
    assert (
        "is not a program that can be run (One)"
        in window.settings_ui.noticeLabel.text()
    )
    assert window.settings.assistant_programs == {} and runner.CUSTOM_PROGRAMS == {}

    paths["one"].setText(str(program))
    window._save_preferences()
    assert window.settings.assistant_programs == {"one": str(program)}
    assert {"one": str(program)} == runner.CUSTOM_PROGRAMS

    window._load_settings_form()  # it is shown again, and the other is empty
    assert window._assistant_paths["one"].text() == str(program)
    window._assistant_paths["one"].setText("")
    window._save_preferences()
    assert window.settings.assistant_programs == {} and runner.CUSTOM_PROGRAMS == {}
    window.close()


def test_browsing_for_a_program_fills_its_path(monkeypatch, tmp_path) -> None:
    window, _messages = _open(monkeypatch)
    window._load_settings_form()
    edit = window._assistant_paths["claude"]
    chosen = [str(tmp_path / "claude"), ""]
    monkeypatch.setattr(
        window_module.QFileDialog, "getOpenFileName", lambda *_a: (chosen.pop(0), "")
    )

    window._browse_program(edit, "Claude")
    assert edit.text() == str(tmp_path / "claude")
    window._browse_program(edit, "Claude")  # cancelled: nothing changes
    assert edit.text() == str(tmp_path / "claude")
    window.close()


def test_the_paths_kept_are_used_from_the_start(monkeypatch, tmp_path) -> None:
    from kubescope.assistant import runner
    from kubescope.settings import Settings

    monkeypatch.setattr(runner, "CUSTOM_PROGRAMS", {})
    saved = Settings()
    saved.assistant_programs = {"claude": str(tmp_path / "claude")}
    saved.save()

    window, _messages = _open(monkeypatch)

    assert {"claude": str(tmp_path / "claude")} == runner.CUSTOM_PROGRAMS
    window.close()


def test_the_assistant_is_told_the_mode_and_follows_it_when_it_changes(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)
    window.settings.write_mode = False
    window._open_assistant()
    tab = _tab(window)
    assert "READ-ONLY mode" in tab.session.system
    assert "- scale [" not in tab.session.system

    window._load_settings_form()
    window.settings_ui.writeModeCheck.setChecked(True)
    window._save_preferences()
    assert "WRITE mode" in tab.session.system and "- scale [" in tab.session.system

    window.settings_ui.writeModeCheck.setChecked(False)
    window._save_preferences()
    assert "READ-ONLY mode" in tab.session.system
    assert "- delete [" not in tab.session.system
    window.close()


def test_the_corner_of_the_footer_is_left_to_the_button_of_the_assistant(
    monkeypatch,
) -> None:
    from kubescope.views.assistant_panel import BUBBLE, MARGIN

    window, _messages = _open(monkeypatch)
    footer = window.ui.footerRow
    links = window.ui.appFooterLayout
    original = {
        footer: footer.contentsMargins().right(),
        links: links.contentsMargins().right(),
    }
    room = BUBBLE + MARGIN
    assert footer.contentsMargins().right() == original[footer]  # on: room was made
    window._load_settings_form()
    window.settings_ui.assistantCheck.setChecked(False)
    window._save_preferences()
    assert footer.contentsMargins().right() == original[footer] - room
    assert links.contentsMargins().right() == original[links] - room

    window.settings_ui.assistantCheck.setChecked(True)
    window._save_preferences()
    assert footer.contentsMargins().right() == original[footer]
    assert links.contentsMargins().right() == original[links]
    window.close()


def test_the_side_menu_width_is_read_at_the_start_and_written_when_it_changes(
    monkeypatch,
) -> None:
    from kubescope.settings import Settings

    saved = Settings()
    saved.sidebar_width = 400
    saved.save()
    window, _messages = _open(monkeypatch)
    assert window.ui.sidebar.maximumWidth() == 400

    window.sidebar_resizer.set_width(250)
    window.sidebar_resizer.width_changed.emit(250)
    assert Settings().sidebar_width == 250

    window.sidebar_resizer.width_changed.emit(window_module.SIDEBAR_WIDTH)
    assert Settings().sidebar_width == 0  # the usual width is kept as none
    window.close()


def test_the_side_menu_starts_240_wide_and_goes_back_to_it(monkeypatch) -> None:
    window, _messages = _open(monkeypatch)

    assert window_module.SIDEBAR_WIDTH == 240
    assert window.ui.sidebar.maximumWidth() == 240

    window.sidebar_resizer.set_width(400)
    window.sidebar_resizer.grip.reset.emit()
    assert window.ui.sidebar.maximumWidth() == 240
    window.close()


def test_every_section_of_the_menu_starts_open_and_what_is_closed_is_kept(
    monkeypatch,
) -> None:
    from kubescope.settings import Settings

    window, _messages = _open(monkeypatch)
    sections = (window.submenu, window.network_submenu, window.config_submenu)
    assert all(section.maximumHeight() > 0 for section in sections)
    assert Settings().menu_collapsed == []

    window.nav_network.click()  # close Network
    window._submenus[window.network_submenu].setCurrentTime(
        window._submenus[window.network_submenu].duration()
    )
    assert window.network_submenu.maximumHeight() == 0
    assert Settings().menu_collapsed == ["network"]

    window.nav_config.click()
    assert Settings().menu_collapsed == ["config", "network"]
    window.nav_network.click()  # open it again
    assert Settings().menu_collapsed == ["config"]
    window.close()

    again, _messages = _open(monkeypatch)  # the next run: Config is still closed
    assert again.config_submenu.maximumHeight() == 0
    assert (
        again.submenu.maximumHeight() > 0 and again.network_submenu.maximumHeight() > 0
    )
    again.close()


def test_each_entry_of_the_side_menu_carries_its_whole_name_as_a_tip(
    monkeypatch,
) -> None:
    window, _messages = _open(monkeypatch)

    for button in window._nav_views.values():
        assert button.toolTip() == button.text() != ""
    window._retranslate()
    assert window.nav_pods.toolTip() == window.nav_pods.text()
    window.close()


@pytest.fixture
def preview_tool():
    """The tool that takes the screenshots, which is not a package.

    It puts a fake cluster in the window module when it is loaded, which
    is taken back when the test is over.
    """
    import importlib.util
    from pathlib import Path

    kept = dict(vars(window_module))
    path = Path(__file__).resolve().parent.parent / "tools" / "preview.py"
    spec = importlib.util.spec_from_file_location("kubescope_preview", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        for name, value in kept.items():
            if getattr(window_module, name, None) is not value:
                setattr(window_module, name, value)


def test_the_screenshot_opens_what_is_closed_and_leaves_open_what_is_open(
    monkeypatch, preview_tool
) -> None:
    from PySide6.QtWidgets import QApplication

    preview = preview_tool
    window, _messages = _open(monkeypatch)
    sections = (window.submenu, window.network_submenu, window.config_submenu)
    window.nav_config.click()  # one of them closed by the person
    window._submenus[window.config_submenu].setCurrentTime(
        window._submenus[window.config_submenu].duration()
    )
    assert window.config_submenu.maximumHeight() == 0
    application = QApplication.instance()
    assert application is not None

    preview.open_menus(application, window)
    preview.open_menus(application, window)  # again: nothing is closed

    assert all(section.maximumHeight() > 0 for section in sections)
    window.close()


def test_changing_the_theme_repaints_the_chat_that_is_open(monkeypatch) -> None:
    from kubescope import theme

    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    tab.note("a note")
    light = tab._bubbles[0].styleSheet()

    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    window._apply_theme()

    assert tab._bubbles[0].styleSheet() != light
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)
    window.close()
