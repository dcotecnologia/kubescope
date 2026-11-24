"""Which Pod took the place of one that was deleted or evicted.

No Qt. A Pod of a workload that is gone is replaced by another of the
same owner that runs and is ready; a StatefulSet makes the new one with
the same name, so the one that was born after the deletion is the
replacement.
"""

from collections.abc import Sequence

from kubescope.sdk.models import PodInfo, age_seconds

WATCH_SECONDS = 180.0  # how long the replacement is waited for
POLL_SECONDS = 4.0  # between two looks at the Pods


def _siblings(gone: PodInfo, pod: PodInfo) -> bool:
    """Whether `pod` belongs to the one that went: the same owner, or the same
    name up to the last word when the owner is not known."""
    if gone.owner is not None:
        return pod.owner == gone.owner
    return pod.name.rsplit("-", 1)[0] == gone.name.rsplit("-", 1)[0]


def replacement_for(
    gone: PodInfo, pods: Sequence[PodInfo], waited: float
) -> PodInfo | None:
    """The Pod that runs and is ready in the place of `gone`, `waited` seconds
    after it was deleted, or None while there is none."""
    for pod in pods:
        if (
            pod.namespace != gone.namespace
            or pod.phase != "Running"
            or pod.total == 0
            or pod.ready != pod.total
            or not _siblings(gone, pod)
        ):
            continue
        if pod.name != gone.name or age_seconds(pod.age) < waited:
            return pod  # another Pod, or the same name born after the delete
    return None
