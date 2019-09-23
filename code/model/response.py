"""A recorded time series of responses."""
from enum import Enum
from typing import List, NewType

# A single response without additional information.
Response_ = NewType("Response", float)

# A time series of responses without additional information.
TimeSeries = NewType("Responses", List[Response_])


class ResponseType(Enum):
    """The type of a response or sensor."""

    XTranslation = "xtrans"
    YTranslation = "ytrans"
    ZTranslation = "ztrans"
    Stress = "stress"
    Strain = "strain"

    def name(self) -> str:
        """Human readable name for a response type."""
        return {
            ResponseType.XTranslation: "X translation",
            ResponseType.YTranslation: "Y translation",
            ResponseType.ZTranslation: "Z translation",
            ResponseType.Stress: "Stress",
            ResponseType.Strain: "Strain"
        }[self]

    def units(self, short: bool = True) -> str:
        """Human readable units (long or short) for a response type."""
        return {
            ResponseType.XTranslation: ("meters", "m"),
            ResponseType.YTranslation: ("meters", "m"),
            ResponseType.ZTranslation: ("meters", "m"),
            ResponseType.Stress: ("kilo newton", "kN"),
            ResponseType.Strain: ("kilo newton", "kN")
        }[self][int(short)]


class Event:
    """A recorded time series of responses."""
    def __init__(
            self, time_series: TimeSeries = None, noise: TimeSeries = None,
            axle_time_series: List[TimeSeries] = None,
            axle_noise: List[TimeSeries] = None, overlap: int = None,
            start_index: int = None):
        self.time_series = time_series
        self.noise = noise
        self.axle_time_series = axle_time_series
        self.axle_noise = axle_noise
        self.overlap = overlap
        self.start_index = start_index

    def get_time_series(self, noise: bool = True):
        """Return the time series optionally with noise."""
        if self.time_series is None:
            raise ValueError("Time series not defined")
        if not noise:
            return self.time_series
        return list(sum(x) for x in zip(self.time_series, self.noise))

    def get_axle_time_series(self, noise: bool = True):
        """Return the axle time series optionally with noise."""
        if self.axle_time_series is None:
            raise ValueError("Axle time series not defined")
        if not noise:
            return self.axle_time_series
        return list(
            sum(x) for x in zip(self.axle_time_series, self.axle_noise))
