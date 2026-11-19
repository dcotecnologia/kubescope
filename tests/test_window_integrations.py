from unittest.mock import MagicMock

import pytest
from kubescope.sdk.timezone import set_timezone
from PySide6.QtCore import QEvent
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QMenu,
    QToolButton,
)

from kubescope import integrations
from kubescope import window as window_module
from kubescope.integrations import Found
from tests.test_window_flows import _ready_window, _wait_until

KEYS = {"access_key_id": "AKIA", "secret_access_key": "secret", "regions": "us-east-1"}


def _fake_menu(monkeypatch, shown) -> None:
    """A menu that does not open: it keeps the actions it was asked to show."""

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            shown.append(self.actions())
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)


@pytest.fixture(autouse=True)
def _local_time():
    yield
    set_timezone("auto")  # a test that chose a zone leaves none behind


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


def _sso(monkeypatch) -> integrations.Account:
    account = integrations.Account(
        "sso-modern", "aws", "modern", {"profile": "modern", "regions": "sa-east-1"}
    )
    monkeypatch.setattr(integrations, "sso_accounts", lambda: [account])
    monkeypatch.setattr(integrations, "aws_profiles", lambda: [("modern", "1111")])
    return account


def test_an_sso_profile_signed_in_counts_as_an_integration(window, monkeypatch) -> None:
    window.show()

    _sso(monkeypatch)
    window._sync_aws_menu()

    window._render_integrations()
    text = _texts(window)
    assert "1 accounts" in text
    tables = window.settings_ui.integrationsCard.findChildren(
        window_module.QTableWidget
    )
    assert tables[0].item(0, 0).text() == "modern"
    assert tables[0].item(0, 1).text() == "modern  1111  (SSO)"


def test_the_menu_of_an_sso_profile_finds_clusters_and_signs_in(
    window, monkeypatch
) -> None:
    account = _sso(monkeypatch)
    opened = []
    monkeypatch.setattr(
        window,
        "_open_account_dialog",
        lambda provider, found, profile="": opened.append((provider, found, profile)),
    )
    window._render_integrations()
    button = window.settings_ui.integrationsCard.findChildren(QToolButton)[0]
    actions = button.menu().actions()

    assert [action.text() for action in actions] == ["Find and add clusters", "Sign in"]
    actions[0].trigger()
    assert opened == [("aws", None, "modern")]

    ran = []
    monkeypatch.setattr(window_module, "run_login", lambda action: ran.append(action))
    actions[1].trigger()
    _wait_until(lambda: ran)
    assert ran[0].command[-1] == account.name


def test_coming_back_to_the_window_looks_for_a_new_sso_sign_in(
    window, monkeypatch
) -> None:
    window.show()
    assert window._aws_accounts == ()
    _sso(monkeypatch)

    window.changeEvent(QEvent(QEvent.Type.ActivationChange))
    window._sync_aws_menu()

    assert window._aws_accounts == ("sso-modern",)


def test_the_status_of_a_database_is_green_amber_red_or_neutral() -> None:
    colors = window_module._badge_colors
    good, warning, bad, other = (
        colors("available"),
        colors("modifying"),
        colors("incompatible-parameters"),
        colors("stopped"),
    )
    assert len({good, warning, bad, other}) == 4
    assert colors("backing-up") == warning and colors("failed") == bad


def test_the_integrations_page_follows_an_sso_sign_in_that_comes_and_goes(
    window, monkeypatch
) -> None:
    window._show_page(2)
    window._show_settings_section(4)
    assert "Not connected" in _texts(window)

    _sso(monkeypatch)  # the person signs in, and comes back to the window
    window._sync_aws_menu()
    assert "1 accounts" in _texts(window)

    window._sync_aws_menu()  # nothing changed: the page is left as it is
    assert "1 accounts" in _texts(window)

    monkeypatch.setattr(integrations, "sso_accounts", lambda: [])  # it runs out
    window._sync_aws_menu()
    assert "Not connected" in _texts(window)
