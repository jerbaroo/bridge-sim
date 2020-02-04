"""Bridge scenarios."""
from copy import deepcopy
from typing import Callable, NewType, Tuple

from config import Config
from fem.params import SimParams
from fem.responses import SimResponses
from model.bridge import Bridge
from model.load import PierSettlement
from model.response import ResponseType
from model.scenario import DamageScenario
from util import round_m


class HealthyDamage(DamageScenario):
    def __init__(self):
        super().__init__(name="normal")


CrackArea = NewType("CrackArea", Tuple[float, float, float, float])


class CrackedDamage(DamageScenario):
    """A cracked bridge, defined by an area of a bridge's deck to crack."""

    def __init__(
        self, name: str, crack_area: Callable[[Bridge], CrackArea],
    ):
        def mod_bridge(bridge: Bridge):
            bridge.type = self.name
            self._crack_deck(bridge)
            return bridge

        super().__init__(name=name, mod_bridge=mod_bridge)
        self.crack_area = crack_area

    def _crack_deck(self, bridge: Bridge):
        """Adds cracked sections to the given bridge's deck."""
        c_x_start, c_z_start, c_x_end, c_z_end = list(
            map(round_m, self.crack_area(bridge))
        )

        if callable(bridge.sections):
            raise NotImplementedError()

        # Find where the cracked area and current sections overlap.
        overlaps: List[Tuple[Section3D, float, float, float, float]] = []
        for section in bridge.sections:
            s_x_start = round_m(bridge.x(section.start_x_frac))
            s_z_start = round_m(bridge.z(section.start_z_frac))
            s_x_end = round_m(bridge.x(section.end_x_frac))
            s_z_end = round_m(bridge.z(section.end_z_frac))

            overlap_x_start = max(c_x_start, s_x_start)
            overlap_z_start = max(c_z_start, s_z_start)
            overlap_x_end = min(c_x_end, s_x_end)
            overlap_z_end = min(c_z_end, s_z_end)

            if overlap_x_end - overlap_x_start > 0:
                if overlap_z_end - overlap_z_start > 0:
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
        cracked_sections, max_id = [], bridge.sections[-1].id
        for i, (section, x_start, z_start, x_end, z_end) in enumerate(overlaps):
            cracked_section = deepcopy(section)
            cracked_section.id = max_id + i + 1
            cracked_section.youngs *= 1 / 3
            cracked_section.start_x_frac = bridge.x_frac(x_start)
            cracked_section.start_z_frac = bridge.z_frac(z_start)
            cracked_section.end_x_frac = bridge.x_frac(x_end)
            cracked_section.end_z_frac = bridge.z_frac(z_end)
            cracked_sections.append(cracked_section)

        bridge.sections = cracked_sections + bridge.sections


def center_lane_crack(percent: float = 20, lane: int = 0) -> CrackedDamage:
    """A bridge with the center of a lane cracked."""
    x_frac = percent / 100

    def crack_area(bridge: Bridge) -> CrackArea:
        x_start, z_start = bridge.x(0.5 - (x_frac / 2)), bridge.lanes[lane].z_min
        length, width = bridge.x(x_frac), bridge.lanes[lane].width
        return x_start, z_start, x_start + length, z_start + width

    return CrackedDamage(
        name=f"crack-lane-{lane}-center-{percent}", crack_area=crack_area
    )


def start_lane_crack(percent: float = 20, lane: int = 0) -> CrackedDamage:
    """A bridge with the start of the lane cracked."""
    x_frac = percent / 100

    def crack_area(bridge: Bridge) -> CrackArea:
        x_start, z_start = 0, bridge.lanes[lane].z_min
        length, width = bridge.x(x_frac), bridge.lanes[lane].width
        return x_start, z_start, x_start + length, z_start + width

    return CrackedDamage(
        name=f"crack-lane-{lane}-start-{percent}", crack_area=crack_area
    )


class PierDispDamage(DamageScenario):
    def __init__(self, pier_disps: [PierSettlement], name_prefix: str = ""):
        if len(pier_disps) < 1:
            raise ValueError("At least 1 PierDisp required")
        name = name_prefix + "-".join(list(map(lambda pd: pd.id_str(), pier_disps)))
        super().__init__(name=name)
        self.pier_disps = pier_disps


def equal_pier_disp(bridge: Bridge, displacement: float) -> PierDispDamage:
    """All piers with equal given displacement."""
    return PierDispDamage(
        pier_disps=[
            PierSettlement(displacement=displacement, pier=p)
            for p in range(len(bridge.supports))
        ],
        name_prefix="equal-piers",
    )


def longitudinal_pier_disp(bridge: Bridge, start: float, step: float) -> PierDispDamage:
    """Pier displacement that increases in longitudinal direction."""
    increase_every = len(set(pier.z for pier in bridge.supports))
    pier_disps = []
    displacement = start
    for p in range(len(bridge.supports)):
        if p != 0 and p % increase_every == 0:
            displacement += step
        pier_disps.append(PierSettlement(displacement=displacement, pier=p))
    return PierDispDamage(pier_disps=pier_disps, name_prefix="longitudinal")


class ThermalDamage(DamageScenario):
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

    def to_stress(self, c: Config, sim_responses: SimResponses):
        if sim_responses.response_type != ResponseType.Strain:
            raise ValueError("Can only convert Strain not {sim_responses.response_type}")
        if self.axial_delta_temp != 0 and self.moment_delta_temp != 0:
            raise ValueError("Must be only axial or moment loading")
        if self.axial_delta_temp != 0:
            sim_responses = sim_responses.map(lambda r: r * 1E-6 - (c.cte * c.unit_axial_delta_temp_c))
            sim_responses = sim_responses.to_stress(c.bridge)
        elif self.moment_delta_temp != 0:
            sim_responses = sim_responses.map(lambda r: r * 1E-6 + (0.5 * c.cte * c.unit_moment_delta_temp_c))
            sim_responses = sim_responses.to_stress(c.bridge)
        else:
            raise ValueError("Dont know how to convert to stress")
        return sim_responses


def thermal_damage(axial_delta_temp: float = 0, moment_delta_temp: float = 0, mod_msl: float = 0.8):
    """Like ThermalDamage, but also modifies the bridge's MSL parameter."""
    td = ThermalDamage(axial_delta_temp=axial_delta_temp, moment_delta_temp=moment_delta_temp)
    og_mod_bridge = td.mod_bridge
    def mod_bridge(b: Bridge):
        b = og_mod_bridge(b)
        b.base_mesh_deck_max_x *= mod_msl
        b.base_mesh_deck_max_z *= mod_msl
        b.base_mesh_pier_max_long *= mod_msl
        return b
    td.mod_bridge = mod_bridge
    return td
