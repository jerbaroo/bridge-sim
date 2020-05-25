"""Bridge scenarios."""
from copy import deepcopy
from typing import Callable, List, NewType, Optional, Tuple

import numpy as np

from bridge_sim.model import Point, Config, Bridge, PierSettlement
from bridge_sim.scenarios import Scenario
from lib.fem.params import SimParams
from lib.fem.responses import SimResponses
from bridge_sim.util import round_m, safe_str


class Healthy(Scenario):
    def __init__(self):
        super().__init__(name="normal")


CrackArea = NewType("CrackArea", Tuple[float, float, float, float])


class Cracked(Scenario):
    """A cracked bridge, defined by an area of a bridge's deck to crack."""

    def __init__(
        self, name: str, crack_area: Callable[[Bridge], CrackArea],
    ):
        def mod_bridge(bridge: Bridge):
            bridge = bridge
            bridge.data_id = self.name
            self._crack_deck(bridge)
            c_x_start, c_z_start, c_x_end, c_z_end = list(
                map(round_m, self.crack_area(bridge))
            )
            # Three meters below.
            lowest = max(bridge.x_min, c_x_start - 3)
            highest = min(bridge.x_max, c_x_end + 3)
            # Half a meter below.
            lower = max(bridge.x_min, c_x_start - 0.5)
            # 10 cm below.
            lowerer = max(bridge.x_min, c_x_start - 0.1)
            # print()
            # print(f"lowest, highest, lower, lowerer, c_x_start, c_x_end = {lowest, highest, lower, lowerer, c_x_start, c_x_end}")
            bridge.additional_xs = sorted(
                set(
                    map(
                        round_m,
                        np.concatenate(
                            (
                                np.arange(lowest, c_x_start + 0.01, 0.1),
                                np.arange(c_x_end, highest + 0.01, 0.1),
                                # np.arange(lowest, lower + 0.01, 0.1),
                                # np.arange(lower, lowerer + 0.01, 0.05),
                                # np.arange(lowerer, c_x_start + 0.01, 0.01),
                            )
                        ),
                    )
                )
            )
            # print("bridge.additional_xs")
            # print(bridge.additional_xs)
            # exit()
            # bridge.additional_xs = sorted(map(round_m, np.arange(lowest, highest, 0.05)))
            # print(bridge.additional_xs)
            # print(len(bridge.additional_xs))
            return bridge

        super().__init__(name=name, mod_bridge=mod_bridge)
        self.crack_area = crack_area

    def _crack_deck(self, bridge: Bridge):
        """Adds cracked sections to the given bridge's deck."""
        c_x_start, c_z_start, c_x_end, c_z_end = list(
            map(round_m, self.crack_area(bridge))
        )
        # print(f"crack x: (start, end) = ({c_x_start}, {c_x_end})")
        # print(f"crack z: (start, end) = ({c_z_start}, {c_z_end})")

        if callable(bridge.sections):
            raise NotImplementedError()

        # Find where the cracked area and current sections overlap.
        overlaps: List[Tuple[Section3D, float, float, float, float]] = []
        for section in bridge.sections:
            s_x_start = round_m(bridge.x(section.start_x_frac))
            s_z_start = round_m(bridge.z(section.start_z_frac))
            s_x_end = round_m(bridge.x(section.end_x_frac))
            s_z_end = round_m(bridge.z(section.end_z_frac))

            # print()
            # print(f"section x: (start, end) = ({s_x_start}, {s_x_end})")
            # print(f"section z: (start, end) = ({s_z_start}, {s_z_end})")

            overlap_x_start = max(c_x_start, s_x_start)
            overlap_z_start = max(c_z_start, s_z_start)
            overlap_x_end = min(c_x_end, s_x_end)
            overlap_z_end = min(c_z_end, s_z_end)

            # print(f"overlap x (start, end) = ({overlap_x_start}, {overlap_x_end})")
            # print(f"overlap z (start, end) = ({overlap_z_start}, {overlap_z_end})")

            overlap_x = overlap_x_end - overlap_x_start
            overlap_z = overlap_z_end - overlap_z_start

            # print(f"overlap x = {overlap_x}")
            # print(f"overlap z = {overlap_z}")

            if overlap_x > 0 and overlap_z > 0:
                overlaps.append(
                    (
                        section,
                        overlap_x_start,
                        overlap_z_start,
                        overlap_x_end,
                        overlap_z_end,
                    )
                )

        # Create new cracked sections for each of these overlaps.
        cracked_sections, max_id = [], 1000000
        for i, (section, x_start, z_start, x_end, z_end) in enumerate(overlaps):
            # print(f"x (start, end) = ({x_start}, {x_end})")
            # print(f"z (start, end) = ({z_start}, {z_end})")
            cracked_section = deepcopy(section)
            cracked_section.id = max_id + i + 1
            y_x = cracked_section.youngs_x()
            cracked_section.youngs_x = lambda: 0.5 * y_x
            cracked_section.start_x_frac = bridge.x_frac(x_start)
            cracked_section.start_z_frac = bridge.z_frac(z_start)
            cracked_section.end_x_frac = bridge.x_frac(x_end)
            cracked_section.end_z_frac = bridge.z_frac(z_end)
            cracked_sections.append(cracked_section)

        bridge.sections = cracked_sections + bridge.sections

    def without(self, bridge: Bridge, thresh: float = 0):
        """Return a function to reject non crack area points."""
        c_x_start, c_z_start, c_x_end, c_z_end = list(
            map(round_m, self.crack_area(bridge))
        )
        if thresh != 0:
            c_x_start -= thresh
            c_z_start -= thresh
            c_x_end += thresh
            c_z_end += thresh

        def reject(point: Point) -> Point:
            if point.x < c_x_start:
                return True
            if point.x > c_x_end:
                return True
            if point.z < c_z_start:
                return True
            if point.z > c_z_end:
                return True
            return False

        return reject


