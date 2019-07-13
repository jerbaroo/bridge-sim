"""Classes for modeling bridges and loads."""
from enum import Enum

import numpy as np


class Fix:
    """A node fixed in some degrees of freedom.

    Args:
        x_frac: float, fraction in [0 1] of x length.
        x: bool, whether to fix x translation.
        y: bool, whether to fix y translation.
        rot: bool, whether to fix rotation.
    """
    def __init__(self, x_frac, x=False, y=False, rot=False):
        assert x_frac >= 0 and x_frac <= 1
        self.x_frac = x_frac
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
    """A load to apply to a bridge, either a point or axle-based load.

    TODO: Where is axle-based load placed on the bridge.

    Args:
        x_frac: float, fraction of x position in [0 1].
        kgs: float or [float], point load or weight at each axle in kgs.
        lane: int, 0 is the first lane.
        axle_distances: None or [float], distances between axles, in meters.
        axle_width: None or float, width of an axle, in meters.
        quadim: None or (float, float): length and width of wheel, in meters.
    """
    def __init__(self, x_frac, kgs, lane=0, axle_distances=None,
                 axle_width=None, quadim=None):
        assert x_frac >= 0 and x_frac <= 1
        self.x_frac = x_frac
        self.kgs = kgs
        self.lane = lane
        self.axle_distances = axle_distances
        self.axle_width = axle_width
        self.quadim = quadim
        if isinstance(kgs, list) or axle_distances:
            if len(kgs) != len(axle_distances) + 1:
                raise ValueError(
                    "Length of axle_distances and kgs don't correspond")

    def total_kgs(self):
        """The total weight in kgs of this load."""
        if self.axle_distances:
            return sum(kgs for kgs in self.kgs)
        return self.kgs

    def __repr__(self):
        """Human readable representation of this load."""
        load_type = ("point" if self.axle_distances is None
                     else f"{len(selx.axle_distances) + 1}-axle")
        return f"{self.total_kgs} kgs, lane {self.lane}, {load_type} load"

    def __str__(self):
        """String uniquely respresenting this load."""
        return f"({self.x_frac:.2f}, {self.kgs:.2f})"


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
    """A point described as (x, y, z).

    x is with the beam, y across the beam, and z is the height.

    """
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


_bridge_705_piers = [0]  # Pier locations in meters.
for span_distance in [12.75, 15.30, 15.30, 15.30, 15.30, 15.30, 12.75]:
    _bridge_705_piers.append(_bridge_705_piers[-1] + span_distance)
_bridge_705_length = 102

bridge_705 = Bridge(
    length=_bridge_705_length,
    width=33.2,
    lanes=[Lane(4, 12.4), Lane(20.8, 29.2)],
    fixed_nodes=[Fix(x / _bridge_705_length, y=True)
                 for x in _bridge_705_piers],
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
