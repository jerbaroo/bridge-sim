"""A recorded time series of responses."""
from enum import Enum
from typing import List, NewType, Tuple

import numpy as np

from lib.model.bridge import Point


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
    StressT = "stresst"
    StressZZB = "stresszzb"
    Strain = "strain"
    StrainT = "straint"
    StrainZZB = "strainzzb"

    @staticmethod
    def all() -> List["ResponseType"]:
        return [rt for rt in ResponseType]

    def d2(self) -> bool:
        """Is this response type supported by 2D models?"""
        return self != ResponseType.ZTranslation

    def ss_direction(self) -> str:
        """Direction identifier for stress or strain."""
        if self in [ResponseType.Stress, ResponseType.Strain]:
            return "XXB"
        elif self in [ResponseType.StressT, ResponseType.StrainT]:
            return "XXT"
        elif self in [ResponseType.StressZZB, ResponseType.StrainZZB]:
            return "ZZB"
        else:
            raise ValueError("Not stress or strain")

    def name(self) -> str:
        """Human readable name for a response type."""
        return {
            ResponseType.XTranslation: "X translation",
            ResponseType.YTranslation: "Y translation",
            ResponseType.ZTranslation: "Z translation",
            ResponseType.Stress: "Stress",
            ResponseType.StressT: "Stress",
            ResponseType.StressZZB: "Stress ZZB",
            ResponseType.Strain: "Strain",
            ResponseType.StrainT: "Top strain",
            ResponseType.StrainZZB: "Strain ZZB",
        }[self]

    def units(self, short: bool = True) -> str:
        """Human readable units (long or short) for a response type."""
        return {
            ResponseType.XTranslation: ("meters", "m"),
            ResponseType.YTranslation: ("meters", "m"),
            ResponseType.ZTranslation: ("meters", "m"),
            ResponseType.Stress: ("kilo Newton", "N/mm²"),
            ResponseType.StressT: ("kilo Newton", "N/mm²"),
            ResponseType.StressZZB: ("kilo Newton", "N/mm²"),
            ResponseType.Strain: ("kilo Newton", ""),
            ResponseType.StrainT: ("kilo Newton", ""),
            ResponseType.StrainZZB: ("kilo Newton", ""),
        }[self][int(short)]
