"""Every shortcut of the app is in the list of the Settings: the ones that can
be changed in `shortcuts.DEFAULTS` and the ones that cannot in
`shortcuts.FIXED`.

Adding a key anywhere else breaks these tests on purpose:
put it in the list first (see the rule in AGENTS.md).
"""

import os
import re
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from kubescope import window as window_module
from kubescope.utils import shortcuts
from tests.test_window_flows import _ready_window

SOURCE = Path(__file__).resolve().parent.parent / "src" / "kubescope"
KEY_CODE = re.compile(r"QShortcut\(|\.setShortcut\(|\.setShortcuts\(|def keyPressEvent")

# Where the code reads a key, and which entry of `shortcuts` lists it.
LISTED = {
    "window.py": "every action of DEFAULTS, and the ones of the extensions",
    "views/detail_tab.py": "FIXED find_in_text",
    "views/log_tab.py": "FIXED find_in_text",
    "views/search_bar.py": "FIXED close",
    "extensions/side_panel.py": "FIXED close",
    "extensions/chat_view.py": "FIXED send_message",
}


def test_every_file_that_reads_a_key_is_listed() -> None:
    found = {
        str(path.relative_to(SOURCE))
        for path in SOURCE.rglob("*.py")
        if not path.name.startswith("ui_") and KEY_CODE.search(path.read_text())
    }
    assert found == set(LISTED), (
        "a shortcut was added or removed: list it in kubescope.utils.shortcuts "
        "(DEFAULTS if it can change, FIXED if not), give it a label in the "
        "Settings, and update LISTED"
    )


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def test_every_shortcut_has_a_label_and_a_row_in_the_settings(window) -> None:
    labels = window._shortcut_labels()
    assert set(shortcuts.DEFAULTS) <= set(labels)
    assert set(window._shortcuts) >= set(shortcuts.DEFAULTS)

    window._fill_shortcuts(window._shortcut_values())
    table = window.settings_ui.shortcutsTable
    listed = {
        table.item(row, 0).data(window_module.Qt.ItemDataRole.UserRole)
        for row in range(table.rowCount())
    }
    assert set(shortcuts.DEFAULTS) <= listed
    assert {f"fixed:{action}" for action in shortcuts.FIXED} <= listed

    for row in range(table.rowCount()):  # the fixed ones are shown, not edited
        action = table.item(row, 0).data(window_module.Qt.ItemDataRole.UserRole)
        if action.startswith("fixed:"):
            assert table.item(row, 1).text() == shortcuts.FIXED[action[6:]]
            assert table.cellWidget(row, 1) is None


def test_a_key_of_a_list_does_not_clash_with_another_shortcut() -> None:
    assert shortcuts.duplicate(shortcuts.DEFAULTS) is None


def test_the_names_of_the_shortcuts_are_shown_whole(window) -> None:
    window.show()
    window._show_page(2)
    window._show_settings_section(3)
    window._fill_shortcuts(window._shortcut_values())
    table = window.settings_ui.shortcutsTable
    widest = max(
        table.fontMetrics().horizontalAdvance(table.item(row, 0).text())
        for row in range(table.rowCount())
    )
    assert table.horizontalHeader().sectionSize(0) >= widest
