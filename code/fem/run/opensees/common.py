"""Common functions used by OpenSees FEMRunner components."""
import itertools
from typing import List, Optional, Tuple

from config import Config
from util import round_m

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


class Node:
    """A node that can be converted to an OpenSees command."""
    def __init__(
            self, n_id: int, x: float, y: float, z: float,
            comment: Optional[str] = None):
        self.n_id = n_id
        self.x = x
        self.y = y
        self.z = z
        self.comment = comment

    def command_3d(self):
        """OpenSees node command."""
        comment_str = "" if self.comment is None else f" # {self.comment}"
        return (f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
                + f" {round_m(self.z)}{comment_str}")


def traverse_3d_nodes(deck_nodes: List[List[Node]]):
    """Traverse built nodes in a deterministic order."""
    return list(itertools.chain.from_iterable(deck_nodes))

