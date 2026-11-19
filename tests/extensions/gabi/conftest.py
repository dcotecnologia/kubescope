"""Fixtures of the tests of Gabi, the extension that ships with the app."""

import pytest


@pytest.fixture(autouse=True)
def no_chosen_assistant_programs():
    """The program, the model and the effort chosen for an assistant are kept
    in the runner; a test starts without."""
    from kubescope.extensions.bundled.gabi import runner

    saved = [
        dict(d)
        for d in (runner.CUSTOM_PROGRAMS, runner.CUSTOM_MODELS, runner.CUSTOM_EFFORTS)
    ]
    for chosen in (runner.CUSTOM_PROGRAMS, runner.CUSTOM_MODELS, runner.CUSTOM_EFFORTS):
        chosen.clear()
    yield
    for chosen, before in zip(
        (runner.CUSTOM_PROGRAMS, runner.CUSTOM_MODELS, runner.CUSTOM_EFFORTS),
        saved,
        strict=True,
    ):
        chosen.clear()
        chosen.update(before)


@pytest.fixture(autouse=True)
def still_panel(monkeypatch):
    """The panel of Gabi shows and goes at once."""
    from kubescope.extensions.bundled.gabi import panel

    monkeypatch.setattr(panel, "ANIMATION_MS", 0)
