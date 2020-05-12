"""Refinement of the deck mesh."""
from collections import OrderedDict
from typing import Dict, List

import numpy as np

from lib.fem.params import SimParams
from lib.model.bridge import Bridge
from lib.model.load import PointLoad
from util import round_m


def get_pier_refinement_positions(bridge: Bridge) -> "DeckPositions":
    x_positions, z_positions = [], []
    add_x_per_pier = 9  # Number of x positions to add per pier.
    for pier in bridge.supports:
        half = pier.width_top / 2
        assert half * 2 == pier.width_top
        # The '+ 2' is to account for positions of the supports which will
        # already be accounted for.
        for x_position in np.linspace(pier.x - half, pier.x + half, add_x_per_pier + 2):
            x_positions.append(x_position)
    return x_positions, z_positions


def get_load_refinement_positions(
    bridge: Bridge, loads: [PointLoad]
) -> "DeckPositions":
    # Offsets from the load, where to add a node line.
    offsets = [-1, -3, -6, -10, 1, 3, 6, 10]  # In mm
    offsets = np.array(offsets) / 1000  # In m.
    x_positions, z_positions = [], []
    for load in loads:
        load_x = bridge.x(load.x_frac)
        load_z = bridge.z(load.z_frac)
        for offset in offsets:
            node_x = load_x + offset
            if bridge.x_min <= node_x <= bridge.x_max:
                x_positions.append(node_x)
            node_z = load_z + offset
            if bridge.z_min <= node_z <= bridge.z_max:
                z_positions.append(node_z)
    return x_positions, z_positions


def get_deck_refinement_positions(
    bridge: Bridge, sim_params: SimParams
) -> Dict[str, "DeckPositions"]:
    result = OrderedDict()
    result["pier-refinement"] = get_pier_refinement_positions(bridge)
    result["load-refinement"] = get_load_refinement_positions(
        bridge=bridge, loads=sim_params.ploads
    )
    return result
