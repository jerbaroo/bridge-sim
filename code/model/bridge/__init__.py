"""Model of a bridge."""
from typing import List
from enum import Enum

import numpy as np

# ID for all fiber commands.
_fiber_cmd_id = 1


class Fix:
    """A node fixed in some degrees of freedom, used to model a pier.

    Args:
        x_frac: float, fraction in [0 1] of x length.
        x: bool, whether to fix x translation.
        y: bool, whether to fix y translation.
        rot: bool, whether to fix rotation.

    """
    def __init__(
            self, x_frac: float, x: bool=False, y: bool=False, rot: bool=False):
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


class Material(Enum):
    Concrete = 1
    Steel = 2


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


class Section:
    """A section composed of fibers."""
    next_id = 1
    def __init__(self, patches: List[Patch]=[], layers: List[Layer]=[]):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches
        self.layers = layers


def reset_model_ids():
    """Called automatically when constructing a Config."""
    global _fiber_cmd_id
    _fiber_cmd_id = 1
    Section.next_id = 1


class Bridge:
    """A bridge specification.

    Args:
        name: str, the name of the bridge.
        length: float, length of the bridge in meters.
        width: float, width of the bridge in meters.
        fixed_nodes: [Fix], nodes fixed in some degrees of freedom (piers).
        sections: [Section], specification of the bridge's cross section.
        lanes: [Lane], lanes that span the bridge, where to place loads.

    """
    def __init__(
            self, name: str, length: float, width: float,
            fixed_nodes: List[Fix], sections: List[Section],
            lanes: List[Lane]):
        self.name = name
        self.length = length
        self.width = width
        self.fixed_nodes = fixed_nodes
        self.sections = sections
        self.lanes = lanes
        if len(sections) != 1:
            raise ValueError(
                f"Only 1 section is currently supported, was {len(sections)}")
        if self.fixed_nodes and not self.fixed_nodes[0].x:
            raise ValueError("First fixed node must be fixed in x direction")

    def x_axis(self) -> List[float]:
        """Fixed nodes in meters along the bridge's x-axis."""
        return np.interp(
            [f.x_frac for f in self.fixed_nodes], [0, 1], [0, self.length])

    def x_axis_equi(self, n) -> List[float]:
        """n equidistant values along the bridge's x-axis, in meters."""
        return np.interp(np.linspace(0, 1, n), [0, 1], [0, self.length])

    def x_frac(self, x: float):
        return x / self.length

    def x(self, x_frac: float):
        return x_frac * self.length
