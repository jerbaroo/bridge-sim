"""Classes for building bridges and running simulations."""

import os
from enum import Enum
from itertools import chain
from timeit import default_timer as timer
from typing import List, Union, Tuple, Optional, Callable

import numpy as np
from matplotlib import cm as cm, colors as colors, pyplot as plt
from scipy.interpolate import interp1d

from bridge_sim.util import (
    safe_str,
    round_m,
    flatten,
    print_i,
    print_w,
    print_s,
    get_dir,
)

DIST_DECIMALS = 6


class PierSettlement:
    def __init__(self, pier: int, settlement: float):
        """A vertical translation applied to a pier in simulation.

        Args:
            pier: index of a pier on a bridge.
            settlement: amount of pier settlement to apply.

        """
        self.pier = pier
        self.settlement = settlement

    def id_str(self):
        return safe_str(f"{np.around(self.settlement, 3)}-{self.pier}")


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """A point described by three positions: (X, Y, Z).

        Args:
            x: X position of the point.
            y: Y position of the point.
            z: Z position of the point.

        """
        self.x: float = np.around(x, DIST_DECIMALS)
        self.y: float = np.around(y, DIST_DECIMALS)
        self.z: float = np.around(z, DIST_DECIMALS)

    def distance(self, point: "Point"):
        """Distance from this Point to the given Point.

        Args:
            point: other Point to compute the distance to.

        """
        return np.around(
            np.sqrt(
                ((self.x - point.x) ** 2)
                + ((self.y - point.y) ** 2)
                + ((self.z - point.z) ** 2)
            ),
            DIST_DECIMALS,
        )

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class PointLoad:
    def __init__(self, x: float, z: float, load: float, units: Optional[str] = None):
        """A point load applied in simulation.

        Args:
            x: X position of the point-load.
            z: Z position of the point-load.
            load: intensity of the point-load.

        """
        self.x = x
        self.z = z
        self.load = load
        self.units = units

    def __repr__(self):
        """Human readable representation of this point-load."""
        return f"X = {self.x}, Z = {self.z}, load = {self.load}"

    def id_str(self):
        """String uniquely representing this point-load."""
        return safe_str(
            f"({np.around(self.x, DIST_DECIMALS)}, {np.around(self.z, DIST_DECIMALS)}, {np.around(self.load, DIST_DECIMALS)})"
        )

    def point(self) -> Point:
        """The 'Point' part of this point-load."""
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
        return self in [
            ResponseType.StressXXB,
            ResponseType.StressXXT,
            ResponseType.StressZZB,
        ]

    def is_strain(self):
        """Is this response type a strain type?"""
        return self in [
            ResponseType.StrainXXB,
            ResponseType.StrainXXT,
            ResponseType.StrainZZB,
        ]

    def ss_direction(self) -> str:
        """A stress or strain identifier e.g. XXB (if applicable)."""
        if self.is_stress() or self.is_strain():
            return self.name()[-3:]
        raise ValueError("Not stress or strain")

    def name(self) -> str:
        """Human readable name for this response type."""
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

    def to_stress(self):
        """The corresponding stress type for this strain type.

        Raises a ValueError if this is not a strain response type.

        """
        if self == ResponseType.StrainXXB:
            return ResponseType.StressXXB
        if self == ResponseType.StrainXXT:
            return ResponseType.StressXXT
        if self == ResponseType.StrainZZB:
            return ResponseType.StressZZB
        if self == ResponseType.StrainZZT:
            return ResponseType.StressZZT
        raise ValueError(f"Responses must be a strain type")


# Shorthand for ResponseType.
RT = ResponseType


