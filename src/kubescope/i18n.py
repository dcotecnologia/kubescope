"""Language handling: source strings are English, Portuguese ships as a .qm file."""

from pathlib import Path

from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QTranslator

LANGUAGES = {"en": "English", "pt": "Português"}
TRANSLATIONS_DIR = Path(__file__).resolve().parent / "translations"

_installed: list[QTranslator] = []


def resolve_language(choice: str) -> str:
    """Map a stored choice ("auto", "en", "pt") to a supported language code."""
    if choice in LANGUAGES:
        return choice
    system = QLocale.system().name().split("_")[0].lower()
    return system if system in LANGUAGES else "en"


def apply_language(choice: str) -> str:
    """Install the translators for the choice and return the language in use."""
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
    return code