def transverse_crack(
    length: float = 0.5,
    width: Optional[float] = None,
    at_x: Optional[float] = None,
    at_z: Optional[float] = None,
) -> Cracked:
    """A bridge with a transverse crack."""

    def crack_area(bridge: Bridge) -> CrackArea:
        nonlocal width
        nonlocal at_x
        nonlocal at_z
        if width is None:
            width = bridge.width / 2
        if at_x is None:
            at_x = bridge.x_min + (bridge.length / 2)
        if at_z is None:
            at_z = bridge.z_min
        return at_x, at_z, at_x + length, at_z + width

    return Cracked(
        name=safe_str(f"transverse-{length}-{width}-{at_x}-{at_z}"),
        crack_area=crack_area,
    )


class PierDisp(Scenario):
    def __init__(self, pier_disps: [PierSettlement], name_prefix: str = ""):
        if len(pier_disps) < 1:
            raise ValueError("At least 1 PierDisp required")
        name = name_prefix + "-".join(list(map(lambda pd: pd.id_str(), pier_disps)))
        self.pier_disps = pier_disps

        def mod_sim_params(sim_params: SimParams):
            if len(self.pier_disps) > 1:
                raise ValueError("Cannot have SimParams with > 1 pier settlement")
            sim_params.displacement_ctrl = self.pier_disps[0]
            return sim_params

        super().__init__(name=name, mod_sim_params=mod_sim_params)


def pier_disp_damage(pier_disps: List[Tuple[int, float]]) -> PierDisp:
    """All piers with equal given displacement."""
    return PierDisp(
        pier_disps=[
            PierSettlement(pier=p_ind, displacement=displacement)
            for p_ind, displacement in pier_disps
        ],
    )


def equal_pier_disp(bridge: Bridge, displacement: float) -> PierDisp:
    """All piers with equal given displacement."""
    return PierDisp(
        pier_disps=[
            PierSettlement(displacement=displacement, pier=p)
            for p in range(len(bridge.supports))
        ],
        name_prefix="equal-piers",
    )


