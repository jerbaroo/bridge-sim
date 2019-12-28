"""Model of a bridge."""
from enum import Enum
from itertools import chain
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
from scipy.interpolate import interp1d

from util import print_i, print_s, round_m, safe_str

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
        return {Dimensions.D2: "2D", Dimensions.D3: "3D"}[self]


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
        self,
        x_frac: float,
        x: bool = False,
        y: bool = False,
        z: bool = False,
        rot: bool = False,
    ):
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
        x: float, x position of center of the support in meters.
        z: float, z position of center of the support in meters.
        length: float, length of the support in meters.
        height: float, height of the support in meters.
        width_top: float, width of the top of the support in meters.
        width_bottom: float, width of the bottom of the support in meters.

    """

    def __init__(
        self,
        x: float,
        z: float,
        length: float,
        height: float,
        width_top: float,
        width_bottom: float,
        sections: Union[List["Section3DPier"], Callable[[float], "Section3DPier"]],
        fix_x_translation: bool,
        fix_y_translation: bool,
        fix_z_translation: bool,
        fix_x_rotation: bool,
        fix_y_rotation: bool,
        fix_z_rotation: bool,
    ):
        self.x = x
        self.z = z
        self.length = length
        self.height = height
        self.width_top = width_top
        self.width_bottom = width_bottom
        self.fix_x_translation = fix_x_translation
        self.fix_y_translation = fix_y_translation
        self.fix_z_translation = fix_z_translation
        self.fix_x_rotation = fix_x_rotation
        self.fix_y_rotation = fix_y_rotation
        self.fix_z_rotation = fix_z_rotation
        self.sections = sections
        # Must be callable or a list.
        if not callable(self.sections):
            assert isinstance(self.sections, list)
            assert all(isinstance(s, Section3DPier) for s in self.sections)
        if self.width_top < self.width_bottom:
            raise ValueError("Support3D: top width must be >= bottom width")

    def x_min_max(self) -> Tuple[float, float]:
        """The min and max x positions for this pier."""
        half_length = self.length / 2
        return self.x - half_length, self.x + half_length

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max y positions for this pier."""
        return -self.height, 0

    def z_min_max_top(self) -> Tuple[float, float]:
        """The min and max z positions for the top of this pier."""
        half_top = self.width_top / 2
        return self.z - half_top, self.z + half_top


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
        return round_m(
            np.sqrt(
                ((self.x - point.x) ** 2)
                + ((self.y - point.y) ** 2)
                + ((self.z - point.z) ** 2)
            )
        )

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Lane:
    """A traffic lane spanning the length of a bridge.

    Args:
        z0: float, z ordinate of one edge of the lane in meters.
        z1: float, z ordinate of the other edge of the lane in meters.
        ltr: bool, whether traffic moves left to right, or opposite.

    Attrs:
        z_min, float, lower z position of the bridge in meters.
        z_min, float, upper z position of the bridge in meters.
        width, float, Width of the lane in meters.

    """

    def __init__(self, z0: float, z1: float, ltr: bool):
        self.z_min: float = round_m(min(z0, z1))
        self.z_max: float = round_m(max(z0, z1))
        self.ltr: bool = ltr
        self.width = round_m(self.z_max - self.z_min)
        self.z_center = round_m(self.z_min + (self.width / 2))


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
        self,
        y_min: float,
        z_min: float,
        y_max: float,
        z_max: float,
        num_fibers: int,
        area_fiber: float = 4.9e-4,
        material: Material = Material.Steel,
    ):
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
        self,
        y_min: float,
        z_min: float,
        y_max: float,
        z_max: float,
        num_sub_div_z: int = 30,
        material: Material = Material.Concrete,
    ):
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
            Point(y=point.y, z=point.z + (d_sub_div_z * sub_div_z))
            for sub_div_z in range(self.num_sub_div_z)
        ]


