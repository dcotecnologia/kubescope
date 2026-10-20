"""Language handling: source strings are English, the other languages are JSON
files: the ones that ship with the app (`src/kubescope/languages/`), and any in
the `languages` folder of the settings, which add a language or replace a
shipped one by its code.

Qt's own texts (standard dialogs) still come from its translation files.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QCoreApplication, QLibraryInfo, QLocale, Qt, QTranslator
from PySide6.QtGui import QGuiApplication

from kubescope.settings import config_directory

logger = logging.getLogger(__name__)

BUNDLED_DIRECTORY = Path(__file__).resolve().parent / "languages"
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


# System locales that use a language file of another territory.
_LOCALE_ALIASES = {"zh_HK": "zh_TW", "zh_MO": "zh_TW"}


def _english_name(code: str) -> str:
    """The English name of a language, with the territory for a code such as
    zh_TW; empty when Qt does not know it."""
    locale = QLocale(code)
    name = QLocale.languageToString(locale.language())
    if name == "C":
        return ""
    if "_" in code:
        name += f" ({QLocale.territoryToString(locale.territory())})"
    return name


def language_choices() -> list[tuple[str, str]]:
    """The languages for a list: English first, then the others by their
    English name, each shown as its own name followed by the English one, so a
    language can be found without reading its script."""
    named = []
    for code, name in available_languages().items():
        if code == ENGLISH:
            continue
        english = _english_name(code)
        known = english not in ("", name)
        named.append(
            (english if known else name, code, f"{name} · {english}" if known else name)
        )
    named.sort(key=lambda item: item[0].casefold())
    return [(ENGLISH, "English"), *((code, label) for _, code, label in named)]


def resolve_language(choice: str) -> str:
    """Map a stored choice ("auto", "en", "pt") to a supported language
    code."""
    available = available_languages()
    if choice in available:
        return choice
    system = QLocale.system().name()  # such as pt_BR
    for candidate in (
        system,
        _LOCALE_ALIASES.get(system, ""),
        system.split("_")[0].lower(),
    ):
        if candidate in available:
            return candidate
    return ENGLISH


def apply_language(choice: str) -> str:
    """Install the translators for the choice and return the language in
    use."""
    application = QCoreApplication.instance()
    assert application is not None
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
    QGuiApplication.setLayoutDirection(
        Qt.LayoutDirection.RightToLeft
        if code != ENGLISH and languages()[code].right_to_left
        else Qt.LayoutDirection.LeftToRight
    )
    return code
