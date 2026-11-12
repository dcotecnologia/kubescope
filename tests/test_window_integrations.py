from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QEvent, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QToolButton,
)

from kubescope import integrations
from kubescope import window as window_module
from kubescope.cluster import ClusterError
from kubescope.integrations import Found
from kubescope.models import RdsInstance, RdsLogFile, SsmTarget
from kubescope.utils.timezone import set_timezone
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


def _instance(identifier: str = "orders") -> RdsInstance:
    return RdsInstance(
        "107616205814", "us-east-1", identifier, "postgres", "15.4", "db.t3.medium",
        "available", 100, True, "orders.example.com", 5432, "work",
    )  # fmt: skip


def test_the_aws_part_of_the_menu_shows_only_with_an_aws_account(window) -> None:
    window.show()
    ui = window.ui
    assert not ui.navAwsSection.isVisible() and not window.nav_rds.isVisible()

    account = integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    assert ui.navAwsSection.isVisible() and window.nav_rds.isVisible()
    assert ui.navAwsSection.text() == "AWS" and window.nav_rds.text() == "RDS"

    window._show_page(5)
    window._remove_account(account)  # the last one: the page goes with it
    assert not ui.navAwsSection.isVisible() and not window.rds_submenu.isVisible()
    assert window.pages.currentIndex() == 0


def test_the_rds_instances_are_those_of_the_context_and_refresh_like_the_other_pages(
    window, monkeypatch
) -> None:
    asked = []
    monkeypatch.setattr(
        window_module,
        "get_rds_instances",
        lambda context, region="": asked.append((context, region)) or [_instance()],
    )
    integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    table = window.rds_ui.instancesTable
    assert table.columnWidth(0) > table.columnWidth(1)  # the name has room

    window.nav_rds_instances.click()
    _wait_until(lambda: table.rowCount() == 1)

    assert asked == [("prod", "us-east-1")] and window.pages.currentIndex() == 5
    assert window.nav_rds_instances.isChecked()
    assert window.ui.pageTitle.text() == "RDS instances"
    assert [table.item(0, column).text() for column in range(10)] == [
        "orders", "postgres", "15.4", "db.t3.medium", "available", "100 GiB",
        "Yes", "us-east-1", "107616205814", "orders.example.com",
    ]  # fmt: skip
    assert "1 instances" in window.rds_ui.noticeLabel.text()
    status = table.item(0, 4)
    assert status.data(window_module.BADGE_ROLE) == window_module._badge_colors(
        "available"
    )
    assert window.rds_refresh_button.isVisibleTo(window)  # the header button

    window._show_page(5)  # the same context: not asked again
    assert asked == [("prod", "us-east-1")]
    monkeypatch.setattr(
        window_module, "get_rds_instances", lambda context, region="": []
    )
    window._press_refresh()  # Ctrl+R, like the other pages
    _wait_until(lambda: table.rowCount() == 0)
    assert "0 instances" in window.rds_ui.noticeLabel.text()


def test_another_context_asks_again_and_a_stale_answer_is_dropped(
    window, monkeypatch
) -> None:
    monkeypatch.setattr(
        window_module,
        "get_rds_instances",
        lambda context, region="": [_instance(context)],
    )
    integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    window._show_page(5)
    table = window.rds_ui.instancesTable
    _wait_until(lambda: table.rowCount() == 1)

    window.context_combo.blockSignals(True)
    window.context_combo.addItem("other")
    window.context_combo.setCurrentIndex(1)
    window.context_combo.blockSignals(False)
    window._context_changed()  # on this page: it asks for the new context
    _wait_until(
        lambda: table.item(0, 0) is not None and table.item(0, 0).text() == "other"
    )

    window._rds_loaded(
        "prod", "us-east-1", [_instance("stale")]
    )  # not the selected context
    window._rds_failed("prod", "us-east-1", "late error")
    assert table.item(0, 0).text() == "other"
    assert not window.rds_ui.rdsBanner.isVisible()  # a late error is not told

    window._rds_failed(
        "other", "us-east-1", "This list is only available for Amazon EKS contexts"
    )
    assert table.rowCount() == 0
    assert window.rds_ui.rdsBanner.isVisibleTo(window.rds_ui.rdsBanner.parent())
    assert window.rds_ui.noticeLabel.text() == ""  # the banner says it, not the notice


