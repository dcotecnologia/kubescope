import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtGui import QCloseEvent

from kubescope import integrations
from kubescope.dialogs import account_dialog
from kubescope.dialogs.account_dialog import AccountDialog
from kubescope.integrations import Account, Found, IntegrationError
from tests.qt import get_application
from tests.test_window_flows import _wait_until

application = get_application()


@pytest.fixture(autouse=True)
def _delete_the_windows():
    """Delete what a test shows before the application goes away."""
    before = set(application.topLevelWidgets())
    yield
    for widget in set(application.topLevelWidgets()) - before:
        widget.close()
        widget.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


@pytest.fixture(autouse=True)
def _state(monkeypatch):
    monkeypatch.setattr(integrations, "_accounts", {})
    monkeypatch.setattr(integrations, "_secrets", {})
    monkeypatch.setattr(
        integrations, "aws_profiles", lambda: [("work", "123456789012"), ("bare", "")]
    )
    opened = []
    yield opened


def _dialog(provider: str, account: Account | None = None) -> AccountDialog:
    dialog = AccountDialog(provider, account)
    return dialog


def test_an_aws_account_signs_in_with_a_profile_or_with_keys() -> None:
    dialog = _dialog("aws")
    assert (
        dialog.mode.currentData() == "profile"
        and dialog.name() == "Amazon Web Services"
    )

    dialog._profiles.setCurrentIndex(0)
    values = dialog.values()
    assert values["profile"] == "work" and values["secret_access_key"] == ""

    dialog._profiles.setCurrentIndex(-1)  # a profile that is not listed
    dialog._profiles.setEditText("typed")
    assert dialog.values()["profile"] == "typed"
    dialog._profiles.setEditText("")
    assert dialog.values()["profile"] == ""

    dialog.mode.setCurrentIndex(1)  # keys: the profile is left out
    dialog._edits["access_key_id"].setText("AKIA")
    keys = dialog.values()
    assert keys["profile"] == "" and keys["access_key_id"] == "AKIA"
    dialog.name_edit.setText(" work ")
    assert dialog.name() == "work"
    dialog.name_edit.setText("")
    assert dialog.name() == "Amazon Web Services"


def test_a_cloud_other_than_aws_has_no_mode_to_choose() -> None:
    dialog = _dialog("azure")
    assert dialog.mode.isHidden()
    assert dialog._edits["client_secret"].echoMode().name == "Password"
    assert dialog.values()["tenant_id"] == ""


def test_an_account_is_edited_with_what_was_saved(monkeypatch) -> None:
    account = integrations.add_account(
        "aws", "work", {"access_key_id": "AKIA", "secret_access_key": "s"}
    )
    dialog = _dialog("aws", account)

    assert not dialog.name_edit.isEnabled() and dialog.name() == "work"
    assert dialog.mode.currentData() == "keys"
    assert dialog._edits["secret_access_key"].text() == "s"

    profile = Account("aws-p", "aws", "p", {"profile": "bare"})
    assert _dialog("aws", profile).mode.currentData() == "profile"


def test_finding_needs_the_fields_then_lists_the_clusters(monkeypatch) -> None:
    dialog = _dialog("aws")
    dialog.mode.setCurrentIndex(1)
    dialog._find()
    assert "Access key ID is required" in dialog.status.text()

    hits = [Found("aws", "a", "us-east-1"), Found("aws", "b", "eu-west-1")]
    monkeypatch.setattr(integrations, "discover", lambda account, values: hits)
    dialog._edits["access_key_id"].setText("AKIA")
    dialog._edits["secret_access_key"].setText("s")
    dialog._find()
    _wait_until(lambda: dialog.clusters.count() == 2)
    _wait_until(lambda: dialog.find_button.isEnabled())

    assert dialog.add_button.isEnabled() and "2 clusters found" in dialog.status.text()
    assert dialog.chosen() == hits  # all of them, to begin with
    dialog.clusters.item(0).setSelected(False)
    assert dialog.chosen() == [hits[1]]
    assert dialog._worker is not None
    dialog.done_working()


def test_no_clusters_and_failures_are_told(monkeypatch) -> None:
    dialog = _dialog("gcp")
    dialog._edits["project_id"].setText("p")
    dialog._edits["key_file"].setText("/k.json")

    monkeypatch.setattr(integrations, "discover", lambda account, values: [])
    dialog._find()
    _wait_until(lambda: dialog.status.text() == "No clusters found.")
    assert not dialog.add_button.isEnabled()

    def refused(account, values):
        raise IntegrationError("denied")

    monkeypatch.setattr(integrations, "discover", refused)
    dialog._find()
    _wait_until(lambda: dialog.status.text() == "denied")

    def broken(account, values):
        raise RuntimeError("boom")

    monkeypatch.setattr(integrations, "discover", broken)
    dialog._find()
    _wait_until(lambda: dialog.status.text() == "Something went wrong.")
    dialog.done_working()


def test_the_key_file_is_picked_with_a_dialog(monkeypatch) -> None:
    dialog = _dialog("gcp")
    edit = dialog._edits["key_file"]
    monkeypatch.setattr(
        account_dialog.QFileDialog, "getOpenFileName", lambda *_a: ("/k.json", "")
    )
    dialog._browse(edit)
    assert edit.text() == "/k.json"
    monkeypatch.setattr(
        account_dialog.QFileDialog, "getOpenFileName", lambda *_a: ("", "")
    )
    dialog._browse(edit)
    assert edit.text() == "/k.json"


def test_the_labels_are_translated_and_unknown_ones_are_left_alone() -> None:
    assert account_dialog.label_of("Project ID") == "Project ID"
    assert account_dialog.label_of("Something else") == "Something else"


def test_closing_waits_for_a_search_that_is_running(monkeypatch) -> None:
    dialog = _dialog("gcp")
    dialog.done_working()  # nothing started
    dialog._edits["project_id"].setText("p")
    dialog._edits["key_file"].setText("/k.json")
    monkeypatch.setattr(integrations, "discover", lambda account, values: [])
    dialog._find()
    dialog.closeEvent(QCloseEvent())
    dialog.done(0)
    assert dialog._worker is not None and dialog._worker.isFinished()
    assert QEvent.Type.Close


def test_a_profile_picked_elsewhere_is_chosen_and_names_the_account() -> None:
    dialog = AccountDialog("aws", None, None, "work")

    assert dialog.name() == "work" and dialog.mode.currentData() == "profile"
    assert dialog.values()["profile"] == "work"
