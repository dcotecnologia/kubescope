import json

from kubescope.assistant import history as store
from kubescope.assistant.history import History


def test_a_conversation_is_kept_for_each_context_between_runs(tmp_path) -> None:
    path = tmp_path / "assistant" / "history.json"
    history = History(path)
    assert history.entries("prod") == []

    history.set("prod", [("user", "why?"), ("assistant", "Because."), ("app", "Done")])
    history.set("dev", [("user", "hi")])

    again = History(path)
    assert again.entries("prod") == [
        ("user", "why?"),
        ("assistant", "Because."),
        ("app", "Done"),
    ]
    assert again.entries("dev") == [("user", "hi")]


def test_tokens_are_redacted_and_empty_or_foreign_entries_are_dropped(tmp_path) -> None:
    history = History(tmp_path / "h.json")

    history.set(
        "prod",
        [
            ("user", "use Bearer abcdefghijklmnop"),
            ("user", "   "),
            ("system", "ignored"),
        ],
    )

    entries = history.entries("prod")
    assert len(entries) == 1 and "abcdefghijklmnop" not in entries[0][1]
    assert "abcdefghijklmnop" not in (tmp_path / "h.json").read_text(encoding="utf-8")


def test_only_the_newest_entries_and_the_start_of_a_long_text_are_kept(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setattr(store, "ENTRY_LIMIT", 2)
    monkeypatch.setattr(store, "TEXT_LIMIT", 5)
    history = History(tmp_path / "h.json")

    history.set("prod", [("user", "one"), ("user", "two"), ("user", "three-long")])

    assert history.entries("prod") == [("user", "two"), ("user", "three")]
    assert History(tmp_path / "h.json").entries("prod") == [
        ("user", "two"),
        ("user", "three"),
    ]


def test_setting_nothing_forgets_the_context_and_clear_forgets_them_all(
    tmp_path,
) -> None:
    history = History(tmp_path / "h.json")
    history.set("prod", [("user", "a")])
    history.set("dev", [("user", "b")])

    history.set("prod", [])
    assert History(tmp_path / "h.json").entries("prod") == []

    history.clear("dev")
    assert history.entries("dev") == []
    history.set("qa", [("user", "c")])
    history.clear()
    assert History(tmp_path / "h.json").entries("qa") == []


def test_a_damaged_or_foreign_file_is_read_as_empty(tmp_path) -> None:
    path = tmp_path / "h.json"
    for text in ("not json", "[1]", '{"contexts": []}'):
        path.write_text(text, encoding="utf-8")
        assert History(path).entries("prod") == []

    path.write_text(
        json.dumps(
            {
                "contexts": {
                    "prod": [
                        {"role": "user", "text": "ok"},
                        {"role": "robot", "text": "no"},
                        {"role": "user", "text": 3},
                        "x",
                    ],
                    "dev": "nope",
                    "qa": [],
                }
            }
        ),
        encoding="utf-8",
    )
    history = History(path)
    assert history.entries("prod") == [("user", "ok")]
    assert history.entries("dev") == [] and history.entries("qa") == []


def test_a_file_that_cannot_be_written_is_only_logged(tmp_path, caplog) -> None:
    blocker = tmp_path / "blocked"
    blocker.write_text("a file, not a folder")
    history = History(blocker / "h.json")

    history.set("prod", [("user", "a")])

    assert "Could not save the assistant history" in caplog.text
    assert history.entries("prod") == [("user", "a")]
