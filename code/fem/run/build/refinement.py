"""Refinement of the deck mesh."""
from collections import OrderedDict
from typing import Dict, List

import numpy as np

from model.bridge import Bridge
from util import round_m


def get_pier_refinement_positions(
        bridge: Bridge) -> "DeckPositions":
    x_positions, z_positions = [], []
    add_x_per_pier = 9  # Number of x positions to add per pier.
    for pier in bridge.supports:
        half = pier.width_top / 2
        assert half * 2 == pier.width_top
        # The '+ 2' is to account for positions of the supports which will
        # already be accounted for.
        for x_position in np.linspace(
                pier.x - half, pier.x + half, add_x_per_pier + 2):
            x_positions.append(x_position)
    return x_positions, z_positions


def get_deck_refinement_positions(
        bridge: Bridge) -> Dict[str, "DeckPositions"]:
    result = OrderedDict()
    result["pier-refinement"] = get_pier_refinement_positions(bridge)
    return result
