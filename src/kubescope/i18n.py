"""Language handling: source strings are English, the other languages are JSON
files in the `languages` folder of the settings.

The ones that ship with the app are copied there, like the community
themes, and refreshed while the person has not edited them; any other
file placed there adds a language. Qt's own texts (standard dialogs)
still come from its translation files.
"""

import hashlib
import json
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, Qt, QTranslator

from kubescope.settings import config_directory

logger = logging.getLogger(__name__)

BUNDLED_DIRECTORY = Path(__file__).resolve().parent / "languages"
INSTALLED_FILE = "installed-languages.json"
ENGLISH = "en"

_installed: list[QTranslator] = []
_languages: dict[str, "Language"] | None = None


@dataclass(frozen=True)
class Language:
    name: str  # in the language itself
    right_to_left: bool
    strings: dict[str, dict[str, str]]  # context -> English text -> translation


class JsonTranslator(QTranslator):
    """Answers the texts of one language from a dictionary."""

    def __init__(self, language: Language, parent: Any = None) -> None:
        super().__init__(parent)
        self._strings = language.strings

    def translate(
        self,
        context: str,
        source_text: str,
        disambiguation: str | None = None,
        n: int = -1,
    ) -> str | None:
        """None when the text is not translated, so Qt shows the English."""
        return self._strings.get(context, {}).get(source_text)

    def isEmpty(self) -> bool:
        return not self._strings


def languages_directory() -> Path:
    return config_directory() / "languages"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _installed_digests() -> dict[str, str]:
    """What the app last wrote for each language, to tell an untouched copy
    from one the person edited."""
    try:
        document = json.loads(
            (config_directory() / INSTALLED_FILE).read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return {}
    return (
        {k: v for k, v in document.items() if isinstance(v, str)}
        if isinstance(document, dict)
        else {}
    )


def install_bundled_languages(source: Path = BUNDLED_DIRECTORY) -> list[str]:
    """Copy the languages that came with the app into the languages folder.

    A language is installed once and kept up to date while its copy is
    the one the app wrote; one the person edited is never overwritten,
    and one they deleted does not come back. Returns the codes written
    now.
    """
    global _languages
    recorded = _installed_digests()
    written: list[str] = []
    for path in sorted(source.glob("*.json")) if source.is_dir() else []:
        target = languages_directory() / path.name
        try:
            fresh = _digest(path)
            if target.exists():
                if recorded.get(path.stem) != _digest(target) or fresh == _digest(
                    target
                ):
                    continue  # edited by the person, or already current
            elif path.stem in recorded:
                continue  # deleted by the person
            languages_directory().mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        except OSError as error:
            logger.warning("Could not install the language %s: %s", path.stem, error)
            continue
        recorded[path.stem] = fresh
        written.append(path.stem)
    if written:
        logger.info("Installed languages: %s", ", ".join(written))
        _languages = None
        try:
            (config_directory() / INSTALLED_FILE).write_text(
                json.dumps(recorded, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        except OSError as error:
            logger.warning("Could not record the installed languages: %s", error)
    return written


def parse_language(document: object) -> Language:
    """A language from its JSON document; ValueError when it is not one."""
    if not isinstance(document, dict):
        raise ValueError("it is not an object")
    name, strings = document.get("name"), document.get("strings")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("it has no name")
    if not isinstance(strings, dict):
        raise ValueError("it has no strings")
    return Language(
        name=name.strip(),
        right_to_left=document.get("rtl") is True,
        strings={
            context: {
                text: translation
                for text, translation in texts.items()
                if isinstance(translation, str) and translation
            }
            for context, texts in strings.items()
            if isinstance(texts, dict)
        },
    )


def _read_languages(directory: Path, into: dict[str, Language]) -> None:
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        if path.stem == ENGLISH:
            continue
        try:
            into[path.stem] = parse_language(
                json.loads(path.read_text(encoding="utf-8"))
            )
        except (OSError, ValueError) as error:
            logger.warning("Skipping language %s: %s", path.name, error)


def languages() -> dict[str, Language]:
    """The languages besides English: the ones that ship with the app, and the
    files of the languages folder on top of them, which win by code."""
    global _languages
    if _languages is None:
        found: dict[str, Language] = {}
        _read_languages(BUNDLED_DIRECTORY, found)
        _read_languages(languages_directory(), found)
        _languages = found
    return _languages


def reload_languages() -> None:
    """Read the languages folder again, after a file was added or edited."""
    global _languages
    _languages = None


def available_languages() -> dict[str, str]:
    """Every language by code, each named in itself, English first."""
    return {
        ENGLISH: "English",
        **{code: language.name for code, language in languages().items()},
    }


def resolve_language(choice: str) -> str:
    """Map a stored choice ("auto", "en", "pt") to a supported language
    code."""
    available = available_languages()
    if choice in available:
        return choice
    system = QLocale.system().name().split("_")[0].lower()
    return system if system in available else ENGLISH


def apply_language(choice: str) -> str:
    """Install the translators for the choice and return the language in
    use."""
    application = QCoreApplication.instance()
    code = resolve_language(choice)
    for translator in _installed:
        application.removeTranslator(translator)
    _installed.clear()
    if code != ENGLISH:
        translator = JsonTranslator(languages()[code], application)
        application.installTranslator(translator)
        _installed.append(translator)
        qt_translator = QTranslator(application)
        if qt_translator.load(
            f"qtbase_{code}",
            QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
        ):
            application.installTranslator(qt_translator)
            _installed.append(qt_translator)
    application.setLayoutDirection(
        Qt.LayoutDirection.RightToLeft
        if code != ENGLISH and languages()[code].right_to_left
        else Qt.LayoutDirection.LeftToRight
    )
    return code
