import time

from PySide6.QtWidgets import QApplication, QDialog

from kubescope.dialogs import update_dialog
from kubescope.dialogs.update_dialog import UpdateDialog, UpdateWorker
from kubescope.utils.selfupdate import Install, UpdateError
from kubescope.utils.updates import Asset, Release
from tests.qt import get_application

DEB = Install("deb", update_dialog.find_asset.__globals__["DEB_EXECUTABLE"])
ASSET = Asset("kubescope_0.7.0_amd64.deb", "https://x", "0" * 64)
RELEASE = Release(
    "0.7.0", "https://github.test/tag", "# 0.7.0\n\n- Fixed a thing", (ASSET,)
)


def wait_until(condition, receiver, seconds: float = 5) -> None:
    """Deliver the queued signals of the worker to the dialog only, so a window
    that an earlier test left behind does not get its late events here."""
    deadline = time.monotonic() + seconds
    while not condition() and time.monotonic() < deadline:
        QApplication.sendPostedEvents(receiver)
        time.sleep(0.01)
    assert condition()


def test_the_dialog_confirms_the_versions_and_shows_the_notes(qtbot_free=None) -> None:
    get_application()
    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)

    assert dialog.can_update
    assert "0.6.2" in dialog.findChildren(type(dialog.message))[0].text()
    assert "0.7.0" in dialog.findChildren(type(dialog.message))[0].text()
    assert "Fixed a thing" in dialog.notes.toPlainText()
    assert dialog.start_button.text() == "Update and restart"
    assert dialog.message.isHidden()


def test_a_release_without_notes_says_so() -> None:
    get_application()
    dialog = UpdateDialog(None, "0.6.2", Release("0.7.0", "u", "", (ASSET,)), DEB)

    assert "No release notes" in dialog.notes.toPlainText()


def test_an_installation_that_cannot_update_opens_the_release_page(monkeypatch) -> None:
    get_application()
    opened = []
    monkeypatch.setattr(
        update_dialog.QDesktopServices,
        "openUrl",
        lambda url: opened.append(url.toString()),
    )

    for install in (None, Install("appimage", DEB.path)):  # or no file for it
        dialog = UpdateDialog(None, "0.6.2", RELEASE, install)
        assert not dialog.can_update
        assert dialog.start_button.text() == "Open release page"
        assert "cannot update itself" in dialog.message.text()
        dialog.start_button.click()

    assert opened == [RELEASE.url, RELEASE.url]


def fake_run(monkeypatch, behavior) -> None:
    monkeypatch.setattr(update_dialog, "run_update", behavior)


def test_updating_installs_and_hands_back_the_restart_command(monkeypatch) -> None:
    get_application()

    def run(install, release, current, stage, progress):
        progress(5, 10)
        stage("install")
        return ["kubescope"]

    fake_run(monkeypatch, run)
    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)
    accepted = []
    dialog.accepted.connect(lambda: accepted.append(1))

    dialog.start_button.click()
    assert not dialog.start_button.isEnabled() and not dialog.cancel_button.isEnabled()
    wait_until(lambda: accepted, dialog)

    assert dialog.restart_command == ["kubescope"]
    assert dialog.result() == QDialog.DialogCode.Accepted
    dialog.done_with_worker()


def test_a_failed_update_can_be_tried_again(monkeypatch) -> None:
    get_application()
    outcomes = iter([UpdateError("no space"), RuntimeError("boom")])

    def run(*_args):
        raise next(outcomes)

    fake_run(monkeypatch, run)
    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)

    dialog.start_button.click()
    wait_until(lambda: dialog.start_button.text() == "Try again", dialog)
    assert "no space" in dialog.message.text()
    assert dialog.start_button.isEnabled() and dialog.cancel_button.isEnabled()
    assert dialog.restart_command is None

    dialog.start_button.click()  # an unexpected error is reported too
    wait_until(lambda: "boom" in dialog.message.text(), dialog)
    dialog.done_with_worker()


def test_the_dialog_cannot_be_dismissed_while_installing(monkeypatch) -> None:
    get_application()
    closed = []
    monkeypatch.setattr(QDialog, "reject", lambda _dialog: closed.append(1))
    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)
    dialog.reject()  # nothing started yet: closes
    assert closed == [1]

    class Busy:
        def isRunning(self):
            return True

    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)
    dialog.worker = Busy()  # type: ignore[assignment]
    dialog.reject()
    assert closed == [1]  # still open
    dialog.worker = None
    dialog.done_with_worker()


def test_progress_without_a_total_leaves_the_bar_busy() -> None:
    get_application()
    dialog = UpdateDialog(None, "0.6.2", RELEASE, DEB)

    dialog._progress(5, 0)
    assert dialog.bar.value() != 5

    dialog._progress(5, 10)
    assert dialog.bar.value() == 5 and dialog.bar.maximum() == 10


def _run_worker(monkeypatch, behavior) -> dict:
    """Run the body of the worker in this thread, so it is measured on every
    Python, and collect what it reports."""
    monkeypatch.setattr(update_dialog, "run_update", behavior)
    worker = UpdateWorker(DEB, RELEASE, "0.6.2")
    seen: dict = {"stages": [], "progress": []}
    worker.stage.connect(seen["stages"].append)
    worker.progress.connect(lambda done, total: seen["progress"].append((done, total)))
    worker.done.connect(lambda command: seen.update(done=command))
    worker.failed.connect(lambda message: seen.update(failed=message))
    worker.run()
    return seen


def test_the_worker_reports_the_stages_and_the_restart_command(monkeypatch) -> None:
    def run(install, release, current, stage, progress):
        assert (install, release, current) == (DEB, RELEASE, "0.6.2")
        stage("download")
        progress(1, 2)
        return ["kubescope"]

    seen = _run_worker(monkeypatch, run)

    assert seen == {
        "stages": ["download"],
        "progress": [(1, 2)],
        "done": ["kubescope"],
    }


def test_the_worker_reports_an_expected_and_an_unexpected_failure(monkeypatch) -> None:
    def refused(*_args):
        raise UpdateError("no space")

    def broken(*_args):
        raise RuntimeError("boom")

    assert _run_worker(monkeypatch, refused)["failed"] == "no space"
    assert _run_worker(monkeypatch, broken)["failed"] == "boom"
