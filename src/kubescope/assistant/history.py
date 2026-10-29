"""The conversations with the assistant, kept between runs.

What is kept is what the person said and what the assistant answered,
one conversation for each context, and the notes of the app. The
documents, logs and screens the assistant read to answer are not: they
were only sent, never written here. Every text goes through the
redaction of tokens and keys. No Qt.
"""

import json
import logging
from pathlib import Path

from kubescope.utils.diagnostics import redact

logger = logging.getLogger(__name__)

ROLES = ("user", "assistant", "app")
ENTRY_LIMIT = 200  # entries kept for each context, the newest
TEXT_LIMIT = 20_000  # characters of one entry

Entry = tuple[str, str]  # (role, text)


class History:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._contexts: dict[str, list[Entry]] = {}
        self._load()

    def _load(self) -> None:
        try:
            document = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        contexts = document.get("contexts") if isinstance(document, dict) else None
        for context, entries in (
            contexts if isinstance(contexts, dict) else {}
        ).items():
            kept = [
                (item["role"], item["text"])
                for item in (entries if isinstance(entries, list) else [])
                if isinstance(item, dict)
                and item.get("role") in ROLES
                and isinstance(item.get("text"), str)
            ]
            if kept:
                self._contexts[str(context)] = kept[-ENTRY_LIMIT:]

    def entries(self, context: str) -> list[Entry]:
        """The conversation of a context, oldest first."""
        return list(self._contexts.get(context, []))

    def set(self, context: str, entries: list[Entry]) -> None:
        """Keep the conversation of a context and write the file."""
        cleaned = [
            (role, redact(text)[:TEXT_LIMIT])
            for role, text in entries
            if role in ROLES and text.strip()
        ][-ENTRY_LIMIT:]
        if cleaned:
            self._contexts[context] = cleaned
        else:
            self._contexts.pop(context, None)
        self._save()

    def clear(self, context: str | None = None) -> None:
        """Forget a context, or all of them."""
        if context is None:
            self._contexts.clear()
        else:
            self._contexts.pop(context, None)
        self._save()

    def _save(self) -> None:
        document = {
            "contexts": {
                context: [{"role": role, "text": text} for role, text in entries]
                for context, entries in self._contexts.items()
            }
        }
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(document, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.path)
        except OSError as error:
            logger.warning("Could not save the assistant history: %s", error)
