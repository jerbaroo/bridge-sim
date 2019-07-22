"""Classes for modeling bridges and loads."""
from __future__ import annotations
from enum import Enum
from typing import List

import numpy as np


class Fix:
    """A node fixed in some degrees of freedom, used to model a pier.

    Args:
        x_frac: float, fraction in [0 1] of x length.
        x: bool, whether to fix x translation.
        y: bool, whether to fix y translation.
        rot: bool, whether to fix rotation.

    """
    def __init__(self, x_frac: float, x: bool=False, y: bool=False,
                 rot: bool=False):
        assert x_frac >= 0 and x_frac <= 1
        self.x_frac = x_frac
        self.x = x
        self.y = y
        self.rot = rot


class Lane:
    """A traffic lane spanning the length of a bridge.

    Args:
        z0: float, z ordinate of one edge of the lane in meters.
        z1: float, z ordinate of the other edge of the lane in meters.
        left_to_right: bool, whether traffic moves left to right, or opposite.

    """
    def __init__(self, z0: float, z1: float, left_to_right: bool=True):
        self.z0 = min(z0, z1)
        self.z1 = max(z0, z1)
        self.left_to_right = left_to_right

    def width(self):
        """Width of the lane in meters."""
        return self.z1 - self.z0

    def z_center(self):
        """Z ordinate of the center of the lane in meters."""
        return self.z0 + (self.width() / 2)


class Load:
    """A load to apply to a bridge, either a point or axle-based load.

    Args:
        x_frac: float, fraction of x position in [0 1].
        kn: float, point load intensity or force per axle, in kN.
        lane: int, 0 is the first lane.
        axle_distances: None or [float], distances between axles in meters.
        axle_width: None or float, width of an axle in meters.
        quadim: None or (float, float): length and width of wheel in meters.

    """
    def __init__(self, x_frac: float, kn: float, lane: int=0,
                 axle_distances: List[float]=None, axle_width: float=2,
                 quadim: (float, float)=(0.4, 0.2)):
        assert x_frac >= 0 and x_frac <= 1
        self.x_frac = x_frac
        self.kn = kn
        self.lane = lane
        self.axle_distances = axle_distances
        self.num_axles = (None if self.axle_distances is None
                          else len(self.axle_distances) + 1)
        self.axle_width = axle_width
        self.quadim = quadim

    def is_point_load(self):
        """Whether this load is a point load."""
        return self.axle_distances is None

    def total_kn(self):
        """The total weight in kN of this load."""
        if self.is_point_load():
            return self.kn
        return sum(self.kn for _ in range(self.num_axles))

    def __repr__(self):
        """Human readable representation of this load."""
        load_type = ("point" if self.is_point_load()
                     else f"{len(self.axle_distances) + 1}-axle")
        return f"{self.total_kn()} kN, lane {self.lane}, {load_type} load"

    def __str__(self):
        """String uniquely respresenting this load."""
        return f"({self.x_frac:.2f}, {self.total_kn():.2f})"


class MovingLoad:
    """A load with a constant speed."""
    def __init__(self, load: Load, kmph: float, left_to_right: bool=True):
        self.load = load
        self.kmph = kmph
        self.mps = self.kmph / 3.6
        self.left_to_right = left_to_right

    def x_frac_at(self, time: float, bridge: Bridge):
        """Fraction of bridge length after given time.

        Args:
            time: float, time in seconds.
        """
        delta_frac = (self.mps * time) / bridge.length
        print(type(self))
        if not self.left_to_right:
            delta_frac *= 1
        return self.load.x_frac + delta_frac

    def x_at(self, time: float, bridge: Bridge):
        """X ordinate of bridge in meters after given time.

        Args:
            time: float, time in seconds.
        """
        return bridge.x(self.x_frac_at(time, bridge))


class DisplacementCtrl:
    """Apply a load in simulation until the displacement is reached.

    Args:
        displacement: float, displacement in meters.
        pier: int, index of the pier (fixed node) starting at 0.

    """
    def __init__(self, displacement: float, pier: int):
        self.displacement = displacement
        self.pier = pier


class Material(Enum):
    Concrete = 1
    Steel = 2


# ID for all fiber commands.
_fiber_cmd_id = 1


class Patch:
    """A rectangular patch, used to describe a Section."""
    def __init__(self, y_i: float, z_i: float, y_j: float, z_j: float,
                 num_sub_div_z: int=30, material: Material=Material.Concrete):
        global _fiber_cmd_id
        self.fiber_cmd_id = _fiber_cmd_id
        _fiber_cmd_id += 1
        self.p0 = Point(y=y_i, z=z_i)
        self.p1 = Point(y=y_j, z=z_j)
        self.num_sub_div_z = num_sub_div_z
        self.material = material

    def center(self):
        """Point in the center of this patch."""
        dy = abs(self.p0.y - self.p1.y)
        dz = abs(self.p0.z - self.p1.z)
        point = Point(y=min(self.p0.y, self.p1.y) + (dy / 2),
                      z=min(self.p0.z, self.p1.z) + (dz / 2))
        def assertBetween(a, b, c):
            assert (a < c and c < b) or (b < c and c < a)
        assertBetween(self.p0.y, self.p1.y, point.y)
        assertBetween(self.p0.z, self.p1.z, point.z)
        return point


