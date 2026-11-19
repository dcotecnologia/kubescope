from tests.qt import cell
from tests.test_window_flows import _ready_window


def test_the_settings_have_a_section_for_the_extensions(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    form = window.settings_ui
    content = form.settingsContent

    assert not form.extensionsCard.isVisibleTo(content)  # only in its own section

    form.extensionsSectionButton.click()

    assert form.extensionsCard.isVisibleTo(content)
    assert form.extensionsSectionButton.isChecked()
    assert not form.generalSectionButton.isChecked()
    assert not form.generalCard.isVisibleTo(content)


def test_the_bundled_gabi_is_listed_in_the_section(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    window.settings_ui.extensionsSectionButton.click()

    table = window.settings_ui.extensionsTable
    assert [cell(table, 0, column).text() for column in range(4)] == [
        "Gabi",
        "1.0.0",
        "Bundled",
        "Installed",
    ]
