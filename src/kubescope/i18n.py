"""Language handling: source strings are English, the other languages ship as
.qm files made from the .ts files in translations/."""

from pathlib import Path

from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, Qt, QTranslator

from kubescope.settings import LANGUAGES

TRANSLATIONS_DIR = Path(__file__).resolve().parent / "translations"

_installed: list[QTranslator] = []
RIGHT_TO_LEFT = frozenset({"ar"})  # written from right to left: the layout mirrors


def resolve_language(choice: str) -> str:
    """Map a stored choice ("auto", "en", "pt") to a supported language
    code."""
    if choice in LANGUAGES:
        return choice
    system = QLocale.system().name().split("_")[0].lower()
    return system if system in LANGUAGES else "en"


def apply_language(choice: str) -> str:
    """Install the translators for the choice and return the language in
    use."""
    application = QCoreApplication.instance()
    code = resolve_language(choice)
    for translator in _installed:
        application.removeTranslator(translator)
    _installed.clear()
    if code != "en":
        sources = (
            (f"kubescope_{code}", str(TRANSLATIONS_DIR)),
            (
                f"qtbase_{code}",
                QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
            ),
        )
        for name, directory in sources:
            translator = QTranslator(application)
            if translator.load(name, directory):
                application.installTranslator(translator)
                _installed.append(translator)
    application.setLayoutDirection(
        Qt.LayoutDirection.RightToLeft
        if code in RIGHT_TO_LEFT
        else Qt.LayoutDirection.LeftToRight
    )
    return code
