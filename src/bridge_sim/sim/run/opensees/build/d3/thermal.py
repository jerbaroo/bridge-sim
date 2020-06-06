from collections import defaultdict
from enum import Enum
from typing import Dict

import numpy as np

from bridge_sim.model import Config
from bridge_sim.sim.build import det_shells
from bridge_sim.sim.model import BuildContext, DeckShells, Node, SimParams
from bridge_sim.sim.run.opensees.build.d3.util import comment
from bridge_sim.util import print_d

# Print debug information for this file.
D: str = "fem.run.opensees.build.d3.thermal"
D: bool = False


def opensees_thermal_axial_deck_loads(
    c: Config, sim_params: SimParams, deck_elements: DeckShells, ctx: BuildContext
):
    """Thermal axial loads for deck shells, if in the simulation parameters."""
    if sim_params.axial_delta_temp is None:
        return ""

    class LoadDirection(Enum):
        """Direction a thermal load is applied to a shell."""

        XPOS = 1
        XNEG = 2
        ZPOS = 3
        ZNEG = 4

    def assert_load_direction(node_0: Node, node_1: Node, direction: LoadDirection):
        """Assert the load direction is perpendicular to the nodes."""
        if direction in [LoadDirection.XPOS, LoadDirection.XNEG]:
            assert node_0.x == node_1.x
        elif direction in [LoadDirection.ZPOS, LoadDirection.ZNEG]:
            assert node_0.z == node_1.z
        else:
            raise ValueError(f"Unknown thermal load direction {direction}")

    class ThermalLoad:
        """Total thermal load to be applied to a node."""

        def __init__(self):
            self.x = 0
            self.z = 0

        def add_load(self, magnitude: float, direction: LoadDirection):
            """Add a load in a given direction."""
            if direction == LoadDirection.XPOS:
                self.x += magnitude
            elif direction == LoadDirection.XNEG:
                self.x -= magnitude
            elif direction == LoadDirection.ZPOS:
                self.z += magnitude
            elif direction == LoadDirection.ZNEG:
                self.z -= magnitude
            else:
                raise ValueError(f"Unknown thermal load direction {direction}")

        def to_tcl(self, n_id: int):
            """Return a string with 0, 1, or 2 OpenSees load commands."""
            if np.isclose(self.x, 0) and np.isclose(self.z, 0):
                return ""
            return (
                f"\nload {n_id} {np.around(self.x, 3)} 0 {np.around(self.z, 3)} 0 0 0"
            )

    thermal_loads_by_nid: Dict[int, ThermalLoad] = defaultdict(ThermalLoad)
    for shell in det_shells(deck_elements):
        print_d(D, shell)
        print_d(D, np.array(deck_elements).shape)
        print_d(D, "")
        print_d(D, f"cte = {c.cte}")
        print_d(D, f"d_temp = {sim_params.axial_delta_temp}")
        shell_thermal_strain = c.cte * sim_params.axial_delta_temp
        shell_youngs_si = shell.section.youngs * 1e6
        shell_thermal_stress = shell_youngs_si * shell_thermal_strain
        print_d(D, f"shell youngs SI = {shell_youngs_si}")
        print_d(D, f"thermal stress = {shell_thermal_stress}")
        # For each cross section consider the pair of nodes at the corners.
        for n_id_0, n_id_1, load_direction in [
            (shell.ni_id, shell.nj_id, LoadDirection.ZPOS),
            (shell.nj_id, shell.nk_id, LoadDirection.XNEG),
            (shell.nk_id, shell.nl_id, LoadDirection.ZNEG),
            (shell.nl_id, shell.ni_id, LoadDirection.XPOS),
        ]:
            print_d(D, f"node ids = {n_id_0}, {n_id_1}")
            node_0, node_1 = ctx.nodes_by_id[n_id_0], ctx.nodes_by_id[n_id_1]
            assert_load_direction(
                node_0=node_0, node_1=node_1, direction=load_direction
            )
            node_distance = node_0.distance_n(node_1)
            assert node_distance > 0
            print_d(D, f"node distance = {node_distance}")
            cross_section_area = shell.section.thickness * node_distance
            print_d(D, f"cross section area = {cross_section_area}")
            cross_section_thermal_force_n = shell_thermal_stress * cross_section_area
            print_d(D, f"cross section thermal force = {cross_section_thermal_force_n}")
            nodal_thermal_force_n = cross_section_thermal_force_n / 2
            assert np.isclose(
                cross_section_thermal_force_n, (cross_section_thermal_force_n / 2) * 2
            )
            print_d(
                D,
                f"Before applying force node_0: x = {thermal_loads_by_nid[n_id_0].x} z = {thermal_loads_by_nid[n_id_0].z}",
            )
            print_d(
                D,
                f"Before applying force node_1: x = {thermal_loads_by_nid[n_id_1].x} z = {thermal_loads_by_nid[n_id_1].z}",
            )
            for n_id in [n_id_0, n_id_1]:
                thermal_loads_by_nid[n_id].add_load(
                    magnitude=nodal_thermal_force_n, direction=load_direction
                )
            print_d(
                D,
                f"After applying force node_0: x = {thermal_loads_by_nid[n_id_0].x} z = {thermal_loads_by_nid[n_id_0].z}",
            )
            print_d(
                D,
                f"After applying force node_1: x = {thermal_loads_by_nid[n_id_1].x} z = {thermal_loads_by_nid[n_id_1].z}",
            )

    thermal_load_str = "".join(
        [load.to_tcl(n_id) for n_id, load in thermal_loads_by_nid.items()]
    )
    return comment(
        "thermal loads",
        thermal_load_str,
        units="load nodeTag N_x N_y N_z N_rx N_ry N_rz",
    )


