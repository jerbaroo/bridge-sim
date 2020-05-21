"""All classes: bridges, simulation, vehicles etc."""
# This module should import no other bridge_sim modules!

from enum import Enum
from typing import List

import numpy as np

from util import safe_str

DIST_DECIMALS: int = 6


class PierSettlement:
    def __init__(self, pier: int, settlement: float):
        """A vertical translation applied in simulation to a pier.

        :param pier: index of a pier on a bridge.
        :param settlement: amount of pier settlement to apply.
        :return: A pier settlement object.
        """
        self.pier = pier
        self.settlement = settlement

    def id_str(self):
        return safe_str(f"{np.around(self.settlement, 3)}-{self.pier}")


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """A point described by three positions: (X, Y, Z).

        :param x:
        :param y:
        :param z:
        """
        self.x: float = np.around(x, DIST_DECIMALS)
        self.y: float = np.around(y, DIST_DECIMALS)
        self.z: float = np.around(z, DIST_DECIMALS)

    def distance(self, point):
        return np.around(np.sqrt(
            ((self.x - point.x) ** 2)
            + ((self.y - point.y) ** 2)
            + ((self.z - point.z) ** 2)
        ), DIST_DECIMALS)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class PointLoad:
    def __init__(self, x: float, z: float, load: float):
        """A point load applied in simulation.

        :param x: X position on a bridge.
        :param z: Z position on a bridge.
        :param load: intensity of the point load.
        :return: A point load object.
        """
        self.x = x
        self.z = z
        self.load = load

    def __repr__(self):
        """Human readable representation."""
        return f"x = {self.x}, z = {self.z}, load = {self.load}"

    def id_str(self):
        """String uniquely representing this point load."""
        return safe_str(f"({np.around(self.x, DIST_DECIMALS)}, {np.around(self.z, DIST_DECIMALS)}, {np.around(self.load, DIST_DECIMALS)})")

    def point(self) -> Point:
        """The 'Point' part of this point load."""
        return Point(x=self.x, y=0, z=self.z)


class ResponseType(Enum):
    """A simulation response type."""

    XTrans = "xtrans"
    YTrans = "ytrans"
    ZTrans = "ztrans"
    StressXXB = "stressxxb"
    StressXXT = "stressxxt"
    StressZZB = "stresszzb"
    StrainXXB = "strainxxb"
    StrainXXT = "strainxxt"
    StrainZZB = "strainzzb"

    @staticmethod
    def all() -> List["ResponseType"]:
        """A list of all response types."""
        return [rt for rt in ResponseType]

    def is_stress(self):
        """Is this response type a stress type?"""
        return self in [ResponseType.StressXXB, ResponseType.StressXXT, ResponseType.StressZZB]

    def is_strain(self):
        """Is this response type a strain type?"""
        return self in [ResponseType.StrainXXB, ResponseType.StrainXXT, ResponseType.StrainZZB]

    def ss_direction(self) -> str:
        """A stress or strain identifier e.g. XXB is applicable."""
        if self.is_stress() or self.is_strain():
            return self.name()[-3:]
        raise ValueError("Not stress or strain")

    def name(self) -> str:
        """Human readable name for a response type."""
        return {
            ResponseType.XTrans: "X translation",
            ResponseType.YTrans: "Y translation",
            ResponseType.ZTrans: "Z translation",
            ResponseType.StressXXB: "Stress XXB",
            ResponseType.StressXXT: "Stress XXT",
            ResponseType.StressZZB: "Stress ZZB",
            ResponseType.StrainXXB: "Strain XXB",
            ResponseType.StrainXXT: "Strain XXT",
            ResponseType.StrainZZB: "Strain ZZB",
        }[self]

    def units(self, short: bool = True) -> str:
        """Human readable units (long or short) for a response type."""
        return {
            ResponseType.XTrans: ("meters", "m"),
            ResponseType.YTrans: ("meters", "m"),
            ResponseType.ZTrans: ("meters", "m"),
            ResponseType.StressXXB: ("kilo Newton", "N/mm²"),
            ResponseType.StressXXT: ("kilo Newton", "N/mm²"),
            ResponseType.StressZZB: ("kilo Newton", "N/mm²"),
            ResponseType.StrainXXB: ("kilo Newton", ""),
            ResponseType.StrainXXT: ("kilo Newton", ""),
            ResponseType.StrainZZB: ("kilo Newton", ""),
        }[self][int(short)]


# Shorthand for ResponseType.
RT = ResponseType
