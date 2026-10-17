import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QApplication

from kubescope.utils import fonts

application = QApplication.instance() or QApplication([])


def test_the_shipped_fonts_load_and_name_their_families() -> None:
    families = fonts.load_fonts()

    assert fonts.UI_FAMILY in families and fonts.CODE_FAMILY in families
    assert len(families) == len(set(families))  # Regular and Bold are one family
    assert {path.suffix for path in fonts.FONTS_DIRECTORY.glob("*.ttf")} == {".ttf"}
    assert (fonts.FONTS_DIRECTORY / "LICENSE.txt").is_file()  # the OFL travels along


def test_the_interface_uses_noto_sans_and_code_uses_noto_sans_mono() -> None:
    original = application.font()
    try:
        fonts.apply_fonts(application)

        assert application.font().family() == "Noto Sans"
        assert application.font().pointSize() == fonts.UI_POINT_SIZE
        code = fonts.code_font()
        assert code.family() == "Noto Sans Mono"
        metrics = QFontMetrics(code)  # every character is as wide as another
        assert metrics.horizontalAdvance("i") == metrics.horizontalAdvance("W")
        assert code.styleHint() == QFont.StyleHint.Monospace
    finally:
        application.setFont(original)


def test_a_font_that_cannot_load_is_skipped_with_a_warning(monkeypatch, caplog) -> None:
    monkeypatch.setattr(
        fonts.QFontDatabase, "addApplicationFont", staticmethod(lambda _path: -1)
    )

    with caplog.at_level("WARNING"):
        assert fonts.load_fonts() == []

    assert "Could not load the font" in caplog.text
