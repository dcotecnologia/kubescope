from kubescope.extensions import testing
from kubescope.extensions.components import UiComponents


def test_the_helpers_find_widgets_by_kind_and_read_their_texts() -> None:
    testing.application()
    components = UiComponents()
    host = components.widget()
    column = components.column(
        components.label("one"),
        components.button("Go"),
        components.command_box("ls"),
        components.filter_select([("A", 1)]),
    )
    host.setLayout(column)
    assert testing.texts(host) == ["one"]
    assert testing.texts(host, "text") == ["ls"]
    assert set(testing.buttons(host)) == {"Go"}
    assert testing.find(host, "combo").count() == 1
    assert len(testing.find_all(host, "button")) == 1
    clicked: list[int] = []
    testing.buttons(host)["Go"].clicked.connect(lambda: clicked.append(1))
    testing.click(testing.buttons(host)["Go"], kind="press")
    testing.click(testing.buttons(host)["Go"], kind="release")
    testing.click(host, kind="move")
    testing.click(host, kind="release", button="right")
    testing.settle()
    item = components.table_item("x")
    components.set_badge_colors(item, "#111", "#222")
    assert testing.badge_of(item) == ("#111", "#222")


def test_the_modals_refuse_to_block_or_are_answered(monkeypatch) -> None:
    import pytest
    from PySide6.QtWidgets import QDialog, QMessageBox

    testing.refuse_modals(monkeypatch)
    for kind in (QDialog(), QMessageBox()):
        with pytest.raises(AssertionError):
            kind.exec()
    seen: list[object] = []
    testing.answer_dialogs(monkeypatch, lambda dialog: seen.append(dialog))
    assert QDialog().exec() == 0 and len(seen) == 1


def test_the_cleanup_deletes_what_a_test_showed() -> None:
    from PySide6.QtWidgets import QWidget

    steps = testing.cleanup()
    next(steps)
    window = QWidget()
    window.show()
    list(steps)
    from shiboken6 import isValid

    assert not isValid(window)


def test_the_panels_are_made_still(monkeypatch) -> None:
    from kubescope.extensions import chat_dock, side_panel

    testing.still_panels(monkeypatch)
    assert chat_dock.ANIMATION_MS == 0 and side_panel.SLIDE_MS == 0


def test_a_picture_is_made_without_an_image_class(tmp_path) -> None:
    data = testing.png_bytes(4, 3)
    assert data.startswith(b"\x89PNG")
    path = tmp_path / "a.png"
    testing.write_png(path, color=(0, 0, 255))
    assert path.read_bytes().startswith(b"\x89PNG")
    from PySide6.QtGui import QPixmap

    pixmap = QPixmap()
    assert pixmap.loadFromData(data) and pixmap.width() == 4
