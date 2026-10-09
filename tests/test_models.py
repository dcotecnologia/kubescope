import pytest

from kubescope.models import (
    POD_SORT_COLUMNS,
    SORT_COLUMNS,
    PodInfo,
    Workload,
    format_age,
    format_bytes,
    format_cpu,
    format_memory,
    parse_cpu,
    parse_memory,
    pod_sort_key,
    workload_sort_key,
)


@pytest.mark.parametrize(
    ("ready", "desired", "expected"),
    [
        (3, 3, "Healthy"),
        (1, 3, "Degraded"),
        (0, 2, "Unavailable"),
        (0, 0, "Scaled to zero"),
    ],
)
def test_workload_status(ready: int, desired: int, expected: str) -> None:
    workload = Workload("default", "Deployment", "api", ready, desired, "1h")

    assert workload.status == expected


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [(0, "<1m"), (59, "<1m"), (60, "1m"), (3600, "1h"), (86400, "1d")],
)
def test_format_age(seconds: int, expected: str) -> None:
    assert format_age(seconds) == expected


def test_parse_quantities() -> None:
    from kubescope.models import format_bytes, format_cores, parse_cpu, parse_memory

    assert parse_cpu("250m") == 0.25
    assert parse_cpu("2") == 2.0
    assert parse_cpu("1500000n") == 0.0015
    assert parse_cpu(None) == 0.0
    assert parse_memory("512Mi") == 512 * 2**20
    assert parse_memory("2Gi") == 2 * 2**30
    assert parse_memory("1G") == 1e9
    assert parse_memory("129e6") == 129e6
    assert format_cores(3.46) == "3.5"
    assert format_bytes(3 * 2**30) == "3.0 GiB"
    assert format_bytes(512 * 2**20) == "512 MiB"


def test_age_seconds_inverts_format_age() -> None:
    from kubescope.models import age_seconds

    assert age_seconds("<1m") == 0
    assert age_seconds("5m") == 300
    assert age_seconds("3h") == 3 * 3600
    assert age_seconds("12d") == 12 * 86400
    assert age_seconds("unknown") == float("inf")
    assert age_seconds("2d") > age_seconds("47h")


def test_workload_sort_keys_rank_status_worst_first_and_ready_by_fraction() -> None:
    from kubescope.models import workload_sort_key

    healthy = Workload("b", "Deployment", "api", 3, 3, "1d")
    degraded = Workload("a", "Deployment", "web", 1, 4, "2d")
    down = Workload("c", "StatefulSet", "db", 0, 1, "9d")
    off = Workload("a", "Deployment", "job", 0, 0, "3h")
    items = [healthy, degraded, down, off]

    def order(column: int) -> list[str]:
        ranked = sorted(items, key=lambda w: workload_sort_key(w, column))
        return [workload.name for workload in ranked]

    assert order(0) == ["job", "web", "api", "db"]  # namespace, then kind/name
    assert order(1) == ["job", "web", "api", "db"]  # Deployment < StatefulSet
    assert order(2) == ["api", "db", "job", "web"]
    assert order(3) == ["db", "web", "job", "api"]  # 0/1, 1/4, 0/0, 3/3
    assert order(4) == ["db", "web", "job", "api"]  # Unavailable first
    assert order(8) == ["job", "api", "web", "db"]  # youngest first


def test_pod_highlight_flags_problems_over_young_pods() -> None:
    from kubescope.models import PodInfo, pod_highlight

    def pod(phase="Running", ready=1, restarts=0, age="2d") -> PodInfo:
        return PodInfo("d", "p", phase, ready, 1, age, ("a",), restarts=restarts)

    assert pod_highlight(pod()) is None
    assert pod_highlight(pod(age="<1m")) == "young"
    assert pod_highlight(pod(age="59m")) == "young"
    assert pod_highlight(pod(age="1h")) is None
    assert pod_highlight(pod(restarts=2)) == "problem"
    assert pod_highlight(pod(phase="Failed", ready=0)) == "problem"
    assert pod_highlight(pod(ready=0)) == "problem"
    assert pod_highlight(pod(age="5m", restarts=1)) == "problem"  # problem wins
    assert pod_highlight(pod(phase="Pending", ready=0, age="5m")) == "young"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, 0.0), ("", 0.0), ("250m", 0.25), ("2", 2.0), ("1500u", 0.0015)],
)
def test_parse_cpu(value: str | None, expected: float) -> None:
    assert parse_cpu(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, 0.0),
        ("512Mi", 512 * 2**20),
        ("2G", 2e9),
        ("1500m", 1.5),
        ("1024", 1024.0),
    ],
)
def test_parse_memory(value: str | None, expected: float) -> None:
    assert parse_memory(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("cores", "expected"), [(None, "—"), (0.25, "250m"), (2.0, "2.00")]
)
def test_format_cpu(cores: float | None, expected: str) -> None:
    assert format_cpu(cores) == expected


@pytest.mark.parametrize(
    ("size", "expected"),
    [(None, "—"), (512 * 2**20, "512 MiB"), (3 * 2**30, "3.0 GiB")],
)
def test_format_memory_and_bytes(size: float | None, expected: str) -> None:
    assert format_memory(size) == expected
    if size is not None:
        assert format_bytes(size) == expected


def test_workload_sort_key_covers_every_column() -> None:
    workload = Workload("ns", "Deployment", "Api", 1, 2, "3h", 4, 0.5, 100.0)
    bare = Workload("ns", "Deployment", "api", 0, 0, "1d")

    keys = [workload_sort_key(workload, column) for column in range(len(SORT_COLUMNS))]

    assert keys[3][:2] == (0.5, 2)
    assert workload_sort_key(bare, 3)[:2] == (1.0, 0)
    assert workload_sort_key(bare, 5)[0] == -1.0
    assert workload_sort_key(workload, 5)[0] == 0.5
    assert workload_sort_key(workload, 8)[0] == 3 * 3600
    assert workload_sort_key(workload, 1)[0] == "Deployment"
    assert workload_sort_key(workload, 2)[0] == "api"
    assert workload_sort_key(workload, 0)[0] == "ns"


def test_pod_sort_key_covers_every_column() -> None:
    pod = PodInfo("ns", "Web", "Running", 1, 2, "2d", ("a", "b"), 3, 0.2, 50.0)
    empty = PodInfo("ns", "web", "Weird", 0, 0, "1h", ())

    assert len(POD_SORT_COLUMNS) == 9
    assert pod_sort_key(pod, 1)[0] == 2
    assert pod_sort_key(pod, 3)[:2] == (0.5, 2)
    assert pod_sort_key(empty, 3)[:2] == (1.0, 0)
    assert pod_sort_key(pod, 4)[0] == 3
    assert pod_sort_key(empty, 4)[0] == 4
    assert pod_sort_key(empty, 5)[0] == -1.0
    assert pod_sort_key(pod, 7)[0] == 3
    assert pod_sort_key(pod, 8)[0] == 2 * 86400
    assert pod_sort_key(pod, 2)[0] == "web"
    assert pod_sort_key(pod, 0)[0] == "ns"


def test_job_and_cron_job_states_replace_the_replica_status() -> None:
    complete = Workload("ns", "Job", "j", 1, 1, "1h", state="Complete")
    cron = Workload(
        "ns", "CronJob", "c", 0, 0, "1h", state="Suspended", schedule="* * * * *"
    )

    assert complete.status == "Complete" and cron.status == "Suspended"
    failed = Workload("ns", "Job", "k", 0, 1, "1h", state="Failed")
    assert workload_sort_key(failed, 4) < workload_sort_key(complete, 4)  # worst first
