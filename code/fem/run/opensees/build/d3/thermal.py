from collections import defaultdict
from enum import Enum
from itertools import chain

import numpy as np

from config import Config
from fem.params import SimParams
from fem.run.build.types import DeckElements, Node
from fem.run.opensees.build.d3.util import comment


def opensees_thermal_axial_deck_loads(
    c: Config, sim_params: SimParams, deck_elements: DeckElements, nodes_by_id
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
            load_str = ""
            if not np.isclose(self.x, 0):
                load_str += f"\nload {n_id} {self.x} 0 0 0 0 0"
            if not np.isclose(self.z, 0):
                load_str += f"\nload {n_id} 0 0 {self.z} 0 0 0"
            return load_str

    thermal_loads_by_nid: Dict[int, ThermalLoad] = defaultdict(ThermalLoad)
    for shell in chain.from_iterable(deck_elements):
        print(shell)
        print(np.array(deck_elements).shape)
        print()
        print(f"cte = {shell.section.cte}")
        print(f"d_temp = {sim_params.axial_delta_temp}")
        shell_thermal_strain = shell.section.cte * sim_params.axial_delta_temp
        print(f"thermal strain = {shell_thermal_strain}")
        shell_youngs_si = shell.section.youngs * 1e6
        shell_thermal_stress = shell_youngs_si * shell_thermal_strain
        print(f"shell youngs SI = {shell_youngs_si}")
        print(f"thermal stress = {shell_thermal_stress}")
        # For each cross section consider the pair of nodes at the corners.
        for n_id_0, n_id_1, load_direction in [
            (shell.ni_id, shell.nj_id, LoadDirection.ZPOS),
            (shell.nj_id, shell.nk_id, LoadDirection.XNEG),
            (shell.nk_id, shell.nl_id, LoadDirection.ZNEG),
            (shell.nl_id, shell.ni_id, LoadDirection.XPOS),
        ]:
            print(f"node ids = {n_id_0}, {n_id_1}")
            node_0, node_1 = nodes_by_id[n_id_0], nodes_by_id[n_id_1]
            assert_load_direction(
                node_0=node_0, node_1=node_1, direction=load_direction
            )
            node_distance = node_0.distance_n(node_1)
            print(f"node distance = {node_distance}")
            cross_section_area = shell.section.thickness * node_distance
            print(f"cross section area = {cross_section_area}")
            cross_section_thermal_force_n = shell_thermal_stress * cross_section_area
            print(f"cross section thermal force = {cross_section_thermal_force_n}")
            nodal_thermal_force_n = cross_section_thermal_force_n / 2
            assert np.isclose(nodal_thermal_force_n * 2, cross_section_thermal_force_n)
            print(
                f"Before applying force: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}"
            )
            print(
                f"Before applying force: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}"
            )
            for n_id in [n_id_0, n_id_1]:
                thermal_loads_by_nid[n_id].add_load(
                    magnitude=nodal_thermal_force_n, direction=load_direction
                )
            print(
                f"After applying force: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}"
            )
            print(
                f"After applying force: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}"
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
    c: Config, sim_params: SimParams, deck_elements: DeckElements, nodes_by_id
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
            load_str = ""
            if not np.isclose(self.x, 0):
                load_str += f"\nload {n_id} 0 0 0 {-self.z} 0 0"
            if not np.isclose(self.z, 0):
                load_str += f"\nload {n_id} 0 0 0 0 0 {-self.x}"
            return load_str

    thermal_loads_by_nid: Dict[int, ThermalLoad] = defaultdict(ThermalLoad)
    for shell in chain.from_iterable(deck_elements):
        print(shell)
        print(np.array(deck_elements).shape)
        print()
        print(f"cte = {shell.section.cte}")
        print(f"d_temp = {sim_params.moment_delta_temp}")
        shell_strain_top = shell.section.cte * sim_params.moment_delta_temp
        print(f"strain_top = {shell_strain_top}")
        shell_youngs_si = shell.section.youngs * 1e6
        shell_stress_top = shell_youngs_si * shell_strain_top
        print(f"shell youngs SI = {shell_youngs_si}")
        print(f"stress_top = {shell_stress_top}")
        # For each cross section consider the pair of nodes at the corners.
        for n_id_0, n_id_1, load_direction in [
            (shell.ni_id, shell.nj_id, LoadDirection.ZPOS),
            (shell.nj_id, shell.nk_id, LoadDirection.XNEG),
            (shell.nk_id, shell.nl_id, LoadDirection.ZNEG),
            (shell.nl_id, shell.ni_id, LoadDirection.XPOS),
        ]:
            print(f"node ids = {n_id_0}, {n_id_1}")
            node_0, node_1 = nodes_by_id[n_id_0], nodes_by_id[n_id_1]
            assert_load_direction(
                node_0=node_0, node_1=node_1, direction=load_direction
            )
            node_distance = node_0.distance_n(node_1)
            print(f"node distance = {node_distance}")
            print(f"section thickness = {shell.section.thickness}")
            force_top_n = (
                shell_stress_top
                * (shell.section.thickness / 2)
                * (1 / 2)
                * node_distance
            )
            moment_top_nm = force_top_n * (2 / 3) * (shell.section.thickness / 2)
            print(f"force top n = {force_top_n}")
            print(f"moment nm = {moment_top_nm}")
            print(
                f"Before applying moment: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}"
            )
            print(
                f"Before applying moment: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}"
            )
            # The moment per node is moment_top_nm / 2. But since we also want
            # to include moment_bottom_nm / 2 which is equal to moment_top_nm,
            # then we just use moment_top_nm.
            for n_id in [n_id_0, n_id_1]:
                thermal_loads_by_nid[n_id].add_load(
                    magnitude=moment_top_nm, direction=load_direction
                )
            print(
                f"After applying moment: node_0 = {thermal_loads_by_nid[n_id_0].x}, {thermal_loads_by_nid[n_id_0].z}"
            )
            print(
                f"After applying moment: node_1 = {thermal_loads_by_nid[n_id_1].x}, {thermal_loads_by_nid[n_id_1].z}"
            )

    thermal_load_str = "".join(
        [load.to_tcl(n_id) for n_id, load in thermal_loads_by_nid.items()]
    )
    return comment(
        "thermal loads",
        thermal_load_str,
        units="load nodeTag N_x N_y N_z N_rx N_ry N_rz",
    )
