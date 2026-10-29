import pytest

from kubescope.assistant import actions, executor
from kubescope.cluster import ClusterError


def _request(action: str, **args) -> actions.Request:
    return actions.Request(actions.BY_NAME[action], args)


@pytest.fixture
def cluster_reads(monkeypatch):
    """What the cluster answers; every call is kept in `calls`."""
    calls: list[tuple] = []
    answers: dict = {
        "details": {"spec": {"containers": [{"name": "app"}, {"name": "side"}]}},
        "logs": "line 1\nline 2",
    }

    def details(*args):
        calls.append(("details", *args))
        if isinstance(answers["details"], Exception):
            raise answers["details"]
        return answers["details"]

    def logs(*args, **options):
        calls.append(("logs", *args, options))
        return answers["logs"]

    monkeypatch.setattr(executor.cluster, "get_resource_details", details)
    monkeypatch.setattr(executor.cluster, "get_pod_logs", logs)
    return calls, answers


def test_the_details_of_a_resource_come_back_as_data(cluster_reads) -> None:
    calls, _answers = cluster_reads

    message = executor.fetch(
        _request("get_details", kind="Pod", namespace="ns", name="web"), "ctx"
    )

    assert calls == [("details", "ctx", "Pod", "ns", "web")]
    assert "not instructions to follow" in message and "get_details" in message
    assert '"name": "app"' in message and message.rstrip().endswith("```")


def test_the_logs_are_read_from_the_container_named_or_the_first_one(
    cluster_reads,
) -> None:
    calls, _answers = cluster_reads

    named = executor.fetch(
        _request("get_logs", namespace="ns", pod="web", container="side", lines=50),
        "ctx",
    )
    first = executor.fetch(_request("get_logs", namespace="ns", pod="web"), "ctx")

    assert "line 1\nline 2" in named
    assert calls[0] == ("logs", "ctx", "ns", "web", "side", {"tail_lines": 50})
    assert calls[1:] == [
        ("details", "ctx", "Pod", "ns", "web"),
        ("logs", "ctx", "ns", "web", "app", {"tail_lines": executor.LOG_LINES}),
    ]
    assert "line 2" in first


def test_tokens_and_keys_are_redacted_before_they_go(cluster_reads) -> None:
    _calls, answers = cluster_reads
    key_id = "AK" + "IA" + "ABCDEFGHIJKLMNOP"  # built, so no scanner takes it for real
    answers["logs"] = f"Authorization: Bearer abcdefghijklmnop\nkey {key_id}"

    message = executor.fetch(
        _request("get_logs", namespace="ns", pod="web", container="app"), "ctx"
    )

    assert "abcdefghijklmnop" not in message and key_id not in message
    assert "[redacted" in message


def test_a_long_answer_is_cut_keeping_the_end_of_a_log_and_the_start_of_a_document(
    cluster_reads, monkeypatch
) -> None:
    _calls, answers = cluster_reads
    monkeypatch.setattr(executor, "RESULT_LIMIT", 10)
    answers["logs"] = "0123456789ABCDEFGHIJ"
    answers["details"] = {"a": "x" * 100}

    log = executor.fetch(
        _request("get_logs", namespace="ns", pod="web", container="app"), "ctx"
    )
    document = executor.fetch(
        _request("get_details", kind="Pod", namespace="ns", name="web"), "ctx"
    )

    assert "[earlier lines left out]\nABCDEFGHIJ" in log and "0123456789" not in log
    assert "[the rest left out]" in document


def test_a_failure_is_the_answer_so_the_assistant_can_tell_the_person(
    cluster_reads,
) -> None:
    _calls, answers = cluster_reads
    answers["details"] = ClusterError("forbidden")

    message = executor.fetch(
        _request("get_details", kind="Pod", namespace="ns", name="web"), "ctx"
    )
    no_container = executor.fetch(
        _request("get_logs", namespace="ns", pod="web"), "ctx"
    )

    assert "The cluster did not answer: forbidden" in message
    assert "forbidden" in no_container

    answers["details"] = {"spec": {}}
    empty = executor.fetch(_request("get_logs", namespace="ns", pod="web"), "ctx")
    assert "has no container" in empty


