"""Common functions used by OpenSees FEMRunner components."""
import itertools
from typing import List, NewType, Optional, Tuple

import numpy as np

from config import Config
from model.bridge import Support3D
from util import print_d, round_m


# Print debug information for this file.
D: bool = True


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

# The nodes that make up a bridge deck. Represented as a matrix of Node ordered
# by z then x position. Only used in 3D modeling.
DeckNodes = NewType("DeckNodes", List[List[Node]])

# The nodes that make up one of a support's walls. Represented as a matrix of
# Node ordered by z then y position. Only used in 3D modeling.
WallNodes = NewType("WallNodes", List[List[Node]])

# Support nodes are a 2-tuple of wall nodes (two walls per support). Only used
# in 3D modeling.
SupportNodes = NewType("SupportNodes", Tuple[WallNodes, WallNodes])

# The support nodes for all a bridge's supports. Only used in 3D modeling.
AllSupportNodes = NewType("AllSupportNodes", List[SupportNodes])


def bridge_3d_nodes(
        deck_nodes: List[List[Node]], all_support_nodes: AllSupportNodes):
    """All a 3D bridge's nodes in a deterministic order."""
    all_nodes = list(itertools.chain.from_iterable(deck_nodes))
    for support_nodes in all_support_nodes:
        for wall_nodes in support_nodes:
            for y_nodes in wall_nodes:
                for node in y_nodes:
                    all_nodes.append(node)
    assert isinstance(all_nodes[0], Node)
    assert isinstance(all_nodes[-1], Node)
    print_d(D, f"Total 3D bridge nodes: {len(all_nodes)}")
    return all_nodes
