"""The time zone the dates and times are shown in.

No Qt. "auto" is the local time of the computer; otherwise it is an IANA
name such as `America/Sao_Paulo` or `UTC`.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

AUTO = "auto"

_chosen = AUTO

COMMON = (
    "UTC",
    "America/Sao_Paulo",
    "America/New_York",
    "Europe/London",
    "Asia/Tokyo",
)


def is_timezone(name: object) -> bool:
    if not isinstance(name, str) or not name or name == AUTO:
        return False
    try:
        ZoneInfo(name)
    except Exception:  # unknown, malformed or without data on this system
        return False
    return True


def set_timezone(name: str) -> None:
    """Choose the zone; anything that is not a known zone means the local
    time."""
    global _chosen
    _chosen = name if is_timezone(name) else AUTO


def timezone_choices() -> list[str]:
    """The zones, the ones most people pick first, then the rest A to Z."""
    rest = sorted(available_timezones() - set(COMMON))
    return [*(name for name in COMMON if is_timezone(name)), *rest]


def to_zone(moment: datetime) -> datetime:
    """The moment in the chosen zone (an aware one; a naive one is local
    time)."""
    if _chosen == AUTO:
        return moment.astimezone()
    return moment.astimezone(ZoneInfo(_chosen))


def zone_now() -> datetime:
    return to_zone(datetime.now().astimezone())