def test_without_a_context_the_rds_page_asks_to_select_one(window) -> None:
    window.context_combo.clear()
    window._load_rds()
    assert window.rds_ui.noticeLabel.text() == "Select a context."
    assert window.rds_ui.instancesTable.rowCount() == 0


def _sso(monkeypatch) -> integrations.Account:
    account = integrations.Account(
        "sso-modern", "aws", "modern", {"profile": "modern", "regions": "sa-east-1"}
    )
    monkeypatch.setattr(integrations, "sso_accounts", lambda: [account])
    monkeypatch.setattr(integrations, "aws_profiles", lambda: [("modern", "1111")])
    return account


def test_an_sso_profile_signed_in_counts_as_an_integration(window, monkeypatch) -> None:
    window.show()
    assert not window.nav_rds.isVisible()

    _sso(monkeypatch)
    window._sync_aws_menu()
    assert window.ui.navAwsSection.isVisible() and window.nav_rds.isVisible()

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
    assert not window.nav_rds.isVisible()
    _sso(monkeypatch)

    window.changeEvent(QEvent(QEvent.Type.ActivationChange))
    assert window.nav_rds.isVisible() == window.isActiveWindow()
    window._sync_aws_menu()
    assert window.nav_rds.isVisible()


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


def _rds_window(window, monkeypatch):
    monkeypatch.setattr(
        window_module, "get_rds_instances", lambda context, region="": [_instance()]
    )
    integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    window._show_page(5)
    table = window.rds_ui.instancesTable
    _wait_until(lambda: table.rowCount() == 1)
    return table, table.visualItemRect(table.item(0, 0)).center()


def test_a_database_offers_details_and_a_forward_only_in_the_write_mode(
    window, monkeypatch
) -> None:
    table, position = _rds_window(window, monkeypatch)
    shown = []
    _fake_menu(monkeypatch, shown)

    window.settings.write_mode = False
    window._show_rds_menu(position)
    window._show_rds_menu(QPoint(5, 5000))  # below the rows: no menu
    assert [action.text() for action in shown[0]] == ["Details", "Logs"]
    assert len(shown) == 1

    window.settings.write_mode = True
    window._show_rds_menu(position)
    assert [action.text() for action in shown[1]] == [
        "Details",
        "Logs",
        "Forward with SSM",
    ]
    window._rds = None
    window._show_rds_menu(position)
    assert len(shown) == 2


def test_the_details_of_a_database_open_as_a_document(window, monkeypatch) -> None:
    table, _position = _rds_window(window, monkeypatch)
    document = {"DBInstanceIdentifier": "orders", "Engine": "postgres"}
    asked, shown = [], []
    monkeypatch.setattr(
        window_module,
        "get_rds_details",
        lambda context, identifier, region="": (
            asked.append((context, identifier, region)) or document
        ),
    )
    monkeypatch.setattr(
        window, "_show_json_dialog", lambda title, doc: shown.append((title, doc))
    )

    window._rds_row_details(0, 0)  # a double click on the row
    _wait_until(lambda: shown)
    window._rds_row_details(7, 0)  # a row that is not there
    window._rds = None
    window._rds_row_details(0, 0)

    assert asked == [("prod", "orders", "us-east-1")]
    assert shown == [("RDS: orders", document)]
    assert table.rowCount() == 1


