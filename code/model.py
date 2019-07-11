"""Classes for modeling bridges and loads."""
from enum import Enum

import numpy as np


class Fix:
    """A node fixed in some degrees of freedom."""
    def __init__(self, x_pos, x=False, y=False, rot=False):
        assert x_pos >= 0 and x_pos <= 1
        self.x_pos = x_pos
        self.x = x
        self.y = y
        self.rot = rot


class Lane:
    """A traffic lane spanning the length of the bridge.

    Args:
        z0: float, z ordinate of one edge of the lane, in meters.
        z1: float, z ordinate of the other edge of the lane, in meters.
    """
    def __init__(self, z0, z1):
        self.z0 = min(z0, z1)
        self.z1 = max(z0, z1)

    def width(self):
        """Width of the lane in meters."""
        return self.z1 - self.z0

    def z_center(self):
        """Z ordinate of the center of the lane, in meters."""
        return self.z0 + (self.width() / 2)


class Load:
    """A load to apply to the bridge."""
    def __init__(self, x_pos, weight, lane=0):
        assert x_pos >= 0 and x_pos <= 1
        self.x_pos = x_pos
        # Rename to kgs.
        self.weight = weight
        self.lane = lane

    def __str__(self):
        return f"({self.x_pos:.2f}, {self.weight:.2f})"


class Material(Enum):
    Concrete = 1
    Steel = 2


# ID for all fiber commands.
_fiber_cmd_id = 1


class Patch:
    """A rectangular patch, used to describe a Section."""
    def __init__(self, y_i, z_i, y_j, z_j, num_sub_div_z=30,
                 material=Material.Concrete):
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
    def __init__(self, y_i, z_i, y_j, z_j, num_fibers, area_fiber,
                 material=Material.Steel):
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
    """A point described as (x, y, z)."""
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Response:
    """A sensor response collected from a simulation."""
    def __init__(self, value, x=None, y=None, z=None, time=0, elem_id=None,
                 srf_id=None, node_id=None, section_id=None, fiber_cmd_id=None):
        self.value = value
        self.point = Point(x=x, y=y, z=z)
        self.time = time
        self.node_id = node_id
        self.elem_id = elem_id
        self.srf_id = srf_id
        self.section_id = section_id
        self.fiber_cmd_id = fiber_cmd_id

    def __str__(self):
        return (f"{self.value}"
               + f" at ({self.point.x}, {self.point.y}, {self.point.z})"
               + f" t={self.time}"
               + ("" if self.node_id is None else f" node_id={self.node_id}")
               + ("" if self.elem_id is None else f" elem_id={self.elem_id}")
               + ("" if self.srf_id is None else f" srf_id={self.srf_id}")
               + ("" if self.section_id is None
                  else f" section_id={self.section_id}")
               + ("" if self.fiber_cmd_id is None
                  else f" fiber_cmd_id={self.fiber_cmd_id}"))


class ResponseType(Enum):
    XTranslation = "xtrans"
    YTranslation = "ytrans"
    Stress = "stress"
    Strain = "strain"


all_response_types = [rt for rt in ResponseType]


class Section:
    """A section composed of fibers."""
    next_id = 1
    def __init__(self, patches=[], layers=[]):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches
        self.layers = layers


class Bridge:
    """Description of a bridge.

    Args:
        length: int, length of the beam in meters.
        width: int, width of the bridge in meters, ignored by OpenSees.
        lanes: [Lane], lanes that span the bridge, where to place loads.
        fixed_nodes: [Fix], nodes fixed in some degrees of freedom (piers).
        sections: [Section], description of the bridge's cross section.

    """
    def __init__(self, length, width, fixed_nodes: [Fix]=[],
                 sections: [Section]=[], lanes: [Lane]=[]):
        self.length = length
        self.width = width
        self.fixed_nodes = fixed_nodes
        self.sections = sections
        self.lanes = lanes
        assert len(sections) == 1

    def x_axis(self, n):
        """n equidistant points along the bridge's length."""
        return np.interp(range(n), [0, n - 1], [0, self.length])


bridge_705 = Bridge(
    length=102,
    width=33.2,
    lanes=[Lane(4, 12.4), Lane(20.8, 29.2)],
    fixed_nodes=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)],
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
