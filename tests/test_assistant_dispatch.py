import pytest

from kubescope import writes
from kubescope.assistant import actions, dispatch


def _request(action: str, **args) -> actions.Request:
    return actions.Request(actions.BY_NAME[action], args)


@pytest.mark.parametrize(
    ("request_", "function", "arguments"),
    [
        (
            _request("scale", namespace="ns", name="web", replicas=2),
            writes.scale_deployment,
            ("ctx", "ns", "web", 2),
        ),
        (
            _request("restart", namespace="ns", name="web"),
            writes.restart_deployment,
            ("ctx", "ns", "web"),
        ),
        (
            _request("evict_pod", namespace="ns", name="p"),
            writes.evict_pod,
            ("ctx", "ns", "p"),
        ),
        (
            _request("delete", kind="Pod", namespace="ns", name="p"),
            writes.delete_pod,
            ("ctx", "ns", "p"),
        ),
        (
            _request("delete", kind="Service", namespace="ns", name="s"),
            writes.delete_resource,
            ("ctx", "Service", "ns", "s"),
        ),
        (
            _request(
                "replace", kind="Pod", namespace="ns", name="p", document={"a": 1}
            ),
            writes.replace_resource,
            ("ctx", "Pod", "ns", "p", {"a": 1}),
        ),
    ],
)
def test_each_change_runs_the_function_of_the_write_mode(
    request_, function, arguments
) -> None:
    assert dispatch.write_call(request_, "ctx") == (function, arguments)


def test_what_does_not_change_the_cluster_is_refused() -> None:
    with pytest.raises(ValueError, match="does not change"):
        dispatch.write_call(_request("refresh"), "ctx")