def test_the_ssm_dialog_comes_filled_with_the_instance_the_region_and_the_profile(
    window, monkeypatch
) -> None:
    targets = [
        SsmTarget("i-0same", "bastion", "vpc-1", True),
        SsmTarget("i-0other", "", "vpc-2", False),
    ]
    monkeypatch.setattr(
        window_module, "get_ssm_targets", lambda context, vpc, region="": targets
    )
    seen = {}

    def fake_exec(dialog) -> int:
        target = dialog.findChild(QComboBox)
        region, profile = [
            edit
            for edit in dialog.findChildren(QLineEdit)
            if edit.parent() is dialog  # not the ones inside a spin box or a combo
        ]
        remote, local = dialog.findChildren(QSpinBox)
        box = dialog.findChild(QPlainTextEdit)
        buttons = {button.text(): button for button in dialog.findChildren(QPushButton)}
        _wait_until(lambda: target.count() == 2)
        seen["filled"] = (target.currentText(), region.text(), profile.text())
        seen["command"] = box.toPlainText()
        seen["hint"] = [label.text() for label in dialog.findChildren(QLabel)]
        target.setCurrentIndex(1)  # the other one
        region.setText("sa-east-1")
        profile.setText("lab")
        remote.setValue(5433)
        local.setValue(15433)
        seen["changed"] = box.toPlainText()
        target.setEditText("i-0typed")  # or one typed by hand
        seen["typed"] = box.toPlainText()
        buttons["Copy"].click()
        seen["clipboard"] = QApplication.clipboard().text()
        buttons["Close"].click()
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._forward_rds(_instance())

    assert seen["filled"] == ("bastion  (i-0same)", "us-east-1", "work")
    assert "i-0same" in seen["command"] and "--region us-east-1" in seen["command"]
    assert (
        "--profile work" in seen["command"]
        and "<EC2-INSTANCE-ID>" not in seen["command"]
    )
    assert any("first is in the VPC" in text for text in seen["hint"])
    assert "i-0other" in seen["changed"] and "--region sa-east-1" in seen["changed"]
    assert "--profile lab" in seen["changed"] and "15433" in seen["changed"]
    assert "i-0typed" in seen["typed"] and seen["clipboard"] == seen["typed"]


def test_the_ssm_dialog_says_when_no_instance_can_be_reached(
    window, monkeypatch
) -> None:
    results = iter([[SsmTarget("i-0far", "far", "vpc-9", False)], "boom"])
    hints = []

    def targets(context, vpc, region=""):
        answer = next(results)
        if isinstance(answer, str):
            raise ClusterError(answer)
        return answer

    monkeypatch.setattr(window_module, "get_ssm_targets", targets)

    def fake_exec(dialog) -> int:
        target = dialog.findChild(QComboBox)
        target.setEditText("i-0mine")  # typed before the answer comes
        _wait_until(
            lambda: any(
                "type the ID" in label.text() or label.text() == "boom"
                for label in dialog.findChildren(QLabel)
            )
        )
        hints.append(
            (
                target.currentText(),
                [label.text() for label in dialog.findChildren(QLabel)],
            )
        )
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._forward_rds(_instance())
    window._forward_rds(_instance())

    assert hints[0][0] == "i-0mine"  # what was typed stays
    assert any("type the ID" in text for text in hints[0][1])
    assert "boom" in hints[1][1]


def test_the_logs_of_a_database_are_picked_and_read_in_a_tab(
    window, monkeypatch
) -> None:
    set_timezone("Asia/Tokyo")  # the zone of the person, not the one of the computer
    _rds_window(window, monkeypatch)
    files = [
        RdsLogFile("error/postgresql.log.2026-11-12-03", 2048, 1_794_540_600_000),
        RdsLogFile("b", 0, 1),
    ]
    monkeypatch.setattr(
        window_module, "get_rds_log_files", lambda context, ident, region="": files
    )
    texts = ["first read", "second read"]
    asked = []
    monkeypatch.setattr(
        window_module,
        "get_rds_log",
        lambda context, ident, name, region="": (
            asked.append((context, ident, name, region)) or texts.pop(0)
        ),
    )
    picked = []
    monkeypatch.setattr(
        window,
        "_pick_item",
        lambda title, label, items: picked.append(items) or (items[0], True),
    )

    window._rds_logs(_instance())
    _wait_until(lambda: asked)
    tab = window.viewer_tabs.currentWidget()
    _wait_until(lambda: "first read" in tab.ui.logText.toPlainText())

    # 2026-11-13 03:30 UTC, shown in the zone of the settings (Tokyo)
    assert picked[0][0].endswith("(2 KiB, 2026-11-13 12:30)")
    assert asked == [
        ("prod", "orders", "error/postgresql.log.2026-11-12-03", "us-east-1")
    ]
    assert window.viewer_tabs.tabText(window.viewer_tabs.currentIndex()).startswith(
        "Logs: orders / error/postgresql"
    )
    tab.ui.refreshButton.click()  # reads it again
    _wait_until(lambda: len(asked) == 2)
    _wait_until(lambda: "second read" in tab.ui.logText.toPlainText())


