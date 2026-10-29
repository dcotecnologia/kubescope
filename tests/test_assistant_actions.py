import json

import pytest

from kubescope.assistant import actions
from kubescope.assistant.actions import Invalid, Request


def _block(document) -> str:
    body = document if isinstance(document, str) else json.dumps(document)
    return f"```kubescope-action\n{body}\n```\n"


def _only(text: str):
    (found,) = actions.parse(text)
    return found


def test_a_valid_block_becomes_a_request_of_the_catalog() -> None:
    found = _only(
        "Scaling.\n"
        + _block({"action": "scale", "namespace": "ns", "name": "web", "replicas": 3})
    )

    assert isinstance(found, Request)
    assert found.action is actions.BY_NAME["scale"] and found.action.kind == "write"
    assert found.args == {"namespace": "ns", "name": "web", "replicas": 3}


def test_the_blocks_of_an_answer_come_in_order_and_the_rest_is_ignored() -> None:
    text = (
        "one\n"
        + _block({"action": "refresh"})
        + "two\n```json\n{}\n```\n"
        + _block({"action": "open_view", "view": "pods"})
    )

    found = actions.parse(text)

    assert [
        request.action.name for request in found if isinstance(request, Request)
    ] == [
        "refresh",
        "open_view",
    ]
    assert actions.parse("nothing to do") == []


def test_optional_fields_may_be_left_out_and_empty_ones_given() -> None:
    assert isinstance(_only(_block({"action": "search", "text": ""})), Request)
    assert isinstance(
        _only(_block({"action": "search", "text": "x", "regex": True, "case": False})),
        Request,
    )
    details = {"action": "show_details", "kind": "Pod", "namespace": "", "name": "n"}
    assert isinstance(_only(_block(details)), Request)


@pytest.mark.parametrize(
    ("document", "reason"),
    [
        ("not json", "not JSON"),
        ("[1]", "not an object"),
        ({"action": "rm_rf"}, "no action rm_rf"),
        ({}, "no action None"),
        ({"action": "refresh", "force": True}, "no force"),
        ({"action": "scale", "namespace": "ns", "name": "web"}, "needs replicas"),
        (
            {"action": "scale", "namespace": "ns", "name": "web", "replicas": "3"},
            "replicas must be a whole number",
        ),
        (
            {"action": "scale", "namespace": "ns", "name": "web", "replicas": True},
            "replicas must be a whole number",
        ),
        (
            {"action": "scale", "namespace": "ns", "name": "web", "replicas": -1},
            "replicas must be between",
        ),
        (
            {"action": "scale", "namespace": "ns", "name": " ", "replicas": 1},
            "name is empty",
        ),
        (
            {"action": "scale", "namespace": 3, "name": "web", "replicas": 1},
            "namespace must be a str",
        ),
        ({"action": "open_view", "view": "pizza"}, "not one of the known ones"),
        (
            {"action": "delete", "kind": "Node", "namespace": "", "name": "n"},
            "not one of the known ones",
        ),
        (
            {
                "action": "replace",
                "kind": "Pod",
                "namespace": "ns",
                "name": "p",
                "document": [],
            },
            "document must be a dict",
        ),
        ({"action": "search", "text": "x", "regex": 1}, "regex must be a bool"),
    ],
)
def test_a_block_that_does_not_fit_the_catalog_is_dropped(document, reason) -> None:
    found = _only(_block(document))

    assert isinstance(found, Invalid) and reason in found.reason


def test_the_blocks_are_taken_out_of_the_answer_to_read() -> None:
    text = "Let me scale it.\n" + _block({"action": "refresh"}) + "Done soon."

    assert actions.strip(text) == "Let me scale it.\nDone soon."


def test_the_assistant_is_told_every_action_and_its_fields() -> None:
    told = actions.instructions()

    assert actions.FENCE in told
    for action in actions.ACTIONS:
        assert f"- {action.name} [{action.kind}]" in told
    assert "replicas: int" in told and "regex?: bool" in told
    assert "Deployment" in told  # the kinds are listed


def test_only_the_actions_that_change_the_cluster_are_writes() -> None:
    writes = {action.name for action in actions.ACTIONS if action.kind == "write"}

    assert writes == {"scale", "restart", "evict_pod", "delete", "replace"}


def test_a_request_is_described_in_one_line_for_the_person_to_confirm() -> None:
    scale = _only(
        _block({"action": "scale", "namespace": "ns", "name": "web", "replicas": 3})
    )
    replace = _only(
        _block(
            {
                "action": "replace",
                "kind": "Pod",
                "namespace": "ns",
                "name": "p",
                "document": {"a": 1},
            }
        )
    )

    assert isinstance(scale, Request) and isinstance(replace, Request)
    assert actions.describe(scale) == "scale(namespace=ns, name=web, replicas=3)"
    assert 'document={"a": 1}' in actions.describe(replace)
    refresh = _only(_block({"action": "refresh"}))
    assert isinstance(refresh, Request) and actions.describe(refresh) == "refresh()"
