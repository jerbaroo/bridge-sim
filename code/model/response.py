"""A recorded time series of responses."""
from enum import Enum
from typing import List, NewType, Tuple

import numpy as np

from model.bridge import Point


# A single response at a point.
Response = NewType("Response", Tuple[float, Point])

# A NumPy array of responses at times and points.
#
# Each row is a timestep and each column a response point.
ResponseArray = NewType("ResponseArray", np.ndarray)


class ResponseType(Enum):
    """The type of a response or sensor."""

    XTranslation = "xtrans"
    YTranslation = "ytrans"
    ZTranslation = "ztrans"
    Stress = "stress"
    Strain = "strain"

    @staticmethod
    def all() -> List["ResponseType"]:
        return [rt for rt in ResponseType]

    def d2(self) -> bool:
        """Is this response type supported by 2D models?"""
        return self != ResponseType.ZTranslation

    def name(self) -> str:
        """Human readable name for a response type."""
        return {
            ResponseType.XTranslation: "X translation",
            ResponseType.YTranslation: "Y translation",
            ResponseType.ZTranslation: "Z translation",
            ResponseType.Stress: "Stress",
            ResponseType.Strain: "Strain",
        }[self]

    def units(self, short: bool = True) -> str:
        """Human readable units (long or short) for a response type."""
        return {
            ResponseType.XTranslation: ("meters", "m"),
            ResponseType.YTranslation: ("meters", "m"),
            ResponseType.ZTranslation: ("meters", "m"),
            ResponseType.Stress: ("kilo Newton", "N/mm²"),
            ResponseType.Strain: ("kilo Newton", ""),
        }[self][int(short)]