def test_a_log_that_cannot_be_read_or_closed_and_a_database_without_logs(
    window, monkeypatch
) -> None:
    messages = []
    monkeypatch.setattr(
        window, "_show_message", lambda icon, title, text: messages.append(text)
    )
    window._choose_rds_log(_instance(), [])
    assert "orders has no log files." in messages[0]

    file = RdsLogFile("x.log", 0, 1)
    monkeypatch.setattr(window, "_pick_item", lambda *_a: ("x.log  (0 KiB)", False))
    window._choose_rds_log(_instance(), [file])  # cancelled: nothing opens
    assert window.viewer_tabs.count() == 0

    def broken(context, ident, name, region=""):
        raise ClusterError("denied")

    monkeypatch.setattr(window_module, "get_rds_log", broken)
    window._open_rds_log(_instance(), "x.log")
    tab = window.viewer_tabs.currentWidget()
    _wait_until(lambda: "denied" in tab.ui.logText.toPlainText() or not tab.busy)

    tab.closed = True  # a closed tab is left alone
    window._read_rds_log(tab, "x.log", "us-east-1")
    tab.closed = False
    tab.busy = True
    window._read_rds_log(tab, "x.log", "us-east-1")  # and so is one still reading


def test_the_rds_search_hides_the_instances_that_do_not_match(
    window, monkeypatch
) -> None:
    monkeypatch.setattr(
        window_module,
        "get_rds_instances",
        lambda context, region="": [
            _instance("orders"),
            _instance("Billing"),
            _instance("users"),
        ],
    )
    integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    window._show_page(5)
    ui = window.rds_ui
    table = ui.instancesTable
    _wait_until(lambda: table.rowCount() == 3)
    hidden = lambda: [table.isRowHidden(row) for row in range(3)]  # noqa: E731
    assert "3 instances" in ui.noticeLabel.text() and hidden() == [False] * 3

    ui.searchInput.setText("bill")  # in any column, whatever the case
    assert hidden() == [True, False, True]
    assert "1 of 3 instances" in ui.noticeLabel.text()

    window.rds_case_button.setChecked(True)  # now the case matters
    assert hidden() == [True, True, True]
    window.rds_case_button.setChecked(False)

    ui.searchInput.setText("^(orders|users)$")
    assert hidden() == [False, False, False] or "of 3" in ui.noticeLabel.text()
    window.rds_regex_button.setChecked(True)
    assert hidden() == [False, True, False]

    ui.searchInput.setText("(")  # a regular expression that does not compile
    assert ui.searchInput.toolTip() and hidden() == [False] * 3

    ui.searchInput.setText("")
    window.rds_regex_button.setChecked(False)
    assert ui.searchInput.toolTip() == "" and "3 instances" in ui.noticeLabel.text()
    window._retranslate()
    assert window.rds_case_button.toolTip() == "Match case"


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


def test_the_aws_menu_stays_while_aws_is_in_use_even_if_the_sign_in_ran_out(
    window, monkeypatch
) -> None:
    window.show()
    ui = window.ui
    monkeypatch.setattr(window_module, "is_eks_context", lambda context: False)
    window._sync_aws_menu()
    assert not ui.navAwsSection.isVisible()  # nothing of AWS on this computer

    expired = integrations.SsoProfile("work", "1111", "us-east-1", False)
    monkeypatch.setattr(integrations, "sso_profiles", lambda: [expired])
    window._sync_aws_menu()
    assert ui.navAwsSection.isVisible() and window.nav_rds.isVisible()  # a profile
    assert "Not connected" in _texts(window)  # none is signed in, and it says so

    monkeypatch.setattr(integrations, "sso_profiles", lambda: [])
    window._sync_aws_menu()
    assert not ui.navAwsSection.isVisible()

    monkeypatch.setattr(window_module, "is_eks_context", lambda context: True)
    window._context_changed()  # an EKS cluster selected is AWS in use
    assert ui.navAwsSection.isVisible() and window.nav_rds.isVisible()
    window.context_combo.clear()  # with no context selected, it is not
    window._sync_aws_menu()
    assert not ui.navAwsSection.isVisible()


