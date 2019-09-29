"""Common functions used by OpenSees FEMRunner components."""
from typing import Tuple

from config import Config

import numpy as np


def num_deck_nodes(c: Config) -> Tuple[int, int]:
    """The number of deck nodes in x and z directions."""
    num_nodes_x = c.bridge.length / c.os_node_step + 1
    num_nodes_z = c.bridge.width / c.os_node_step_z + 1
    if not np.isclose(num_nodes_x, np.round(num_nodes_x)):
        raise ValueError(
            f"Bridge length {c.bridge.length} not evenly divisible by"
            + f" c.os_node_step {c.os_node_step}, was {num_nodes_x}")
    if not np.isclose(num_nodes_z, np.round(num_nodes_z)):
        raise ValueError(
            f"Bridge width {c.bridge.width} not evenly divisible by"
            + f" c.os_node_step_z {c.os_node_step_z}, was {num_nodes_z}")
    num_nodes_x = int(np.round(num_nodes_x))
    num_nodes_z = int(np.round(num_nodes_z))
    return num_nodes_x, num_nodes_z
