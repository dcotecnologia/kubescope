"""Turn the Qt translation files (.ts) into the JSON languages the app loads.

Every `translations/kubescope_<code>.ts` becomes
`languages/<code>.json`, with the finished translations only. The name
of the language and its direction are kept from the JSON that is already
there; `--new CODE NAME [--rtl]` starts one.
"""

import argparse
import json
import sys
from pathlib import Path
from xml.etree import ElementTree

SOURCE = Path(__file__).resolve().parent.parent / "src" / "kubescope"
TRANSLATIONS = SOURCE / "translations"
LANGUAGES = SOURCE / "languages"


def read_strings(path: Path) -> dict[str, dict[str, str]]:
    strings: dict[str, dict[str, str]] = {}
    for context in ElementTree.parse(path).iter("context"):
        texts = {}
        for message in context.iter("message"):
            translation = message.find("translation")
            text = (translation.text or "") if translation is not None else ""
            if translation is not None and translation.get("type") in (
                "unfinished",
                "vanished",
                "obsolete",
            ):
                continue
            if text:
                texts[message.findtext("source") or ""] = text
        if texts:
            strings[context.findtext("name") or ""] = texts
    return strings


def write(code: str, name: str, rtl: bool, strings: dict) -> None:
    document = {"name": name, "rtl": rtl, "strings": strings}
    LANGUAGES.mkdir(exist_ok=True)
    (LANGUAGES / f"{code}.json").write_text(
        json.dumps(document, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def convert() -> int:
    for path in sorted(TRANSLATIONS.glob("kubescope_*.ts")):
        code = path.stem.removeprefix("kubescope_")
        target = LANGUAGES / f"{code}.json"
        if not target.is_file():
            print(f"{target.name} is missing: start it with --new {code} NAME")
            return 1
        known = json.loads(target.read_text(encoding="utf-8"))
        write(code, known["name"], known.get("rtl") is True, read_strings(path))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new", nargs=2, metavar=("CODE", "NAME"))
    parser.add_argument("--rtl", action="store_true")
    arguments = parser.parse_args()
    if arguments.new:
        write(arguments.new[0], arguments.new[1], arguments.rtl, {})
    return convert()


if __name__ == "__main__":
    sys.exit(main())
