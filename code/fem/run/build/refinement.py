"""Refinement of the deck mesh."""
from typing import List

import numpy as np

from model.bridge import Bridge
from util import round_m


def get_deck_refinement_positions(bridge: Bridge):
    x_positions, z_positions = [], []

    # Adds three x positions per pier.
    add_x_per_pier = 9
    for pier in bridge.supports:
        half = pier.width_top / 2
        assert half * 2 == pier.width_top
        # The '+ 2' is to account for positions of the supports which will
        # already be accounted for.
        for x_position in np.linspace(pier.x - half, pier.x + half, add_x_per_pier + 2):
            x_positions.append(x_position)

    return x_positions, z_positions
