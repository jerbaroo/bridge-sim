from collections import defaultdict
from typing import Dict

import numpy as np
import scipy.constants as constants

from bridge_sim.model import Config
from bridge_sim.sim.build import det_shells
from bridge_sim.sim.model import SimParams, DeckShells


def opensees_self_weight_loads(
    config: Config, sim_params: SimParams, deck_shells: DeckShells
):
    """Loads for the self weight, if in the simulation parameters."""
    if not sim_params.self_weight:
        return ""

    def to_tcl(n_id: int, load_intensity: float):
        """Return an empty string or a load string."""
        if np.isclose(load_intensity, 0):
            return ""
        return f"\nload {n_id} 0 {load_intensity} 0 0 0 0"

    yloads_by_nid: Dict[int, float] = defaultdict(lambda: 0)
    for shell in det_shells(deck_shells):
        node_newtons = shell.mass(config) * constants.g / 4 * 1e3
        for node in shell.nodes():
            yloads_by_nid[node.n_id] += node_newtons
    load_str = "".join([to_tcl(n_id, li) for n_id, li in yloads_by_nid.items()])
    from bridge_sim.sim.run.opensees.build.d3 import comment

    return comment(
        "thermal loads", load_str, units="load nodeTag N_x N_y N_z N_rx N_ry N_rz",
    )
