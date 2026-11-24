from kubescope.sdk.models import PodInfo

from kubescope.utils.replacement import replacement_for


def pod(
    name, phase="Running", ready=1, total=1, age="5s", owner=("ReplicaSet", "api-1")
):
    return PodInfo("ns", name, phase, ready, total, age, ("app",), owner=owner)


GONE = pod("api-1-aaa", age="2d")


def test_another_pod_of_the_same_owner_that_is_ready_is_the_replacement() -> None:
    pods = [pod("web-1-x", owner=("ReplicaSet", "web-1")), pod("api-1-bbb")]

    assert replacement_for(GONE, pods, 10).name == "api-1-bbb"  # type: ignore[union-attr]


def test_a_pod_that_is_not_ready_or_not_running_or_in_another_namespace_is_not() -> (
    None
):
    other = PodInfo(
        "other", "api-1-ccc", "Running", 1, 1, "5s", ("app",), owner=GONE.owner
    )
    pods = [
        pod("api-1-bbb", ready=0),
        pod("api-1-ddd", phase="Pending"),
        pod("api-1-eee", total=0, ready=0),
        other,
    ]

    assert replacement_for(GONE, pods, 10) is None


def test_with_no_owner_the_name_up_to_the_last_word_tells_the_siblings() -> None:
    gone = pod("batch-job-x1", owner=None)
    pods = [pod("batch-job-y2", owner=None), pod("other-y2", owner=None)]

    assert replacement_for(gone, pods, 10).name == "batch-job-y2"  # type: ignore[union-attr]
    assert replacement_for(gone, [pod("other-y2", owner=None)], 10) is None


def test_a_statefulset_pod_counts_only_when_born_after_the_delete() -> None:
    gone = pod("db-0", age="9d", owner=("StatefulSet", "db"))

    assert (
        replacement_for(gone, [pod("db-0", age="2d", owner=("StatefulSet", "db"))], 8)
        is None
    )
    new = pod("db-0", age="3s", owner=("StatefulSet", "db"))
    assert replacement_for(gone, [new], 8) is new
