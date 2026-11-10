from datetime import UTC, datetime

import pytest

from kubescope.settings import Settings
from kubescope.utils import timezone


@pytest.fixture(autouse=True)
def _reset():
    timezone.set_timezone("auto")
    yield
    timezone.set_timezone("auto")


def test_auto_is_local_time():
    moment = datetime(2026, 1, 1, 12, tzinfo=UTC)
    assert timezone.to_zone(moment) == moment.astimezone()


def test_chosen_zone_is_used():
    timezone.set_timezone("Asia/Tokyo")
    moment = datetime(2026, 1, 1, 12, tzinfo=UTC)
    assert timezone.to_zone(moment).hour == 21
    assert timezone.zone_now().tzname() == "JST"


def test_unknown_zone_falls_back_to_auto():
    timezone.set_timezone("Not/AZone")
    assert timezone.zone_now().utcoffset() == datetime.now().astimezone().utcoffset()
    assert not timezone.is_timezone("")
    assert not timezone.is_timezone(3)


def test_settings_default_and_validation(tmp_path):
    settings = Settings(tmp_path / "s.json")
    assert settings.timezone == "auto"
    settings.timezone = "Europe/Lisbon"
    assert settings.timezone == "Europe/Lisbon"
    settings.timezone = "bogus"
    assert settings.timezone == "auto"


def test_the_common_zones_come_first_and_every_zone_is_listed():
    choices = timezone.timezone_choices()
    assert choices[: len(timezone.COMMON)] == list(timezone.COMMON)
    assert "Europe/Lisbon" in choices
    assert len(choices) == len(set(choices))