def test_the_region_select_starts_in_the_region_of_the_context_and_reloads_on_change(
    window, monkeypatch
) -> None:
    asked = []
    monkeypatch.setattr(
        window_module,
        "get_rds_instances",
        lambda context, region="": asked.append((context, region)) or [_instance()],
    )
    monkeypatch.setattr(window_module, "context_region", lambda context: "sa-east-1")
    integrations.add_account("aws", "work", KEYS)
    window._save_accounts()
    combo = window.rds_ui.regionCombo
    table = window.rds_ui.instancesTable
    assert combo.count() > 20 and combo.findData("sa-east-1") >= 0

    window._show_page(5)
    _wait_until(lambda: table.rowCount() == 1)
    assert combo.currentData() == "sa-east-1"  # the one of the context
    assert asked == [("prod", "sa-east-1")]

    combo.setCurrentIndex(combo.findData("eu-west-1"))  # another is chosen
    _wait_until(lambda: asked[-1] == ("prod", "eu-west-1"))
    window._show_page(5)
    assert asked.count(("prod", "eu-west-1")) == 1  # the same choice: not again

    monkeypatch.setattr(
        window_module, "context_region", lambda context: "us-gov-west-1"
    )
    window.context_combo.blockSignals(True)
    window.context_combo.addItem("gov")
    window.context_combo.setCurrentIndex(1)
    window.context_combo.blockSignals(False)
    window._context_changed()  # another context: its region, even one not listed
    _wait_until(lambda: asked[-1] == ("gov", "us-gov-west-1"))
    assert (
        combo.currentData() == "us-gov-west-1" and combo.itemData(0) == "us-gov-west-1"
    )

    _wait_until(lambda: window._rds_region == "us-gov-west-1")
    window._rds_loaded("gov", "eu-west-1", [])  # an answer for a region left behind
    window._rds_failed("gov", "eu-west-1", "late")
    assert window.rds_ui.noticeLabel.text() != "late"
    assert window._rds_region == "us-gov-west-1"


def test_an_error_of_the_rds_list_is_a_banner_with_the_original_one_click_away(
    window, monkeypatch
) -> None:
    window.show()
    window._show_page(5)
    ui = window.rds_ui
    monkeypatch.setattr(
        window_module, "get_rds_instances", lambda context, region="": []
    )
    window._rds_failed("prod", "us-east-1", "placeholder")  # lets the page settle
    original = (
        "An error occurred (AccessDenied) when calling DescribeDBInstances: User: "
        "arn:aws:sts::1:x is not authorized to perform: rds:DescribeDBInstances "
        "with an explicit deny in a service control policy: arn:aws:organizations::1:p"
    )

    window._rds_failed("prod", "us-east-1", original)

    assert ui.rdsBanner.isVisible()
    assert ui.bannerLabel.text().startswith("Access denied. Your AWS identity")
    assert "perform rds:DescribeDBInstances" in ui.bannerLabel.text()
    assert ui.bannerDetails.isHidden() and ui.bannerDetails.text() == original

    ui.detailsButton.click()  # the original text, one click away
    assert not ui.bannerDetails.isHidden() and ui.detailsButton.text() == "Hide"
    ui.detailsButton.click()
    assert ui.bannerDetails.isHidden() and ui.detailsButton.text() == "Details"

    ui.dismissButton.click()
    assert not ui.rdsBanner.isVisible()

    window._rds_failed("prod", "us-east-1", "")  # an error without any text
    assert ui.rdsBanner.isVisible() and not ui.detailsButton.isVisible()

    window._load_rds()  # asking again takes the banner away
    assert not ui.rdsBanner.isVisible()