class Layer:
    """A straight line of fibers, used to describe a Section.

    Args:
        y_i, z_i: float, y and z-coordinates of first fiber in line.
        y_j, z_j: float, y and z-coordinates of last fiber in line.
        num_fibers: int, number of fibers along line.
        area_fiber: float, area of each fiber.
        material: Material, material of the fibers.
    """
    def __init__(self, y_i: float, z_i: float, y_j: float, z_j: float,
                 num_fibers: int, area_fiber: float,
                 material: Material=Material.Steel):
        global _fiber_cmd_id
        self.fiber_cmd_id = _fiber_cmd_id
        _fiber_cmd_id += 1
        self.p0 = Point(y=y_i, z=z_i)
        self.p1 = Point(y=y_j, z=z_j)
        self.num_fibers = num_fibers
        self.area_fiber = area_fiber
        self.material = material

    def points(self):
        """The points respresenting each fiber."""
        dy = (self.p1.y - self.p0.y) / (self.num_fibers - 1)
        dz = (self.p1.z - self.p0.z) / (self.num_fibers - 1)
        y, z = self.p0.y, self.p0.z
        points = [Point(y=y, z=z)]
        for i in range(self.num_fibers - 1):
            y += dy
            z += dz
            points.append(Point(y=y, z=z))
        return points


class Point:
    """A point described as (x, y, z).

    x is with the beam, y across the beam, and z is the height.

    """
    def __init__(self, x: float=None, y: float=None, z: float=None):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Response:
    """A sensor response collected from a simulation."""
    def __init__(self, value: float, x: float=None, y: float=None,
                 z: float=None, time: int=0, elem_id: int=None,
                 srf_id: int=None, node_id: int=None, section_id: int=None,
                 fiber_cmd_id: int=None):
        self.value = value
        self.point = Point(x=x, y=y, z=z)
        self.time = time
        self.node_id = node_id
        self.elem_id = elem_id
        self.srf_id = srf_id
        self.section_id = section_id
        self.fiber_cmd_id = fiber_cmd_id

    def __str__(self):
        """Readable representation of a sensor response."""
        str_if = lambda s, b: "" if b else s
        return (f"{self.value}"
               + f" at (x={self.point.x}, y={self.point.y}, z={self.point.z})"
               + f" t={self.time}"
               + str_if(f" node_id={self.node_id}", self.node_id)
               + str_if(f" elem_id={self.elem_id}", self.elem_id)
               + str_if(f" srf_id={self.srf_id}", self.srf_id)
               + str_if(f" section_id={self.section_id}", self.section_id)
               + str_if(f" fiber_cmd_id={self.fiber_cmd_id}",
                        self.fiber_cmd_id))


class ResponseType(Enum):
    XTranslation = "xtrans"
    YTranslation = "ytrans"
    Stress = "stress"
    Strain = "strain"


def response_type_name(response_type: ResponseType):
    """Human readable name for a response type."""
    return {
        ResponseType.XTranslation: "x translation",
        ResponseType.YTranslation: "y translation",
        ResponseType.Stress: "stress",
        ResponseType.Strain: "strain",
    }[response_type]


def response_type_units(response_type: ResponseType, short: bool=True):
    """Human readable units (long or short) for a response type."""
    return {
        ResponseType.XTranslation: ("meters", "m"),
        ResponseType.YTranslation: ("meters", "m"),
        ResponseType.Stress: ("kilo newton", "kN"),
        ResponseType.Strain: ("kilo newton", "kN")
    }[response_type][int(short)]


class Section:
    """A section composed of fibers."""
    next_id = 1
    def __init__(self, patches: List[Patch]=[], layers: List[Layer]=[]):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches
        self.layers = layers


def reset_model_ids():
    """Call this before constructing a bridge/loads etc.."""
    global _fiber_cmd_id
    _fiber_cmd_id = 1
    Section.next_id = 1


class Bridge:
    """A bridge specification.

    Args:
        length: float, length of the beam in meters.
        width: float, width of the bridge in meters.
        fixed_nodes: [Fix], nodes fixed in some degrees of freedom (piers).
        sections: [Section], description of the bridge's cross section.
        lanes: [Lane], lanes that span the bridge, where to place loads.

    """
    def __init__(self, length: float, width: float, fixed_nodes: List[Fix]=[],
                 sections: List[Section]=[], lanes: List[Lane]=[]):
        self.length = length
        self.width = width
        self.fixed_nodes = fixed_nodes
        self.sections = sections
        self.lanes = lanes
        if len(sections) != 1:
            raise ValueError("Only single sections are supported")
        if not self.fixed_nodes[0].x:
            raise ValueError("First fixed node must be fixed in x direction")

    def x_axis(self):
        """Fixed points in meters along the bridge's length."""
        return np.interp(
            [f.x_frac for f in self.fixed_nodes],
            [0, 1], [0, self.length])

    def x_frac(self, x: float):
        return x / self.length

    def x(self, x_frac: float):
        return x_frac * self.length


def bridge_705() -> Bridge:

    _bridge_705_piers = [0]  # Pier locations in meters.
    for span_distance in [12.75, 15.30, 15.30, 15.30, 15.30, 15.30, 12.75]:
        _bridge_705_piers.append(_bridge_705_piers[-1] + span_distance)
    _bridge_705_length = 102
    fixed_nodes = [Fix(x / _bridge_705_length, y=True)
                   for x in _bridge_705_piers]
    fixed_nodes[0].x = True

    bridge = Bridge(
        length=_bridge_705_length,
        width=33.2,
        lanes=[Lane(4, 12.4), Lane(20.8, 29.2)],
        fixed_nodes=fixed_nodes,
        sections=[Section(
            patches=[
                Patch(-0.2, -1.075, 0, 1.075),
                Patch(-1.25, -0.25, -0.2, 0.25)
            ], layers=[
                Layer(-0.04, -1.035, -0.04, 0.21, num_fibers=16, area_fiber=4.9e-4),
                Layer(-1.21, -0.21, -1.21, 0.21, num_fibers=5, area_fiber=4.9e-4),
                Layer(-1.16, -0.21, -1.16, 0.21, num_fibers=6, area_fiber=4.9e-4)
            ]
        )]
    )
    return bridge