def opensees_thermal_moment_deck_loads(
    c: Config, sim_params: SimParams, deck_elements: DeckShells, ctx: BuildContext,
):
    """Thermal moment loads for deck shells, if in the simulation parameters."""
    if sim_params.moment_delta_temp is None:
        return ""

    class LoadDirection(Enum):
        """Direction a thermal load is applied to a shell."""

        XPOS = 1
        XNEG = 2
        ZPOS = 3
        ZNEG = 4

    def assert_load_direction(node_0: Node, node_1: Node, direction: LoadDirection):
        """Assert the load direction is perpendicular to the nodes."""
        # TODO: Remove return.
        return
        if direction in [LoadDirection.XPOS, LoadDirection.XNEG]:
            assert node_0.z == node_1.z
        elif direction in [LoadDirection.ZPOS, LoadDirection.ZNEG]:
            assert node_0.x == node_1.x
        else:
            raise ValueError(f"Unknown thermal load direction {direction}")

    class ThermalLoad:
        """Total thermal load to be applied to a node."""

        def __init__(self):
            self.x = 0
            self.z = 0

        def add_load(self, magnitude: float, direction: LoadDirection):
            """Add a load in a given direction."""
            if direction == LoadDirection.XPOS:
                self.x += magnitude
            elif direction == LoadDirection.XNEG:
                self.x -= magnitude
            elif direction == LoadDirection.ZPOS:
                self.z += magnitude
            elif direction == LoadDirection.ZNEG:
                self.z -= magnitude
            else:
                raise ValueError(f"Unknown thermal load direction {direction}")

        def to_tcl(self, n_id: int):
            """Return a string with 0, 1, or 2 OpenSees load commands."""
            if np.isclose(self.x, 0) and np.isclose(self.z, 0):
                return ""
            return (
                f"\nload {n_id} 0 0 0 {np.around(self.x, 3)} 0 {np.around(self.z, 3)}"
            )

    thermal_loads_by_nid: Dict[int, ThermalLoad] = defaultdict(ThermalLoad)
    for shell in det_shells(deck_elements):
        print_d(D, shell)
        print_d(D, np.array(deck_elements).shape)
        print_d(D, "")
        print_d(D, f"cte = {c.cte}")
        print_d(D, f"d_temp = {sim_params.moment_delta_temp}")
        shell_strain_top = c.cte * (sim_params.moment_delta_temp / 2)
        print_d(D, f"strain_top = {shell_strain_top}")
        shell_youngs_si = shell.section.youngs * 1e6
        shell_stress_top = shell_youngs_si * shell_strain_top
        print_d(D, f"shell youngs SI = {shell_youngs_si}")
        print_d(D, f"stress_top = {shell_stress_top}")
        # For each cross section consider the pair of nodes at the corners.
        for n_id_0, n_id_1, load_direction in [
            (shell.ni_id, shell.nj_id, LoadDirection.XPOS),
            (shell.nj_id, shell.nk_id, LoadDirection.ZPOS),
            (shell.nk_id, shell.nl_id, LoadDirection.XNEG),
            (shell.nl_id, shell.ni_id, LoadDirection.ZNEG),
        ]:
            print_d(D, f"node ids = {n_id_0}, {n_id_1}")
            node_0, node_1 = ctx.nodes_by_id[n_id_0], ctx.nodes_by_id[n_id_1]
            assert_load_direction(
                node_0=node_0, node_1=node_1, direction=load_direction
            )
            node_distance = node_0.distance_n(node_1)
            print_d(D, f"node distance = {node_distance}")
            print_d(D, f"section thickness = {shell.section.thickness}")
            force_top_n = (
                shell_stress_top
                * (shell.section.thickness / 2)
                * (1 / 2)
                * node_distance
            )
            moment_top_nm = force_top_n * (2 / 3) * (shell.section.thickness / 2)
            print_d(D, f"force top n = {force_top_n}")
            print_d(D, f"moment nm = {moment_top_nm}")
            print_d(
                D,
                f"Before applying moment: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}",
            )
            print_d(
                D,
                f"Before applying moment: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}",
            )
            # The moment per node is moment_top_nm / 2. But since we also want
            # to include moment_bottom_nm / 2 which is equal to moment_top_nm,
            # then we just use moment_top_nm.
            for n_id in [n_id_0, n_id_1]:
                thermal_loads_by_nid[n_id].add_load(
                    magnitude=moment_top_nm, direction=load_direction
                )
            print_d(
                D,
                f"After applying moment: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}",
            )
            print_d(
                D,
                f"After applying moment: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}",
            )

    thermal_load_str = "".join(
        [load.to_tcl(n_id) for n_id, load in thermal_loads_by_nid.items()]
    )
    return comment(
        "thermal loads",
        thermal_load_str,
        units="load nodeTag N_x N_y N_z N_rx N_ry N_rz",
    )
