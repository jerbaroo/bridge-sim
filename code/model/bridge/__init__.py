"""Model of a bridge."""
from typing import Callable, List, Tuple, Union
from enum import Enum

import numpy as np

from util import print_i, round_m

# ID for all fiber commands.
_fiber_cmd_id = 1


def _next_fiber_id():
    """Return a new unique fiber ID."""
    global _fiber_cmd_id
    result = _fiber_cmd_id
    _fiber_cmd_id += 1
    return result


class Dimensions(Enum):
    """Whether modeling in 2D or 3D."""
    D2 = "2D"
    D3 = "3D"


class Fix:
    """A node fixed in some degrees of freedom, when 2D modeling.

    Args:
        x_frac: float, fraction of x position in [0 1].
        x: bool, whether to fix x translation.
        y: bool, whether to fix y translation.
        rot: bool, whether to fix rotation.

    TODO: Rename to Support2D and move to absolute position.

    """
    def __init__(
            self, x_frac: float, x: bool = False, y: bool = False,
            z: bool = False, rot: bool = False):
        assert 0 <= x_frac <= 1
        self.x_frac: float = x_frac
        self.x: bool = x
        self.y: bool = y
        self.z: bool = z
        self.rot: bool = rot


class Support3D:
    """A support of the bridge deck, when 3D modeling.

    Args:
        x: float, x position in meters of the center of the support.
        z: float, z position in meters of the support.
        width: float, width in meters of the support.
        height: float, height in meters of the support.

        SIDE_VIEW:
        <------------x----------->
                           <---width--->
        |------------------|-----|-----|----------------------| ↑ h
                            \    |    /                         | e
                             \   |   /                          | i
                              \  |  /                           | g
                               \ | /                            | h
                                \|/                             ↓ t

        TOP_VIEW:
        |-----------------------------------------------------| ↑+
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| 0
        |-----------------------------------------------------| |
        |------------------|-----------|----------------------| | z = -2
        |-----------------------------------------------------| |
        |-----------------------------------------------------| ↓-

    """
    def __init__(
            self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# Supports are either a list of 2D or 3D supports.
Supports = Union[List[Fix], List[Support3D]]


class Point:
    """A point described by three positions in meters: (x, y, z).

    X is along the deck, y is the height, and z is across the deck.

    TODO: Change default arguments to None.

    """
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x: float = round_m(x)
        self.y: float = round_m(y)
        self.z: float = round_m(z)

    def distance(self, point):
        return round_m(np.sqrt(
            ((self.x - point.x) ** 2)
            + ((self.y - point.y) ** 2)
            + ((self.z - point.z) ** 2)))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Lane:
    """A traffic lane spanning the length of a bridge.

    Args:
        z0: float, z ordinate of one edge of the lane in meters.
        z1: float, z ordinate of the other edge of the lane in meters.
        ltr: bool, whether traffic moves left to right, or opposite.

    Attrs:
        z_min, lower z position of the bridge in meters.
        z_min, upper z position of the bridge in meters.

    """
    def __init__(self, z0: float, z1: float, ltr: bool = True):
        self.z_min: float = round_m(min(z0, z1))
        self.z_max: float = round_m(max(z0, z1))
        self.ltr: bool = ltr

    def width(self):
        """Width of the lane in meters."""
        return round_m(self.z_max - self.z_min)

    def z_center(self):
        """Z position of the center of the lane in meters."""
        return round_m(self.z_min + (self.width() / 2))


class Material(Enum):
    Concrete = 1
    Steel = 2


class Layer:
    """A straight line of fibers when describing a Section, when 2D modeling.

    Args:
        y_i, z_i: float, y and z-coordinates of first fiber in line.
        y_j, z_j: float, y and z-coordinates of last fiber in line.
        num_fibers: int, number of fibers along line.
        area_fiber: float, area of each fiber.
        material: Material, material of the fibers.

    """
    def __init__(
            self, y_min: float, z_min: float, y_max: float, z_max: float,
            num_fibers: int, area_fiber: float = 4.9e-4,
            material: Material = Material.Steel):
        assert y_min <= y_max
        assert z_min <= z_max
        self.fiber_cmd_id = _next_fiber_id()
        self.p0 = Point(y=y_min, z=z_min)
        self.p1 = Point(y=y_max, z=z_max)
        self.num_fibers = num_fibers
        self.area_fiber = area_fiber
        self.material = material

    def points(self) -> List[Point]:
        """The points representing each fiber."""
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
    """A rectangular patch when describing a Section, when 2D modeling."""
    def __init__(
            self, y_min: float, z_min: float, y_max: float, z_max: float,
            num_sub_div_z: int = 30, material: Material = Material.Concrete):
        assert y_min <= y_max
        assert z_min <= z_max
        self.fiber_cmd_id = _next_fiber_id()
        self.p0 = Point(y=y_min, z=z_min)
        self.p1 = Point(y=y_max, z=z_max)
        self.num_sub_div_z = num_sub_div_z
        self.material = material

    def points(self) -> List[Point]:
        """Points for the center of each subdivision, starting at min z."""
        # Difference of min and max y.
        dy = abs(self.p0.y - self.p1.y)
        # Difference of one z subdivision.
        d_sub_div_z = abs(self.p0.z - self.p1.z) / self.num_sub_div_z
        # Center of y and center of z for first fiber.
        point = Point(y=self.p0.y + (dy / 2), z=self.p0.z + (d_sub_div_z / 2))
        return [
            Point(
                y=point.y,
                z=point.z + (d_sub_div_z * sub_div_z))
            for sub_div_z in range(self.num_sub_div_z)]


class Section:
    """A section composed of fibers (Patch and Layer), when 2D modeling."""

    next_id = 1

    def __init__(self, patches: List[Patch] = [], layers: List[Layer] = []):
        self.id = Section.next_id
        Section.next_id += 1
        self.patches = patches
        self.layers = layers

    def _min_max(
            self, direction: Callable[[Point], float]) -> Tuple[float, float]:
        """The min and max values (in given direction) for this section."""
        _min, _max = np.inf, -np.inf
        for layer in self.layers:
            for point in layer.points():
                _min = np.min([_min, direction(point)])
                _max = np.max([_max, direction(point)])
        for patch in self.patches:
            for point in [patch.p0, patch.p1]:
                _min = np.min([_min, direction(point)])
                _max = np.max([_max, direction(point)])
        return _min, _max

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max values in y for this section."""
        return self._min_max(lambda p: p.y)

    def z_min_max(self) -> Tuple[float, float]:
        """The min and max values in z for this section."""
        return self._min_max(lambda p: p.z)


class Bridge:
    """A bridge specification.

    Args:
        name: str, the name of the bridge.
        length: float, length of the bridge in meters.
        width: float, width of the bridge in meters.
        height: float, height of the bridge in meters.
        supports: Supports, a list of supports for 2D or 3D modeling.
        lanes: List[Lane], lanes that span the bridge, where to place loads.
        sections: List[Section], specification of the bridge's cross section,
            only used in 2D modeling.

    """
    def __init__(
            self, name: str, length: float, fixed_nodes: Supports,
            sections: List[Section], lanes: List[Lane],
            dimensions: Dimensions = Dimensions.D2):
        self.name = name
        self.fixed_nodes = fixed_nodes
        self.sections = sections
        self.lanes = lanes
        self.dimensions = dimensions
        self.x_min, self.x_max = 0, length
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_min, self.y_max = self.sections[0].y_min_max()
        self.y_center = (self.y_min + self.y_max) / 2
        self.z_min, self.z_max = self.sections[0].z_min_max()
        self.z_center = (self.z_min + self.z_max) / 2
        self.length = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.width = self.z_max - self.z_min
        print_i(
            f"Bridge dimensions:"
            + f"\n\tx = ({self.x_min}, {self.x_max})"
            + f"\n\ty = ({self.y_min}, {self.y_max})"
            + f"\n\tz = ({self.z_min}, {self.z_max})")

        assert self.length == length  # Sanity check.
        assert self.x_min < self.x_max
        assert self.y_min < self.y_max
        assert self.z_min < self.z_max

        if len(sections) != 1:
            raise ValueError(f"Max 1 section supported, was {len(sections)}")
        if self.fixed_nodes and not self.fixed_nodes[0].x:
            raise ValueError("First fixed node must be fixed in x direction")
        # for i, lane in enumerate(lanes):
        #     if lane.z_min < self.z_min:
        #         raise ValueError(
        #             f"Lane {i} lower position {lane.z_min} less than bridge"
        #             + f" {self.z_min}")
        #     if lane.z_min > self.z_max:
        #         raise ValueError(
        #             f"Lane {i} lower position {lane.z_min} greater than bridge"
        #             + f" {self.z_max}")
        #     if lane.z_max < self.z_min:
        #         raise ValueError(
        #             f"Lane {i} upper position {lane.z_max} less than bridge"
        #             + f" {self.z_min}")
        #     if lane.z_min > self.z_max:
        #         raise ValueError(
        #             f"Lane {i} upper position {lane.z_max} greater than bridge"
        #             + f" {self.z_max}")

    def x_axis(self) -> List[float]:
        """Position of supports in meters along the bridge's x-axis."""
        return np.interp(
            [f.x_frac for f in self.fixed_nodes], [0, 1], [0, self.length])

    def x_axis_equi(self, n) -> List[float]:
        """n equidistant values along the bridge's x-axis, in meters."""
        return np.interp(np.linspace(0, 1, n), [0, 1], [0, self.length])

    def x_frac(self, x: float):
        assert self.x_min <= x <= self.x_max
        return np.interp(x, [self.x_min, self.x_max], [0, 1])

    def x(self, x_frac: float):
        assert 0 <= x_frac <= 1
        return np.interp(x_frac, [0, 1], [self.x_min, self.x_max])

    def y_frac(self, y: float):
        assert self.y_min <= y <= self.y_max
        return np.interp(y, [self.y_min, self.y_max], [0, 1])

    def y(self, y_frac: float):
        assert 0 <= y_frac <= 1
        return np.interp(y_frac, [0, 1], [self.y_min, self.y_max])

    def z_frac(self, z: float):
        assert self.z_min <= z <= self.z_max
        return np.interp(z, [self.z_min, self.z_max], [0, 1])

    def z(self, z_frac: float):
        assert 0 <= z_frac <= 1
        return np.interp(z_frac, [0, 1], [self.z_min, self.z_max])


def _reset_model_ids():
    """Gets called for you when constructing a Config."""
    global _fiber_cmd_id
    _fiber_cmd_id = 1
    Section.next_id = 1
