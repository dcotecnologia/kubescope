import pytest

from kubescope.models import Workload, format_age


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
    assert order(5) == ["job", "api", "web", "db"]  # youngest first
