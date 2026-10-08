import pytest

from kubectl_gui.models import Workload, format_age


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