class Config:
    def __init__(
        self,
        bridge: Callable[[], "Bridge"],
        sim_runner: "FEMRunner",
        vehicle_data_path: str,
        vehicle_pdf: List[Tuple[float, float]],
        vehicle_pdf_col: str,
        generated_data: str = "generated-data",
        shorten_paths: bool = False,
        il_num_loads: int = 600,
    ):
        """Simulation configuration object.

        Combines a Bridge and FEMRunner among other configuration.

        Args:
            bridge: function that returns a bridge.
            sim_runner: function that returns a simulation runner.
            vehicle_data_path: path of the vehicles CSV file.
            vehicle_pdf:
                percentage of vehicles below a maximum value for that column.

                Example: [(2.4, 0.5), (5.6, 94.5), (16, 5)]

                Here 5% of vehicles are 2.4m or less in length, 94.5% greater than
                2.4m and less than 5.6m, and the remaining 5% are less than 16m.
                This applies if 'vehicle_pdf_col' is "length".
            vehicle_pdf_col: column name of vehicle_data to group by.
            generated_data: path to directory where to save generated files.
            shorten_paths: shorten simulation paths (to avoid OS limits).

        """
        # Core.
        self._bridge = bridge
        self.bridge = self._bridge()
        self.sim_runner = sim_runner

        # OpenSees
        self.os_model_template_path: str = "model-template.tcl"
        self.os_3d_model_template_path: str = "model-template-3d.tcl"

        # Simulation performance.
        self.parallel = 1
        self.shorten_paths = shorten_paths
        self.resp_matrices = dict()

        # Unit loads.
        self.il_num_loads = il_num_loads
        self.il_unit_load: float = 1000000
        self.unit_pier_settlement: float = 1
        self.unit_axial_delta_temp_c: int = 1
        self.unit_moment_delta_temp_c: int = 1
        self.cte = 12e-6
        self.self_weight_asphalt: bool = True

        # Responses & events.
        self.sensor_freq: float = 1 / 100
        self.event_time_s: float = 2  # Seconds.

        # Vehicles.
        self.perturb_stddev: float = 0.1
        self.axle_width: float = 2.5
        self.vehicle_pdf = vehicle_pdf
        self.vehicle_pdf_col = vehicle_pdf_col
        start = timer()
        self.vehicle_data_path = vehicle_data_path
        # Necessary to prevent a circular import.
        from bridge_sim.vehicles.sample import load_vehicle_data

        self.vehicle_data = load_vehicle_data(vehicle_data_path)
        print_i(
            f"Loaded vehicles data from {vehicle_data_path} in"
            + f" {timer() - start:.2f}s"
        )

        # Ensure vehicles probability density sums to 1.
        pdf_sum = sum(map(lambda f: f[1], self.vehicle_pdf))
        if int(pdf_sum) != 100:
            pre_pdf_sum = pdf_sum
            for i in range(len(self.vehicle_pdf)):
                self.vehicle_pdf[i] = (
                    self.vehicle_pdf[i][0],
                    self.vehicle_pdf[i][1] / pdf_sum,
                )
            pdf_sum = sum(map(lambda f: f[1], self.vehicle_pdf))
            print_w(f"Vehicle PDF sums to {pre_pdf_sum}, adjusted to sum to 1")

        # Root directories for generated data.
        self._root_generated_data_dir = generated_data
        self.root_generated_data_dir = lambda: get_dir(self._root_generated_data_dir)
        if self._root_generated_data_dir[-1] in "/\\":
            raise ValueError("generated_data must not end in path separator")
        self.root_generated_images_dir = lambda: get_dir(
            os.path.join(self.root_generated_data_dir() + "-images")
        )

    # Bridge-specific directories for generated data.

    def generated_data_dir(self):
        """Path to directory where data is saved."""
        return get_dir(
            os.path.join(self.root_generated_data_dir(), self.bridge.id_str(),)
        )

    def generated_images_dir(self):
        """Path to directory where images are saved."""
        return get_dir(
            os.path.join(self.root_generated_images_dir(), self.bridge.id_str(),)
        )

    # Bridge-specific but accuracy-independent directories.

    def generated_data_dir_no_acc(self):
        """Like 'generated_data_dir' but doesn't use 'Bridge.msl' or 'Bridge.data_id'."""
        return get_dir(
            os.path.join(
                self.root_generated_data_dir(),
                self.bridge.id_str(msl=False, data_id=False),
            )
        )

    def generated_images_dir_no_acc(self):
        """Like 'generated_images_dir' but doesn't use 'Bridge.msl' or 'Bridge.data_id'."""
        return get_dir(
            os.path.join(
                self.root_generated_images_dir(),
                self.bridge.id_str(msl=False, data_id=False),
            )
        )

    def get_path_in(self, in_: str, dirname: str, filename: str):
        """Filepath in a directory in a directory (created if necessary).

        TODO: Use safe_str here.

        """
        dirpath = os.path.join(in_, dirname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return os.path.join(dirpath, filename)

    def get_data_path(
        self, dirname: str, filename: str, bridge: bool = True, acc: bool = True
    ):
        """Get a bridge-specific image path in a named directory."""
        dir_path = self.generated_data_dir()
        if not bridge:
            dir_path = self.root_generated_images_dir()
        elif not acc:
            dir_path = self.generated_data_dir_no_acc()
        return self.get_path_in(dir_path, dirname, filename)

    def get_image_path(
        self, dirname: str, filename: str, bridge: bool = True, acc: bool = True
    ):
        """Get a bridge-specific image path in a named directory."""
        dir_path = self.generated_images_dir()
        if not bridge:
            dir_path = self.root_generated_images_dir()
        elif not acc:
            dir_path = self.generated_images_dir_no_acc()
        return self.get_path_in(dir_path, dirname, filename)


class Dimensions(Enum):
    D3 = "D3"

    def name(self) -> str:
        """Human readable name for dimensions."""
        return {Dimensions.D3: "3D",}[self]


class Support:
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
        x: X position of center of the support in meters.
        z: Z position of center of the support in meters.
        length: length of the support in meters.
        height: height of the support in meters.
        width_top: width of the top of the support in meters.
        width_bottom: width of the bottom of the support in meters.
        materials: deck materials, either a list or function from X position.

    """

    def __init__(
        self,
        x: float,
        z: float,
        length: float,
        height: float,
        width_top: float,
        width_bottom: float,
        materials: Union[List["MaterialSupport"], Callable[[float], "MaterialSupport"]],
        fix_x_translation: bool,
        fix_z_translation: bool,
        fix_y_translation: bool = True,
        fix_x_rotation: bool = False,
        fix_z_rotation: bool = False,
        fix_y_rotation: bool = False,
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
        self._sections = materials
        # Must be callable or a list.
        if not callable(self._sections):
            assert isinstance(self._sections, list)
            assert all(isinstance(s, MaterialSupport) for s in self._sections)
        if self.width_top < self.width_bottom:
            raise ValueError("Support: top width must be >= bottom width")

    def x_min_max_top(self) -> Tuple[float, float]:
        """The min and max x positions for the top of this pier."""
        half_length = self.length / 2
        return round_m(self.x - half_length), round_m(self.x + half_length)

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max y positions for this pier."""
        return round_m(-self.height), 0

    def z_min_max_top(self) -> Tuple[float, float]:
        """The min and max z positions for the top of this pier."""
        half_top = self.width_top / 2
        return round_m(self.z - half_top), round_m(self.z + half_top)

    def z_min_max_bottom(self) -> Tuple[float, float]:
        """The min and max z positions for the bottom of this pier."""
        half_bottom = self.width_bottom / 2
        return round_m(self.z - half_bottom), round_m(self.z + half_bottom)


class Asphalt:
    def __init__(self, thickness: float, density: float):
        """Asphalt on a lane of a bridge."""
        self.thickness = thickness
        self.density = density


class Lane:
    """A traffic lane spanning the length of a bridge.

    Args:
        z0: Z position of one edge of the lane.
        z1: Z position of the other edge of the lane.
        ltr: traffic moves in left to right direction?
        asphalt: thickness and density of the asphalt.

    Attrs:
        z_min, lower Z position of the bridge.
        z_max, greater Z position of the bridge.
        width, width of the lane.

    """

    def __init__(
        self,
        z0: float,
        z1: float,
        ltr: bool,
        asphalt: Optional[Asphalt] = Asphalt(thickness=0.1, density=2.4),
    ):
        self.z_min: float = round_m(min(z0, z1))
        self.z_max: float = round_m(max(z0, z1))
        self.ltr: bool = ltr
        self.width = round_m(self.z_max - self.z_min)
        self.z_center = round_m(self.z_min + (self.width / 2))
        self.asphalt = asphalt

    def wheel_track_zs(self, config: Config):
        """Z positions of this lane's wheel track on a bridge."""
        half_axle = config.axle_width / 2
        return [self.z_center - half_axle, self.z_center + half_axle]


class Material:
    """An abstract class for material properties.

    Args:
        density: density of the material.
        thickness: thickness of the material.
        youngs: Young's modulus of the material.
        youngs_x: Young's modulus in x direction.
        poissons: Poisson's ratio of the material.
        start_x_frac: start of the material as a fraction of X position.
        start_z_frac: start of the material as a fraction of Z position.
        end_x_frac: end of the section as a fraction of X position.
        end_z_frac: end of the section as a fraction of Z position.

    """

    def __init__(
        self,
        thickness: float,
        youngs: float,
        poissons: float,
        start_x_frac: float = 0,
        start_z_frac: float = 0,
        end_x_frac: float = 1,
        end_z_frac: float = 1,
        density: float = 0,
        youngs_x: Optional[float] = None,
    ):
        self.density = density
        self.thickness = thickness
        self.youngs = youngs
        self._youngs_x = youngs_x
        self.poissons = poissons
        self.start_x_frac = start_x_frac
        self.start_z_frac = start_z_frac
        self.end_x_frac = end_x_frac
        self.end_z_frac = end_z_frac

    def youngs_x(self):
        if self._youngs_x is not None:
            return self._youngs_x
        return self.youngs

    def contains(self, bridge: "Bridge", x: float, z: float) -> bool:
        """Does this material contain the given point?"""
        x_frac, z_frac = bridge.x_frac(x), bridge.z_frac(z)
        return (
            (self.start_x_frac < x_frac or np.isclose(self.start_x_frac, x_frac))
            and (self.end_x_frac > x_frac or np.isclose(self.end_x_frac, x_frac))
            and (self.start_z_frac < z_frac or np.isclose(self.start_z_frac, z_frac))
            and (self.end_z_frac > z_frac or np.isclose(self.end_z_frac, z_frac))
        )

    def mat_id_str(self):
        """Representation of this section by material properties."""
        return f"{self.density}-{self.thickness}-{self.youngs}-{self.poissons}"

    def y_min_max(self) -> Tuple[float, float]:
        """The min and max values in y for this section."""
        return -self.thickness, 0

    def prop_str(self):
        """Textual representation of material properties."""
        return (
            "Material"
            + f"\n  starts at (x_frac, z_frac) ="
            + f" ({round_m(self.start_x_frac)}, {round_m(self.start_z_frac)})"
            + f"\n  ends at (x_frac, z_frac) ="
            + f" ({round_m(self.end_x_frac)}, {round_m(self.end_z_frac)})"
            + f"\n  density = {self.density} kg/m"
            + f"\n  thickness = {self.thickness} m"
            + f"\n  youngs = {self.youngs} MPa"
            + f"\n  poissons = {self.poissons}"
        )


MaterialDeck = Material


class MaterialSupport(Material):
    """Like Material but intended for describing piers.

    Args:
        density: density of the material.
        thickness: thickness of the material.
        youngs: Young's modulus of the material.
        poissons: Poisson's ratio of the material.
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

    def prop_str(self):
        """Textual representation of material properties."""
        return (
            "Material"
            + f"\n  starts at {round_m(self.start_frac_len)}"
            + f"\n  density = {self.density} kg/m"
            + f"\n  thickness = {self.thickness} m"
            + f"\n  youngs = {self.youngs} MPa"
            + f"\n  poissons = {self.poissons}"
        )


class Bridge:
    def __init__(
        self,
        name: str,
        length: float,
        width: float,
        supports: List[Support],
        materials: List["MaterialDeck"],
        lanes: List[Lane],
        msl: float,
        data_id: str = "healthy",
        single_sections: Optional[Tuple[Material, Material]] = None,
    ):
        """A bridge's geometry, material properties and boundary conditions.

        Args:
            name: name of this bridge.
            length: length of this bridge.
            width: width of this bridge.
            supports: a list of Support.
            materials: a list of bridge deck Material.
            lanes: a list of Lane for traffic to drive on.
            msl: maximum shell length.
            data_id: additional identifier for saving/loading data.
            single_sections: tuple of one deck and one material for supports.

        """
        # Given arguments.
        self.name = name
        self.msl = float(msl)
        self.data_id = data_id

        self.length = length
        self.width = width
        self.supports = supports
        self.sections = materials
        self.lanes = lanes
        self.dimensions = Dimensions.D3
        self.ref_temp_c = 17
        self._next_section_id = 1

        # Mesh.
        self.base_mesh_deck_max_x = msl
        self.base_mesh_deck_max_z = msl
        self.base_mesh_pier_max_long = msl

        # Attach single section option for asserts and printing info.
        self.single_sections = single_sections
        if self.single_sections is not None:
            self.name += "-single-sections"
            self.sections = [self.single_sections[0]]  # Set deck section.
            for pier in self.supports:  # Set pier sections.
                pier.sections = [self.single_sections[1]]

        self.additional_xs = []

        # Derived attributes.
        #
        # NOTE: The functions y_min_max and z_min_max calculate the min and max
        # values of the bridge in y and z directions respectively, based on the
        # supports and sections. For a 3D bridge neither supports nor sections
        # contain information on the min or max values in z direction.
        self.x_min, self.x_max = 0, length
        self.y_min, self.y_max = self.y_min_max()
        self.z_min, self.z_max = -width / 2, width / 2
        self.x_center = (self.x_min + self.x_max) / 2
        self.y_center = (self.y_min + self.y_max) / 2
        self.z_center = (self.z_min + self.z_max) / 2
        self.height = self.y_max - self.y_min
        # All sections belonging to this bridge.
        self._sections_dict = dict()
        # Assert the bridge is fine and print info.
        self._assert_bridge()

    def _get_section(self, section: Material) -> Material:
        """An equivalent section if exists, else the given one."""

        def with_id(s: Material) -> Material:
            s.id = self._next_section_id
            self._next_section_id += 1
            return s

        section_prop_str = section.prop_str()
        if section_prop_str in self._sections_dict:
            return with_id(self._sections_dict[section_prop_str])
        self._sections_dict[section_prop_str] = section
        return with_id(self._sections_dict[section_prop_str])

    def deck_section_at(self, x: float, z: float) -> Material:
        """Return the deck section at given position."""
        if callable(self.sections):
            raise NotImplementedError()
        if len(self.sections) == 1:
            return self._get_section(self.sections[0])
        for section in self.sections:
            if section.contains(bridge=self, x=x, z=z):
                return self._get_section(section)
        raise ValueError(f"No section for x, z = {x}, {z}")

    def pier_section_at_len(self, p_i: int, section_frac_len: float) -> Material:
        """Return the section at a fraction of a pier's length"""
        assert 0 <= section_frac_len <= 1
        pier = self.supports[p_i]
        if callable(pier._sections):
            return self._get_section(pier._sections(section_frac_len))
        if len(pier._sections) == 1:
            return self._get_section(pier._sections[0])
        raise ValueError(f"Pier {p_i} sections are not a function")

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
            print_s("One section for the deck, one for piers:")
            print_s(f"Deck:")
            list(map(print_s, str(self.sections[0]).split("\n")))
            print_s(f"Piers:")
            list(map(print_s, str(self.supports[0].sections[0]).split("\n")))

        if pier_fix_info:
            for p, pier in enumerate(self.supports):
                print_s(f"Pier {p} fixed:")
                print_s(f"  x-trans {pier.fix_x_translation}")
                print_s(f"  y-trans {pier.fix_y_translation}")
                print_s(f"  z-trans {pier.fix_z_translation}")
                print_s(f"  x-rot   {pier.fix_x_rotation}")
                print_s(f"  y-rot   {pier.fix_y_rotation}")
                print_s(f"  z-rot   {pier.fix_z_rotation}")

    def id_str(self, msl: bool = True, data_id: bool = True):
        """Name with accuracy information.

        Args:
            msl: bool, include msl in identifier.
            data_id: bool, include data_id in identifier.

        """
        acc_str = f"-{self.msl}" if msl else ""
        data_id_str = f"-{self.data_id}" if data_id else ""
        return safe_str(f"{self.name}{acc_str}{data_id_str}")

    def closest_lane(self, z: float):
        """Index of the lane closest to the point."""
        result = None
        lane_dist = np.inf
        for lane_ind, lane in enumerate(self.lanes):
            this_dist = abs(lane.z_center - z)
            if this_dist < lane_dist:
                result = lane_ind
                lane_dist = this_dist
        return result

    def axle_track_zs(self):
        """Z positions of axle track-centers on the bridge."""
        return sorted(lane.z_center for lane in self.lanes)

    def wheel_track_zs(self, c: "Config"):
        """Z positions of wheel track on the bridge."""
        return sorted(
            chain.from_iterable(lane.wheel_track_zs(c) for lane in self.lanes)
        )

    def wheel_track_xs(self, c: "Config"):
        """Unit load x positions for wheel tracks on this bridge."""
        return round_m(np.linspace(c.bridge.x_min, c.bridge.x_max, c.il_num_loads))

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
        f: Callable[
            [Union[Support, Material]], Tuple[Optional[float], Optional[float]]
        ],
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
            # for pier in self.supports:
            # TODO: Improve this assert, piers are not vertical.
            # assert self.base_mesh_pier_max_long <= pier.height
        self._assert_3d()

    def _assert_3d(self):
        # All sections are Material.
        for section in self.sections:
            if not isinstance(section, Material):
                raise ValueError("3D bridge must use Material sections")

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


class Vehicle:
    def __init__(
        self,
        load: Union[float, List[float]],
        axle_distances: List[float],
        axle_width: float,
        kmph: float,
        lane: int = 0,
        init_x: float = 0,
    ):
        """A vehicles, load intensities, position and speed.

        Args:
            load: either a scalar (total load of this vehicle), or a list (load
                per axle).
            axle_distances: distance between axles in meters.
            axle_width: width of the vehicles's axles in meters.
            kmph: speed of this vehicle.
            lane: index of a lane on a bridge.
            init_x: distance from lane beginning at time 0.

        """
        self.load = load
        self.axle_distances = axle_distances
        self.axle_width = axle_width
        self.length = sum(self.axle_distances)
        self.num_axles = len(self.axle_distances) + 1
        self.num_wheels = self.num_axles * 2
        self.kmph = kmph
        self.mps = self.kmph / 3.6  # Meters per second.
        self.lane = lane
        self.init_x = init_x
        if self.init_x >= 1:
            raise ValueError("Already left bridge at time t = 0")
        if self._is_load_per_axle() and not len(self.load) == self.num_axles:
            raise ValueError("Number of loads and axle distances don't match")

    def _is_load_per_axle(self) -> bool:
        """Is there a load per axle, or a total load?"""
        return isinstance(self.load, list)

    def total_load(self) -> float:
        """Total load of this vehicle."""
        if self._is_load_per_axle():
            return sum(self.load)
        return self.load

    def load_per_axle(self) -> List[float]:
        """Load for each axle."""
        if self._is_load_per_axle():
            return self.load
        result = [(self.load / self.num_axles) for _ in range(self.num_axles)]
        print(result[0])
        assert isinstance(result[0], float)
        return result

    def _cmap_norm(self, all_vehicles: List["Vehicle"], cmap, cmin=0, cmax=1):
        """A colormap and norm for coloring vehicles.

        Args:
            all_vehicles: to compute the maximum and minimum of all vehicles.
            cmap: Matplotlib colormap for the colours to use.
            cmin: the minimum colour value.
            cmax: the maximum colour value.

        Returns: a tuple of Matplotlib colormap and norm.

        """
        from bridge_sim.plot.util import truncate_colormap

        cmap = truncate_colormap(cmap, cmin, cmax)
        total_kns = [v.total_load() for v in all_vehicles] + [self.total_load()]
        norm = colors.Normalize(vmin=min(total_kns), vmax=max(total_kns))
        return cmap, norm

    def color(
        self, all_vehicles: List["Vehicle"] = [], cmap=cm.get_cmap("YlGn")
    ) -> float:
        """Colour of this vehicle, compared to other vehicles if given."""
        cmap, norm = self._cmap_norm(all_vehicles, cmap=cmap)
        if len(all_vehicles) == 0:
            return cmap(0.5)
        return cmap(norm(self.total_load()))

    def wheel_tracks_zs(self, config: Config) -> Tuple[float, float]:
        """Positions of the vehicles's wheels in Z direction."""
        return config.bridge.lanes[self.lane].wheel_track_zs(config)

    def xs_at(self, times: List[float], bridge: Bridge) -> List[List[float]]:
        """X position on bridge for each axle in meters at given times.

        Args:
            times: times when to compute positions.
            bridge: the bridge on which the vehicle moves.

        Returns: a NumPy array of shape len(times) x self.num_axles.

        """
        # Initial positions of axles.
        lane = bridge.lanes[self.lane]
        xs = [bridge.x_min if lane.ltr else bridge.x_max]
        xs[0] += self.init_x if lane.ltr else (-self.init_x)
        for ad in self.axle_distances:
            xs.append(xs[-1] - ad if lane.ltr else xs[-1] + ad)
        # Difference at each point in time.
        deltas = np.array(times) * self.mps
        if not lane.ltr:  # If right to left, decreasing X position.
            deltas *= -1
        assert len(deltas.shape) == 1
        assert len(deltas) == len(times)
        # Make result.
        result = np.ndarray((len(times), self.num_axles))
        assert len(result.shape) == 2
        for t, d in enumerate(deltas):
            result[t] = xs + d
        return result

    def x_at(self, time: float, bridge: Bridge) -> float:
        """X position of front axle on bridge at a time, in meters."""
        return self.xs_at(times=[time], bridge=bridge)[0][0]

    def on_bridge(self, time: float, bridge: Bridge) -> bool:
        """Is the vehicle on a bridge at a given time?"""
        xs = sorted(self.xs_at(times=[time], bridge=bridge)[0])
        x_min, x_max = xs[0], xs[-1]
        assert x_min < x_max
        return (bridge.x_min <= x_min <= bridge.x_max) or (
            bridge.x_min <= x_max <= bridge.x_max
        )

    def passed_bridge(self, time: float, bridge: Bridge) -> bool:
        """Has the current vehicle travelled over a bridge?"""
        rear_x = self.xs_at(times=[time], bridge=bridge)[0][-1]
        lane = bridge.lanes[self.lane]
        return rear_x > bridge.x_max if lane.ltr else rear_x < bridge.x_min

    def time_at(self, x: float, bridge: Bridge) -> float:
        """Time when the front axle is at an X position."""
        if bridge.lanes[self.lane].ltr:
            return (x - bridge.x_min - self.init_x) / self.mps
        return ((-x) + bridge.x_max - self.init_x) / self.mps

    def time_entering_bridge(self, bridge: Bridge) -> float:
        """Time the front axle is at lane beginning."""
        if bridge.lanes[self.lane].ltr:
            return self.time_at(x=bridge.x_min, bridge=bridge)
        return self.time_at(x=bridge.x_max, bridge=bridge)

    def time_entered_bridge(self, bridge: Bridge) -> float:
        """Time the rear axle is at lane beginning."""
        if bridge.lanes[self.lane].ltr:
            return self.time_at(x=bridge.x_min + self.length, bridge=bridge)
        return self.time_at(x=bridge.x_max - self.length, bridge=bridge)

    def time_leaving_bridge(self, bridge: Bridge) -> float:
        """Time the front axle is at lane end."""
        if bridge.lanes[self.lane].ltr:
            return self.time_at(x=bridge.x_max, bridge=bridge)
        return self.time_at(x=bridge.x_min, bridge=bridge)

    def time_left_bridge(self, bridge: Bridge) -> float:
        """Time the rear axle is at lane end."""
        if bridge.lanes[self.lane].ltr:
            return self.time_at(x=bridge.x_max + self.length, bridge=bridge)
        return self.time_at(x=bridge.x_min - self.length, bridge=bridge)

    def _axle_track_weights(self, axle_x: float, wheel_track_xs: List[float]):
        """Indices and weights for some X position.

        NOTE: Before using this function you should check if wheel_x is an X
        position on the bridge.

        """
        unit_load_x_ind = np.searchsorted(wheel_track_xs, axle_x)
        unit_load_x = lambda: wheel_track_xs[unit_load_x_ind]
        # If greater then subtract one index.
        if unit_load_x() > axle_x:
            unit_load_x_ind -= 1
        assert unit_load_x() <= axle_x
        # If the unit load is an exact match just return it..
        if np.isclose(axle_x, unit_load_x()):
            return (unit_load_x_ind, 1), (None, 0)
        # ..otherwise, return a combination of two unit loads. In this case the
        # unit load's position is less than the wheel.
        unit_load_x_lo = unit_load_x()
        unit_load_x_hi = wheel_track_xs[unit_load_x_ind + 1]
        assert unit_load_x_hi > axle_x
        dist_lo = abs(unit_load_x_lo - axle_x)
        dist_hi = abs(unit_load_x_hi - axle_x)
        dist = dist_lo + dist_hi
        return (unit_load_x_ind, dist_hi / dist), (unit_load_x_ind + 1, dist_lo / dist)

    def _axle_track_indices(
        self, config: Config, times: List[float]
    ) -> List[List[Tuple[int, float]]]:
        """Axle track indices and load intensities over time.

        NOTE: Each index is in [0, uls * lanes - 1].

        """
        try:
            self.load[0][0]
            raise ValueError("Load per wheel not supported!")
        except:
            pass
        xs = self.xs_at(times=times, bridge=config.bridge)  # Times x X axles.
        wheel_track_xs = config.bridge.wheel_track_xs(config)
        lane_offset = self.lane * config.il_num_loads
        for t, time in enumerate(times):
            result = []
            for x, kn in zip(xs[t], self.load_per_axle()):
                if config.bridge.x_min <= x <= config.bridge.x_max:
                    (lo, weight_lo), (hi, weight_hi) = self._axle_track_weights(
                        axle_x=x, wheel_track_xs=wheel_track_xs,
                    )
                    result.append(
                        (
                            (lo + lane_offset, weight_lo * kn),
                            (None if hi is None else hi + lane_offset, weight_hi * kn),
                        )
                    )
            yield result

    def wheel_track_loads(
        self, config: Config, times: List[float],
    ) -> List[List[PointLoad]]:
        """Point loads "bucketed" onto axle tracks.

        Returns: a list of PointLoad at every time step.

        """
        from bridge_sim.sim.run import ulm_point_loads

        u_point_loads = ulm_point_loads(config)
        result = []
        # This loop has one item per axle!
        for loads in self._axle_track_indices(config=config, times=times):
            time_results = []
            for (lo, load_lo), (hi, load_hi) in loads:
                # These point loads will have unit loads!
                # The loads need to be overwritten with half axle loads!
                pl_lo0, pl_lo1 = u_point_loads[lo]
                pl_lo0.load = load_lo / 2
                pl_lo1.load = load_lo / 2
                time_results.append(pl_lo0)
                time_results.append(pl_lo1)
                if hi is not None:
                    pl_hi0, pl_hi1 = u_point_loads[hi]
                    pl_hi0.load = load_hi / 2
                    pl_hi1.load = load_hi / 2
                    time_results.append(pl_hi0)
                    time_results.append(pl_hi1)
            result.append(time_results)
        return result

    def point_load_pw(
        self, config: Config, time: float, list: bool = False,
    ) -> Union[List[Tuple[PointLoad, PointLoad]], List[PointLoad]]:
        """A tuple of point load per axle, one point load per wheel."""
        z0, z1 = self.wheel_tracks_zs(config=config)
        assert z0 < z1
        load_per_axle = self.load_per_axle()
        result = []
        # For each axle create two loads.
        for x_i, x in enumerate(self.xs_at(times=[time], bridge=config.bridge)[0]):
            if config.bridge.x_min <= x <= config.bridge.x_max:
                wheel_load = load_per_axle[x_i] / 2
                result.append(
                    (
                        PointLoad(x=x, z=z0, load=wheel_load),
                        PointLoad(x=x, z=z1, load=wheel_load),
                    )
                )
        if list:
            return flatten(result, PointLoad)
        return result

    def _times_on_bridge(
        self, config: Config, sorted_times: List[float]
    ) -> Tuple[List[float], List[float]]:
        """Of the given sorted times only those when on the bridge."""
        entering_time = self.time_entering_bridge(config.bridge)
        left_time = self.time_left_bridge(config.bridge)
        first_index = np.searchsorted(sorted_times, entering_time)
        if not self.on_bridge(time=sorted_times[first_index], bridge=config.bridge):
            return [], []
        last_index = np.searchsorted(sorted_times, left_time)
        if last_index == len(sorted_times) or not self.on_bridge(
            time=sorted_times[last_index], bridge=config.bridge
        ):
            last_index -= 1
        return (
            np.arange(first_index, last_index + 1),
            np.array(sorted_times)[first_index : last_index + 1],
        )

    def plot_wheels(self, c: Config, time: float, label=None, **kwargs):
        """Plot each wheel as a single black dot."""
        wheel_loads = self.point_load_pw(time=time, bridge=c.bridge, list=True)
        for i, load in enumerate(wheel_loads):
            plt.scatter(
                [load.x],
                [load.z],
                facecolors="none",
                edgecolors="black",
                label=None if i > 0 else label,
                **kwargs,
            )