def longitudinal_pier_disp(bridge: Bridge, start: float, step: float) -> PierDisp:
    """Pier displacement that increases in longitudinal direction."""
    increase_every = len(set(pier.z for pier in bridge.supports))
    pier_disps = []
    displacement = start
    for p in range(len(bridge.supports)):
        if p != 0 and p % increase_every == 0:
            displacement += step
        pier_disps.append(PierSettlement(displacement=displacement, pier=p))
    return PierDisp(pier_disps=pier_disps, name_prefix="long-piers")


class Thermal(Scenario):
    """Thermal expansion, with axial and bending moment components."""

    def __init__(self, axial_delta_temp: float = 0, moment_delta_temp: float = 0):
        self.axial_delta_temp = axial_delta_temp
        self.moment_delta_temp = moment_delta_temp

        def mod_sim_params(sim_params: SimParams):
            sim_params.axial_delta_temp = self.axial_delta_temp
            sim_params.moment_delta_temp = self.moment_delta_temp
            return sim_params

        super().__init__(
            name=f"thermal-axial-{self.axial_delta_temp}-moment-{self.moment_delta_temp}",
            mod_sim_params=mod_sim_params,
        )

    def to_strain(self, c: Config, sim_responses: SimResponses):
        """Convert fem, adding free and restrained strain."""
        if sim_responses.response_type not in [
            ResponseType.Strain,
            ResponseType.StrainT,
            ResponseType.StrainZZB,
        ]:
            raise ValueError(
                f"Can only convert Strain not {sim_responses.response_type}"
            )
        if self.axial_delta_temp != 0 and self.moment_delta_temp != 0:
            raise ValueError("Must be only axial or moment loading")
        # Uniform temperature load.
        if self.axial_delta_temp != 0:
            sim_responses = sim_responses.map(
                lambda r: (r * 1e-6) - (1 * c.cte * c.unit_axial_delta_temp_c)
            )
        # Linear temperature load.
        elif self.moment_delta_temp != 0:
            sim_responses = sim_responses.map(
                lambda r: r * 1e-6 + (0.5 * c.cte * c.unit_moment_delta_temp_c)
            )
        else:
            raise ValueError("Don't know how to convert to strain")
        return sim_responses

    def to_stress(self, c: Config, sim_responses: SimResponses):
        sim_responses = self.to_strain(c=c, sim_responses=sim_responses)
        return sim_responses.to_stress(c.bridge)


def thermal_damage(
    axial_delta_temp: float = 0, moment_delta_temp: float = 0, mod_msl: float = 0.6
):
    """Like ThermalDamage, but also modifies the bridge's MSL parameter."""
    td = Thermal(axial_delta_temp=axial_delta_temp, moment_delta_temp=moment_delta_temp)
    og_mod_bridge = td.mod_bridge

    def mod_bridge(b: Bridge):
        b = og_mod_bridge(b)
        b.base_mesh_deck_max_x *= mod_msl
        b.base_mesh_deck_max_z *= mod_msl
        b.base_mesh_pier_max_long *= mod_msl
        return b

    td.mod_bridge = mod_bridge
    return td


def healthy_damage_w_transverse_crack_nodes(crack_f=transverse_crack):
    """Like 'HealthyDamage' but with additional nodes around near a non-existant
    crack zone. Such that both healthy and cracked bridges can have equal nodes.

    """

    healthy_damage = Healthy()
    crack_damage = crack_f()

    def mod_bridge(bridge: Bridge):
        # A copy of the bridge is modified under the cracking scenario.
        some_bridge = crack_damage.mod_bridge(deepcopy(bridge))
        # And the additional nodes are copied into the original given bridge.
        bridge.additional_xs = some_bridge.additional_xs
        return bridge

    healthy_damage.mod_bridge = mod_bridge
    return healthy_damage