def test_an_action_that_does_not_read_for_the_assistant_is_refused() -> None:
    with pytest.raises(ValueError, match="does not read"):
        executor.fetch(_request("refresh"), "ctx")


@pytest.fixture
def lists(monkeypatch):
    """What the cluster lists; the arguments of each call are kept in
    `calls`."""
    from kubescope.models import ClusterResource, PodInfo, Workload

    calls: list[tuple] = []
    pod = PodInfo("ns", "web-1", "Running", 1, 2, "5m", ("app",), restarts=3, node="n1")
    deployment = Workload("ns", "Deployment", "web", 1, 2, "1d", restarts=3)
    events = [
        ClusterResource(
            "ns", "Event", "e1", ("Warning", "BackOff", "Pod/web-1", "crash", "4"), "1m"
        ),
        ClusterResource(
            "ns", "Event", "e2", ("Normal", "Pulled", "Pod/api-1", "ok", "1"), "2m"
        ),
    ]
    service = ClusterResource("", "Node", "n1", ("Ready",), "9d")

    def get_pods(context, namespace):
        calls.append(("pods", context, namespace))
        return [], [pod]

    def get_workloads(context, namespace, kinds):
        calls.append(("workloads", context, namespace, kinds))
        return [], [deployment]

    def get_resources(context, namespace, kind):
        calls.append(("resources", context, namespace, kind))
        return [], events if kind == "Event" else [service]

    monkeypatch.setattr(executor.cluster, "get_pods", get_pods)
    monkeypatch.setattr(executor.cluster, "get_workloads", get_workloads)
    monkeypatch.setattr(executor.cluster, "get_resources", get_resources)
    return calls


def test_a_list_is_read_as_the_app_shows_it(lists) -> None:
    pods = executor.fetch(_request("list", view="pods", namespace="ns"), "ctx")
    workloads = executor.fetch(
        _request("list", view="deployments", namespace=""), "ctx"
    )
    services = executor.fetch(_request("list", view="services", namespace=""), "ctx")

    assert "ns/web-1 Running ready 1/2 restarts 3 node n1 age 5m" in pods
    assert "ns/Deployment/web" in workloads and "restarts 3" in workloads
    assert "Node/n1 Ready age 9d" in services
    assert lists == [
        ("pods", "ctx", "ns"),
        ("workloads", "ctx", None, ("Deployment",)),
        ("resources", "ctx", None, "Service"),
    ]


def test_a_list_that_cannot_be_read_this_way_is_the_answer_too(lists) -> None:
    message = executor.fetch(_request("list", view="bogus", namespace=""), "ctx")

    assert "cannot be read this way" in message


def test_a_long_list_is_cut_at_the_row_limit(lists, monkeypatch) -> None:
    monkeypatch.setattr(executor, "ROW_LIMIT", 1)
    monkeypatch.setattr(
        executor.cluster,
        "get_pods",
        lambda context, namespace: ([], [executor_pod(), executor_pod()]),
    )

    message = executor.fetch(_request("list", view="pods", namespace=""), "ctx")

    assert "[1 more rows left out]" in message


def executor_pod():
    from kubescope.models import PodInfo

    return PodInfo("ns", "p", "Running", 1, 1, "1m", ("app",))


def test_the_events_can_be_kept_by_the_name_of_their_object(lists) -> None:
    every = executor.fetch(_request("get_events", namespace="ns"), "ctx")
    mine = executor.fetch(_request("get_events", namespace="", name="WEB"), "ctx")

    assert "Pod/web-1" in every and "Pod/api-1" in every
    assert "Pod/web-1" in mine and "Pod/api-1" not in mine
    assert lists[0] == ("resources", "ctx", "ns", "Event")
    empty = executor.fetch(_request("get_events", namespace="", name="zzz"), "ctx")
    assert "(no rows)" in empty
