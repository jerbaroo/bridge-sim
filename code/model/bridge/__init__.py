"""Model of a bridge."""
from typing import Callable, List, Optional, Tuple, Union
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

    def name(self):
        return {
            Dimensions.D2: "2D",
            Dimensions.D3: "23"
        }[self]


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

    def y_min_max(self) -> Tuple[None, None]:
        """The min and max values in y direction for this support."""
        return None, None

    def z_min_max(self) -> Tuple[None, None]:
        """The min and max values in z direction for this support."""
        return None, None


class Support3D:
    """A support of the bridge deck, when 3D modeling.

        SIDE_VIEW:
        <------------x----------->
                           <---length-->
        |------------------|-----------|----------------------| ↑ h
                            \         /                         | e
                             \       /                          | i
                              \     /                           | g
                               \   /                            | h
                                \ /                             ↓ t

        TOP_VIEW:
        |-----------------------------------------------------| ↑+
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| |
        |-----------------------------------------------------| 0
        |------------------|-----------|----------------------| |
        |------------------|-----------|----------------------| | z = -2
        |------------------|-----------|----------------------| |
        |-----------------------------------------------------| ↓-

        FRONT_VIEW:
                           <---width-top---->
                           |----------------|
                            \              /
                             \            /
                              \          /
                               \        /
                                \______/
                                <------>
                              width-bottom

    Args:
        x: float, x position of the center of the support in meters.
        z: float, z position of the support in meters.
        length: float, length of the support in meters.
        height: float, height of the support in meters.
        width_top: float, width of the top of the support in meters.
        width_bottom: float, width of the bottom of the support in meters.

    """
    def __init__(
            self, x: float, z: float, length: float, height: float,
            width_top: float, width_bottom: float):
        self.x = x
        self.z = z
        self.length = length
        self.height = height
        self.width_top = width_top
        self.width_bottom = width_bottom
        if self.width_top < self.width_bottom:
            raise ValueError(
                "Support3D: top width must be greater than bottom width")

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max values in y direction for this section."""
        return -self.height, 0

    def z_min_max(self) -> Tuple[float, float]:
        """The min and max values in z direction for this section."""
        half_width = self.width_top / 2
        return self.z - half_width, self.z + half_width


# Supports are either 2D or 3D supports.
Support = Union[Fix, Support3D]


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
        y_i, z_i: float, y and z positions in meters of the first fiber.
        y_j, z_j: float, y and z positions in meters of the last fiber.
        num_fibers: int, number of fibers along the line.
        area_fiber: float, area of each fiber.
        material: Material, material of the fibers.

    TODO: Avoid default argument of area_fiber.

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


class Section2D:
    """A section when 2D modeling, composed of fibers (Patch and Layer)."""

    next_id = 1

    def __init__(self, patches: List[Patch] = [], layers: List[Layer] = []):
        self.id = Section2D.next_id
        Section2D.next_id += 1
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


class Section3D:
    """A section when 3D modeling, density, thickness and young's modulus.

    Args:
        density: float, section density in kg/m.
        thickness: float, section thickness in m.
        youngs: float, Young's modulus of the section MPa.
        start_x_frac: float, start of this section as a fraction of x position
            in meters.

    """
    def __init__(
            self, density: float, thickness: float, youngs: float,
            start_x_frac: float = 0):
        self.density = density
        self.thickness = thickness
        self.youngs = youngs

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max values in y for this section."""
        return -self.thickness, 0

    def z_min_max(self) -> Tuple[None, None]:
        return None, None


# Sections are either 2D or 3D sections.
Section = Union[Section2D, Section3D]


class Bridge:
    """A bridge specification.

    Args:
        name: str, the name of the bridge.
        length: float, length of the bridge in meters.
        width: float, width of the bridge in meters.
        supports: List[Support], a list of supports for 2D or 3D modeling.
        lanes: List[Lane], lanes that span the bridge, where to place loads.
        sections: List[Section], specification of the bridge's cross section,
            only used in 2D modeling.

    """
    def __init__(
            self, name: str, length: float, width: float,
            supports: List[Support], sections: List[Section],
            lanes: List[Lane], dimensions: Dimensions):
        self.name = name
        self.supports = supports
        self.sections = sections
        self.lanes = lanes
        self.dimensions = dimensions
        self.x_min, self.x_max = 0, length
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_min, self.y_max = self.y_min_max()
        self.y_center = (self.y_min + self.y_max) / 2
        self.z_min, self.z_max = self.z_min_max()
        self.z_center = (self.z_min + self.z_max) / 2
        self.length = length
        self.width = width
        self.height = self.y_max - self.y_min
        print_i(
            f"Bridge dimensions:"
            + f"\n\tx = ({self.x_min}, {self.x_max})"
            + f"\n\ty = ({self.y_min}, {self.y_max})"
            + f"\n\tz = ({self.z_min}, {self.z_max})")
        self._assert_bridge()

    def y_min_max(self):
        """The min and max values in y direction from supports and sections."""
        return self._min_max(lambda s: s.y_min_max())

    def z_min_max(self):
        """The min and max values in z direction from supports and sections."""
        return self._min_max(lambda s: s.z_min_max())

    def x_axis(self) -> List[float]:
        """Position of supports in meters along the bridge's x-axis."""
        return np.interp(
            [f.x_frac for f in self.supports], [0, 1], [0, self.length])

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

    def _min_max(
            self,
            f: Callable[
                [Union[Support, Section]],
                Tuple[Optional[float], Optional[float]]]
            ) -> Tuple[float, float]:
        """The min and max values in a direction from supports and sections."""
        z_min, z_max = None, None

        def set_z_min(z: float):
            nonlocal z_min
            if z is None: return
            z_min = z if z_min is None or z < z_min else z_min

        def set_z_max(z: float):
            nonlocal z_max
            if z is None: return
            z_max = z if z_max is None or z > z_max else z_max

        for section in self.sections:
            s_z_min, s_z_max = f(section)
            set_z_min(s_z_min)
            set_z_max(s_z_max)

        for support in self.supports:
            s_z_min, s_z_max = f(support)
            set_z_min(s_z_min)
            set_z_max(s_z_max)

        return z_min, z_max

    def _assert_bridge(self):
        """Assert this bridge makes sense."""
        assert self.x_min < self.x_max
        assert self.y_min < self.y_max
        assert self.z_min < self.z_max
        assert self.length == self.x_max - self.x_min
        assert self.width == self.z_max - self.z_min
        if self.dimensions == Dimensions.D2:
            self._assert_2d()
        else:
            self._assert_3d()

    def _assert_2d(self):
        if self.supports and not self.supports[0].x:
            # TODO: Check self.supports[0].x == 0.
            raise ValueError(
                "2D bridge must have node at x=0 fixed in x direction")
        if len(self.sections) != 1:
            raise ValueError("2D bridge must have exactly 1 section")
        for support in self.supports:
            if not isinstance(support, Fix):
                raise ValueError("2D bridge must use Fix supports")

    def _assert_3d(self):
        for support in self.supports:
            if not isinstance(support, Support3D):
                raise ValueError("3D bridge must use Support3D supports")

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


def _reset_model_ids():
    """Gets called for you when constructing a Config."""
    global _fiber_cmd_id
    _fiber_cmd_id = 1
    Section2D.next_id = 1
