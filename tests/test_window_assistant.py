import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QFileDialog, QMessageBox

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
    tab = window.viewer_tabs.currentWidget()
    assert isinstance(tab, AssistantTab)
    return tab


def test_without_a_program_or_a_context_there_is_no_chat(monkeypatch) -> None:
    window, messages = _open(monkeypatch, found=())
    window._open_assistant()
    assert "No assistant program" in messages[-1][1] and window.viewer_tabs.count() == 0

    monkeypatch.setattr(window_module, "installed_assistants", lambda: [ONE])
    window.context_combo.clear()
    window._open_assistant()
    assert "Choose a context" in messages[-1][1] and window.viewer_tabs.count() == 0
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
    assert window.viewer_tabs.count() == 0 and not window.settings.assistant_consent

    window._open_assistant()
    assert window.settings.assistant_consent and window.settings.assistant == "one"
    assert window.viewer_tabs.count() == 1 and "sent to One" in asked[0]

    window._open_assistant()  # agreed already: it does not ask again
    assert window.viewer_tabs.count() == 2 and len(asked) == 2
    window.close()


def test_the_assistant_chosen_is_used_and_otherwise_the_first_one(monkeypatch) -> None:
    window, _messages = _open(monkeypatch, found=(ONE, TWO))

    window.settings.assistant = "two"
    assert window._assistant_program() is TWO
    window.settings.assistant = "gone"
    assert window._assistant_program() is ONE
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
    assert (
        window.search_regex_button.isChecked() and window.search_case_button.isChecked()
    )
    tab.navigate.emit(_request("search", text=""))
    assert not window.search_regex_button.isChecked()

    tab.navigate.emit(_request("switch_context", context="dev"))
    assert window._context() == "dev" and tab.context == "dev"
    assert window._viewer_contexts[tab] == "dev"
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


def test_the_chat_tab_is_closed_saved_and_themed_like_the_others(
    monkeypatch, tmp_path
) -> None:
    window, _messages = _open(monkeypatch)
    window._open_assistant()
    tab = _tab(window)
    tab.note("hello")
    target = tmp_path / "chat.txt"
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda *a, **k: (str(target), "")
    )

    window._save_viewer_tab()
    window._apply_theme()
    window._retranslate()
    window._close_viewer_tab(0)

    assert "hello" in target.read_text(encoding="utf-8")
    assert tab.closed and window.assistant_button.text() == "Assistant"
    window.close()
