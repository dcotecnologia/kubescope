import pytest

from kubescope.assistant import session as chat
from kubescope.assistant.runner import Assistant, AssistantError
from kubescope.assistant.session import ChatSession, Message

FAKE = Assistant(
    "fake", "Fake", "fake-ai", lambda model, system: [], lambda line: ("", "")
)


@pytest.fixture
def answers(monkeypatch):
    """Make the program answer with the given pieces, or fail; the arguments of
    each call are kept in `calls`."""
    calls: list[tuple] = []
    plan: dict = {"pieces": [], "error": None}

    def ask(assistant, prompt, model, system):
        calls.append((assistant, prompt, model, system))
        yield from plan["pieces"]
        if plan["error"]:
            raise plan["error"]

    monkeypatch.setattr(chat.runner, "ask", ask)
    return calls, plan


def test_the_session_sends_the_whole_conversation_each_time(answers) -> None:
    calls, plan = answers
    session = ChatSession(FAKE, model="big", system="rules")
    plan["pieces"] = ["It is ", "a Pod."]

    assert list(session.send("what is x?")) == ["It is ", "a Pod."]
    plan["pieces"] = ["Yes."]
    assert list(session.send("really?")) == ["Yes."]

    assert calls[0] == (
        FAKE,
        "User: what is x?\n\nAnswer the last message of the User as the Assistant.",
        "big",
        "rules",
    )
    assert calls[1][1] == (
        "User: what is x?\n\nAssistant: It is a Pod.\n\nUser: really?\n\n"
        "Answer the last message of the User as the Assistant."
    )
    assert session.messages[-2:] == [
        Message("user", "really?"),
        Message("assistant", "Yes."),
    ]


def test_the_oldest_messages_are_left_out_but_the_last_one_never(answers) -> None:
    session = ChatSession(FAKE, limit=10)
    session.messages = [
        Message("user", "a" * 8),
        Message("assistant", "b" * 8),
        Message("user", "c" * 30),
    ]

    prompt = session.prompt()

    assert "a" * 8 not in prompt and "b" * 8 not in prompt
    assert "User: " + "c" * 30 in prompt

    session.messages = [Message("user", "a" * 4), Message("assistant", "b" * 4)]
    assert "User: aaaa" in session.prompt()


def test_a_failure_takes_the_question_back_so_it_can_be_sent_again(answers) -> None:
    _calls, plan = answers
    session = ChatSession(FAKE)
    plan["pieces"] = ["half"]
    plan["error"] = AssistantError("Not logged in")

    with pytest.raises(AssistantError):
        list(session.send("why?"))

    assert session.messages == []


def test_stopping_keeps_what_was_answered_and_nothing_when_nothing_was(
    answers,
) -> None:
    _calls, plan = answers
    session = ChatSession(FAKE)
    plan["pieces"] = ["one", "two"]

    pieces = session.send("why?")
    assert next(pieces) == "one"
    pieces.close()
    assert session.messages[-1] == Message("assistant", "one")

    plan["pieces"] = []
    silent = session.send("and?")
    with pytest.raises(StopIteration):
        next(silent)
    assert session.messages[-1] == Message("assistant", "one")
    assert len(session.messages) == 2
