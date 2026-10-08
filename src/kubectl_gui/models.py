from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Workload:
    namespace: str
    kind: str
    name: str
    ready: int
    desired: int
    age: str

    @property
    def status(self) -> str:
        if self.desired == 0:
            return "Scaled to zero"
        if self.ready == self.desired:
            return "Healthy"
        if self.ready > 0:
            return "Degraded"
        return "Unavailable"


@dataclass(frozen=True, slots=True)
class PodInfo:
    namespace: str
    name: str
    phase: str
    ready: int
    total: int
    age: str
    containers: tuple[str, ...]


def format_age(seconds: float) -> str:
    if seconds < 60:
        return "<1m"
    if seconds < 3600:
        return f"{int(seconds // 60)}m"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h"
    return f"{int(seconds // 86400)}d"