class Section2D:
    """A section when 2D modeling, composed of fibers (Patch and Layer)."""

    next_id = 1

    def __init__(self, patches: List[Patch] = [], layers: List[Layer] = []):
        self.id = Section2D.next_id
        Section2D.next_id += 1
        self.patches = patches
        self.layers = layers

    def _min_max(self, direction: Callable[[Point], float]) -> Tuple[float, float]:
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
    """A section for describing the deck when 3D modeling.

    Args:
        density: float, section density in kg/m.
        thickness: float, section thickness in m.
        youngs: float, Young's modulus of the section in MPa.
        poisson: float, Poisson's ratio.
        start_x_frac: float, start of the section as a fraction of x position.
        start_z_frac: float, start of the section as a fraction of z position.
        end_x_frac: float, end of the section as a fraction of x position.
        end_z_frac: float, end of the section as a fraction of z position.
        cte: float, coefficient of thermal expansion, in meters per celcius.

    """

    next_id = 1

    def __init__(
        self,
        density: float,
        thickness: float,
        youngs: float,
        poissons: float,
        start_x_frac: float,
        start_z_frac: float,
        end_x_frac: float,
        end_z_frac: float,
        cte: float = 12e-6,
    ):
        self.id = Section3D.next_id
        Section3D.next_id += 1
        self.density = density
        self.thickness = thickness
        self.youngs = youngs
        self.poissons = poissons
        self.start_x_frac = start_x_frac
        self.start_z_frac = start_z_frac
        self.end_x_frac = end_x_frac
        self.end_z_frac = end_z_frac
        self.cte = cte

    def contains(self, bridge: "Bridge", x: float, z: float) -> bool:
        """Whether this section contains the given point."""
        return (self.start_x_frac <= bridge.x_frac(x) <= self.end_x_frac) and (
            self.start_z_frac <= bridge.z_frac(z) <= self.end_z_frac
        )

    def mat_id_str(self):
        """Representation of this section by material properties."""
        return f"{self.density}-{self.thickness}-{self.youngs}-{self.poissons}"

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max values in y for this section."""
        return -self.thickness, 0

    def __repr__(self):
        """Readable representation."""
        return (
            "Section3D"
            + f"\n  starts at (x_frac, z_frac) ="
            + f" ({round_m(self.start_x_frac)}, {round_m(self.start_z_frac)})"
            + f"\n  density = {self.density} kg/m"
            + f"\n  thickness = {self.thickness} m"
            + f"\n  youngs = {self.youngs} MPa"
            + f"\n  poissons = {self.poissons}"
        )


class Section3DPier(Section3D):
    """Like Section3D but intended for describing piers.

    Args:
        density: float, section density in kg/m.
        thickness: float, section thickness in m.
        youngs: float, Young's modulus of the section in MPa.
        poisson: float, Poisson's ratio.
        start_frac_len: start of the section as a fraction of pier length.

    """

    def __init__(
        self,
        density: float,
        thickness: float,
        youngs: float,
        poissons: float,
        start_frac_len: float,
    ):
        super().__init__(
            density=density,
            thickness=thickness,
            youngs=youngs,
            poissons=poissons,
            start_x_frac=None,
            start_z_frac=None,
            end_x_frac=None,
            end_z_frac=None,
        )
        self.start_frac_len = start_frac_len

    def __repr__(self):
        """Readable representation."""
        return (
            "Section3D"
            + f"\n  starts at {round_m(self.start_frac_len)}"
            + f"\n  density = {self.density} kg/m"
            + f"\n  thickness = {self.thickness} m"
            + f"\n  youngs = {self.youngs} MPa"
            + f"\n  poissons = {self.poissons}"
        )


# Deck Sections are either 2D or 3D sections.
Section = Union[Section2D, Section3D]


class Bridge:
    """A bridge specification.

    Args:
        name: str, the name of the bridge.
        length: float, length of the bridge in meters.
        width: float, width of the bridge in meters.
        supports: List[Support], a list of supports in 2D or 3D.
        sections: List[Section], the bridge's cross section in 2D or 3D.
        lanes: List[Lane], lanes that span the bridge, where to place loads.
        dimensions: Dimensions, whether the model is 2D or 3D.
        base_mesh_deck_nodes_x: int, number of nodes of the base mesh in
            longitudinal direction of the bridge deck, minimum is 2.
        base_mesh_deck_nodes_z: Optional[int], number of nodes of the base mesh
            in transverse direction of the bridge deck, minimum is 2.
        base_mesh_pier_nodes_y: Optional[int], number of nodes of the base mesh
            in vertical direction of the piers, minimum is 2.
        base_mesh_pier_nodes_z: Optional[int], number of nodes of the base mesh
            in transverse direction of the piers, minimum is 2.
        single_sections: Optional[Tuple[Section, Section]], if given then
            override the bridge's deck and each pier sections with the given
            values respectively in the tuple, only applies to a 3D model.

    """

    def __init__(
        self,
        name: str,
        accuracy: str,
        length: float,
        width: float,
        supports: List[Support],
        sections: List[Section],
        lanes: List[Lane],
        dimensions: Dimensions,
        base_mesh_deck_max_x: int,
        base_mesh_deck_max_z: int,
        base_mesh_pier_max_y: int,
        single_sections: Optional[Tuple[Section, Section]] = None,
    ):
        self.type = None

        # Given arguments.
        self.name = name
        self.accuracy = accuracy
        self.length = length
        self.width = width
        self.supports = supports
        self.sections = sections
        self.lanes = lanes
        self.dimensions = dimensions

        # Mesh.
        self.base_mesh_deck_max_x = base_mesh_deck_max_x
        self.base_mesh_deck_max_z = base_mesh_deck_max_z
        self.base_mesh_pier_max_y = base_mesh_pier_max_y

        # Attach single section option for asserts and printing info.
        self.single_sections = single_sections
        if self.single_sections is not None:
            self.name += "-single-sections"
            self.sections = [self.single_sections[0]]  # Set deck section.
            for pier in self.supports:  # Set pier sections.
                pier.sections = [self.single_sections[1]]

        # Derived attributes.
        #
        # NOTE: The functions y_min_max and z_min_max calculate the min and max
        # values of the bridge in y and z directions respectively, based on the
        # supports and sections. For a 3D bridge neither supports nor sections
        # contain information on the min or max values in z direction.
        self.x_min, self.x_max = 0, length
        self.y_min, self.y_max = self.y_min_max()
        if dimensions == Dimensions.D2:
            self.z_min, self.z_max = self.z_min_max()
        else:
            self.z_min, self.z_max = -width / 2, width / 2
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2
        self.z_center = (self.z_min + self.z_max) / 2
        self.height = self.y_max - self.y_min

        # Assert the bridge is fine and print info.
        # TODO Move to another file.
        self._assert_bridge()

    def deck_section_at(self, x: float, z: float) -> Section3D:
        """Return the deck section at given position."""
        if len(self.sections) == 1:
            return self.sections[0]

        for section in self.sections:
            if section.contains(bridge=self, x=x, z=z):
                return section

        raise ValueError("No section for x, z = {x}, {z}")

    def print_info(self, c: "Config", pier_fix_info: bool = False):
        """Print summary information about this bridge.

        Args:
            fix_info: print information on pier's fixed nodes.

        """
        print_s(f"Bridge dimensions:")
        print_s(f"  x = ({self.x_min}, {self.x_max})")
        print_s(f"  y = ({self.y_min}, {self.y_max})")
        print_s(f"  z = ({self.z_min}, {self.z_max})")

        print_s(f"Bridge lanes:")
        wheel_tracks = self.wheel_tracks(c)
        for l, lane in enumerate(self.lanes):
            print_s(f"  lane {l}: {lane.z_min} <= z <= {lane.z_max}")
            print_s(f"  lane {l}: center at z = {lane.z_center}")
            track_0 = wheel_tracks[l * 2]
            track_1 = wheel_tracks[l * 2 + 1]
            print_s(f"  lane {l}: wheel tracks at z = {track_0}, {track_1}")

        if self.single_sections:
            print_s(
                f"Single section per deck and pier:"
                + f"\ndeck = {self.sections[0]}"
                + f"\npier = {self.supports[0].sections[0]}"
            )

        if pier_fix_info:
            for p, pier in enumerate(self.supports):
                print_s(
                    f"Pier {p} fixed:"
                    f"\n  x-trans {pier.fix_x_translation}"
                    f"\n  y-trans {pier.fix_y_translation}"
                    f"\n  z-trans {pier.fix_z_translation}"
                    f"\n  x-rot   {pier.fix_x_rotation}"
                    f"\n  y-rot   {pier.fix_y_rotation}"
                    f"\n  z-rot   {pier.fix_z_rotation}"
                )

    def id_str(self, acc: bool = True):
        """Name with dimensions attached.

        Args:
            acc: bool, whether to include (True) or ignore bridge accuracy.

        """
        acc_str = f"-{self.accuracy}" if acc else ""
        return safe_str(f"{self.name}{acc_str}-{self.dimensions.name()}")

    def wheel_tracks(self, c: "Config"):
        """Z positions of wheel track on the bridge."""
        half_axle = c.axle_width / 2
        return list(
            chain.from_iterable(
                [lane.z_center - half_axle, lane.z_center + half_axle]
                for lane in self.lanes
            )
        )

    def y_min_max(self):
        """The min and max values in y direction from supports and sections."""
        return self._min_max(lambda s: s.y_min_max())

    def z_min_max(self):
        """The min and max values in z direction from supports and sections."""
        return self._min_max(lambda s: s.z_min_max())

    def x_axis(self) -> List[float]:
        """Position of supports in meters along the bridge's x-axis."""
        return np.interp([f.x_frac for f in self.supports], [0, 1], [0, self.length])

    def x_axis_equi(self, n) -> List[float]:
        """n equidistant values along the bridge's x-axis, in meters."""
        return np.interp(np.linspace(0, 1, n), [0, 1], [0, self.length])

    def x_frac(self, x: float):
        return float(
            interp1d([self.x_min, self.x_max], [0, 1], fill_value="extrapolate")(x)
        )

    def x(self, x_frac: float):
        return float(
            interp1d([0, 1], [self.x_min, self.x_max], fill_value="extrapolate")(x_frac)
        )

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
        f: Callable[[Union[Support, Section]], Tuple[Optional[float], Optional[float]]],
    ) -> Tuple[float, float]:
        """The min and max values in a direction from supports and sections."""
        z_min, z_max = None, None

        def set_z_min(z: float):
            nonlocal z_min
            if z is None:
                return
            z_min = z if z_min is None or z < z_min else z_min

        def set_z_max(z: float):
            nonlocal z_max
            if z is None:
                return
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
        # Single section only in 3D.
        if self.single_sections:
            if self.dimensions != Dimensions.D3:
                raise ValueError("Bridge.single_section only supported in 3D")
            assert self.single_sections[0].start_x_frac == 0
            assert self.single_sections[0].start_z_frac == 0
            assert self.single_sections[1].start_x_frac == 0
            assert self.single_sections[1].start_z_frac == 0
            assert self.single_sections[1].start_frac_len == 0
            assert len(self.sections) == 1
            for pier in self.supports:
                assert len(pier.sections) == 1

        # Bridge boundaries should be correct in orientation.
        assert self.x_min < self.x_max
        assert self.y_min < self.y_max
        assert self.z_min < self.z_max

        # Derived dimensions should make sense.
        assert self.length == self.x_max - self.x_min
        assert self.width == self.z_max - self.z_min

        # Base mesh must be of a minimum size.
        assert self.base_mesh_deck_max_x <= self.length
        if self.dimensions == Dimensions.D3:
            assert self.base_mesh_deck_max_z <= self.width
            for pier in self.supports:
                # TODO: Improve this assert, piers are not vertical.
                assert self.base_mesh_pier_max_y <= pier.height

        # Delegate to 2D/3D specific checks.
        if self.dimensions == Dimensions.D2:
            self._assert_2d()
        else:
            self._assert_3d()

    def _assert_2d(self):
        # All supports are Fix.
        for support in self.supports:
            if not isinstance(support, Fix):
                raise ValueError("2D bridge must use Fix supports")

        # All sections are Section2D.
        for section in self.sections:
            if not isinstance(section, Section2D):
                raise ValueError("2D bridge must use Section2D sections")

        # First node must be fixed in x direction.
        if self.supports and not self.supports[0].x:
            # TODO: Remove first check in line above.
            # TODO: Check self.supports[0].x_frac == 0.
            raise ValueError("2D bridge must have node at x=0 fixed in x direction")

        # 2D bridge has exactly 1 section.
        if len(self.sections) != 1:
            raise ValueError("2D bridge must have exactly 1 section")

    def _assert_3d(self):
        # All supports are Support3D.
        for support in self.supports:
            if not isinstance(support, Support3D):
                raise ValueError("3D bridge must use Support3D supports")

        # All sections are Section3D.
        for section in self.sections:
            if not isinstance(section, Section3D):
                raise ValueError("3D bridge must use Section3D sections")

        # First section must start at 0.
        if self.sections[0].start_x_frac != 0:
            raise ValueError("First section of 3D bridge must start at 0")

        # Section must be in order.
        last_start_x_frac = self.sections[0].start_x_frac
        for section in self.sections[1:]:
            if section.start_x_frac < last_start_x_frac:
                raise ValueError("Sections not in order of start_x_frac")
            last_start_x_frac = section.start_x_frac

        # Lanes must be in range.
        for i, lane in enumerate(self.lanes):
            if lane.z_min < self.z_min:
                raise ValueError(
                    f"Lane {i} lower position {lane.z_min} less than bridge"
                    + f" {self.z_min}"
                )
            if lane.z_min > self.z_max:
                raise ValueError(
                    f"Lane {i} lower position {lane.z_min} greater than bridge"
                    + f" {self.z_max}"
                )
            if lane.z_max < self.z_min:
                raise ValueError(
                    f"Lane {i} upper position {lane.z_max} less than bridge"
                    + f" {self.z_min}"
                )
            if lane.z_max > self.z_max:
                raise ValueError(
                    f"Lane {i} upper position {lane.z_max} greater than bridge"
                    + f" {self.z_max}"
                )

        # Supports must be in range.
        for i, support in enumerate(self.supports):
            support_z_min, support_z_max = support.z_min_max_top()
            if support_z_min < self.z_min:
                raise ValueError(
                    f"Support {i} lower position {support_z_min} less than"
                    + f" bridge {self.z_min}"
                )
            if support_z_min > self.z_max:
                raise ValueError(
                    f"Support {i} lower position {support_z_min} greater than"
                    + f" bridge {self.z_max}"
                )
            if support_z_max < self.z_min:
                raise ValueError(
                    f"Support {i} upper position {support_z_max} less than"
                    + f" bridge {self.z_min}"
                )
            if support_z_max > self.z_max:
                raise ValueError(
                    f"Support {i} upper position {support_z_max} greater than"
                    + f" bridge {self.z_max}"
                )


def _reset_model_ids():
    """Gets called for you when constructing a Config."""
    global _fiber_cmd_id
    _fiber_cmd_id = 1
    Section2D.next_id = 1
    Section3D.next_id = 1
