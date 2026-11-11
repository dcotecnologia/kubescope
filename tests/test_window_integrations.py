from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QDialog, QToolButton

from kubescope import integrations
from kubescope import window as window_module
from kubescope.integrations import Found
from tests.test_window_flows import _ready_window, _wait_until

KEYS = {"access_key_id": "AKIA", "secret_access_key": "secret", "regions": "us-east-1"}


@pytest.fixture
def window(monkeypatch):
    monkeypatch.setattr(integrations, "_accounts", {})
    monkeypatch.setattr(integrations, "_secrets", {})
    monkeypatch.setattr(integrations, "find_program", lambda name: f"/bin/{name}")
    shown = _ready_window(monkeypatch)
    loaded: list[int] = []
    monkeypatch.setattr(shown, "_load_contexts", lambda: loaded.append(1))
    shown.loaded = loaded  # type: ignore[attr-defined]
    shown._load_settings_form()
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def _texts(window) -> str:
    layout = window.settings_ui.integrationsLayout
    return " ".join(
        label.text()
        for index in range(layout.count())
        for label in (
            layout.itemAt(index).widget().findChildren(window_module.QLabel)
            if layout.itemAt(index).widget() is not None
            else []
        )
    )


def test_the_section_has_a_part_for_each_cloud_and_the_local_files(window) -> None:
    text = _texts(window)
    for part in ("AMAZON EKS", "AZURE AKS", "GOOGLE GKE", "LOCAL KUBECONFIGS"):
        assert part in text
    assert "Not connected" in text and "1 sources" in text
    assert (
        window.settings_ui.integrationsCard.isVisibleTo(
            window.settings_ui.settingsContent
        )
        is False
    )  # shown only in its own section
    window._show_settings_section(4)
    assert window.settings_ui.integrationsCard.isVisibleTo(
        window.settings_ui.settingsContent
    )


def _dialog(monkeypatch, found: list[Found], **values: str):
    """A dialog that is accepted at once with these values and clusters."""
    dialog = MagicMock()
    dialog.exec.return_value = QDialog.DialogCode.Accepted
    dialog.values.return_value = values
    dialog.name.return_value = "work"
    dialog.chosen.return_value = found
    dialog.account.id = "aws-new"
    monkeypatch.setattr(window_module, "AccountDialog", lambda *_a: dialog)
    return dialog


def test_an_account_added_is_saved_without_its_secret_and_its_clusters_plugged(
    window, monkeypatch
) -> None:
    hits = [Found("aws", "a", "us-east-1")]
    _dialog(monkeypatch, hits, **KEYS)
    plugged = []
    monkeypatch.setattr(
        integrations,
        "plug",
        lambda found, account, values: plugged.append(found) or found,
    )
    monkeypatch.setattr(integrations, "kubeconfig_files", lambda: ["/x.kubeconfig"])

    window._open_account_dialog("aws", None)
    _wait_until(lambda: plugged)
    _wait_until(lambda: window.loaded)

    saved = window.settings.integration_accounts
    assert saved[0]["id"] == "aws-new" and saved[0]["name"] == "work"
    assert "secret_access_key" not in saved[0]["fields"]
    assert plugged == [hits]
    text = _texts(window)
    assert "1 accounts" in text
    assert "1 clusters added" in window.settings_ui.noticeLabel.text()


def test_an_account_without_chosen_clusters_is_only_listed(window, monkeypatch) -> None:
    _dialog(monkeypatch, [], profile="work", regions="us-east-1")
    window._open_account_dialog("aws", None)
    assert "1 accounts" in _texts(window)


def test_a_dialog_that_is_cancelled_changes_nothing(window, monkeypatch) -> None:
    dialog = _dialog(monkeypatch, [])
    dialog.exec.return_value = QDialog.DialogCode.Rejected
    window._open_account_dialog("aws", None)
    assert integrations.accounts() == []


def test_the_keys_of_an_account_are_typed_again_from_its_menu(
    window, monkeypatch
) -> None:
    account = integrations.add_account("aws", "work", KEYS)
    _dialog(monkeypatch, [], **{**KEYS, "regions": "sa-east-1"})
    window._render_integrations()

    window._open_account_dialog("aws", account)

    assert integrations.accounts()[0].fields["regions"] == "sa-east-1"


def test_the_rows_name_the_account_and_a_failure_is_told(window, monkeypatch) -> None:
    integrations.load(
        [
            {"id": "aws-1", "provider": "aws", "name": "a", "fields": {"profile": "p"}},
            {"id": "aws-2", "provider": "aws", "name": "k", "fields": KEYS},
            {
                "id": "az-1",
                "provider": "azure",
                "name": "z",
                "fields": {"subscription_id": "sub"},
            },
            {
                "id": "gcp-1",
                "provider": "gcp",
                "name": "g",
                "fields": {"project_id": "proj"},
            },
        ]
    )
    monkeypatch.setattr(integrations, "aws_profiles", lambda: [("p", "123456789012")])
    window._render_integrations()

    layout = window.settings_ui.integrationsLayout
    tables = [
        layout.itemAt(index).widget().findChild(window_module.QTableWidget)
        for index in range(layout.count())
        if layout.itemAt(index).widget() is not None
    ]
    cells = [
        table.item(row, 1).text()
        for table in tables
        if table is not None
        for row in range(table.rowCount())
    ]
    assert cells[0] == "p  123456789012"
    assert cells[1].startswith("AKIA") and "type the keys again" in cells[1]
    assert "sub" in cells[2] and "proj" in cells[3]

    window._integration_failed("denied")
    assert window.settings_ui.noticeLabel.text() == "denied"


def test_removing_an_account_forgets_it_and_its_clusters(window, monkeypatch) -> None:
    account = integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    window._render_integrations()
    buttons = window.settings_ui.integrationsCard.findChildren(QToolButton)
    assert buttons  # the menu of the account

    window._remove_account(account)

    assert integrations.accounts() == [] and window.settings.integration_accounts == []
    assert window.loaded


def test_a_profile_account_signs_in_from_its_menu(window, monkeypatch) -> None:
    account = integrations.add_account(
        "aws", "work", {"profile": "work", "regions": "us-east-1"}
    )
    ran = []
    monkeypatch.setattr(
        window_module, "run_login", lambda action: ran.append(action.command)
    )

    window._sign_in_account(account)
    _wait_until(lambda: ran)
    _wait_until(lambda: window.settings_ui.noticeLabel.text() == "Signed in.")

    assert ran == [["aws", "sso", "login", "--profile", "work"]]
    window._show_settings_section(4)
    window._local_section()  # the button that goes to the kubeconfig files
    assert window.settings.kubeconfig_files == []
