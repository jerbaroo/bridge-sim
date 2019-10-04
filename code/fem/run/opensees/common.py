"""Common functions used by OpenSees FEMRunner components."""
import itertools
from typing import List, Optional, Tuple

from config import Config
from model.bridge import Support3D
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
    """A node that can be converted to an OpenSees command.

    Args:
        n_id: int, the ID of this node.
        x: float, the x position of this node on the bridge.
        y: float, the y position of this node on the bridge.
        z: float, the z position of this node on the bridge.
        comment: Optional[str], an optional comment for the .tcl file.
        support: Optional[3D], the support that this node may belong to.

    """
    def __init__(
            self, n_id: int, x: float, y: float, z: float,
            comment: Optional[str] = None,
            support: Optional[Support3D] = None):
        self.n_id = n_id
        self.x = round_m(x)
        self.y = round_m(y)
        self.z = round_m(z)
        self.comment = comment
        self.support = support

    def command_3d(self):
        """OpenSees node command."""
        comment = "" if self.comment is None else f"; # {self.comment}"
        return (f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
                + f" {round_m(self.z)}{comment}")


def traverse_3d_nodes(deck_nodes: List[List[Node]]):
    """Traverse built nodes in a deterministic order."""
    return list(itertools.chain.from_iterable(deck_nodes))

