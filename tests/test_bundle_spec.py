import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_the_bundle_keeps_every_qt_module_the_app_imports() -> None:
    spec = (ROOT / "KubeScope.spec").read_text(encoding="utf-8")
    excluded = set(
        re.findall(r'"(PySide6\.Qt\w+)"', spec.split("excludes=[")[1].split("]")[0])
    )
    imported = {
        module
        for source in (ROOT / "src").rglob("*.py")
        for module in re.findall(
            r"^\s*from (PySide6\.Qt\w+) import",
            source.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    }

    assert "PySide6.QtNetwork" in imported  # the single instance needs it
    assert imported & excluded == set()  # a module left out is a crash on start
