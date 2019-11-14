"""Decides when to start and stop recording an event."""
from typing import Callable

from model.response import Event, TimeSeries


class Trigger:
    """Decides when to start and stop recording an event."""

    def __init__(
        self,
        name: str,
        description: str,
        start: Callable[[TimeSeries], bool],
        stop: Callable[[TimeSeries, Event], bool] = None,
    ):
        self.name = name
        self.description = description
        self.start = start
        self.stop = (lambda _e, _h: False) if stop is None else stop


def always_trigger() -> Trigger:
    """A trigger that always fires."""
    return Trigger("always", "always", lambda _: True)


def abs_threshold_trigger(threshold: float) -> Trigger:
    """A trigger that fires when an absolute threshold is exceeded."""
    return Trigger(
        f"abs-threshold-{threshold:.2f}",
        f"when |response| exceeds {threshold:.2f}",
        lambda xs: abs(xs[-1]) > threshold,
    )
