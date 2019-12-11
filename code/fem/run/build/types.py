"""Common functions used by OpenSees FEMRunner components."""
import itertools
from typing import Dict, List, NewType, Optional, Tuple

import numpy as np
from scipy.spatial import distance

from config import Config
from model.bridge import Point, Section3D, Section3DPier, Support3D
from util import print_d, round_m


# Print debug information for this file.
D: bool = True


class Node:
    """A node that can be converted to an OpenSees command.

    Args:
        n_id: int, the ID of this node.
        x: float, x position of this node on the bridge.
        y: float, y position of this node on the bridge.
        z: float, z position of this node on the bridge.
        deck: bool, whether this node belongs to the bridge deck.
        pier: Optional[Support3D], a pier that this node may belong to.
        comment: Optional[str], an optional comment for the .tcl file.
        support: Optional[3D], a support that this node may belong to.

    Attrs:
        section: Section3D, a section that may be attached, or not.

    """

    def __init__(
        self,
        n_id: int,
        x: float,
        y: float,
        z: float,
        deck: bool,
        pier: Optional[Support3D] = None,
        comment: Optional[str] = None,
        support: Optional[Support3D] = None,
    ):
        self.n_id = n_id
        self.x = round_m(x)
        self.y = round_m(y)
        self.z = round_m(z)
        self.pier = pier
        self.deck = deck
        self.comment = comment
        self.support = support

    def command_3d(self):
        """OpenSees node command."""
        comment = "" if self.comment is None else f"; # {self.comment}"
        return (
            f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
            + f" {round_m(self.z)}{comment}"
        )

    def distance(self, x: float, y: float, z: float):
        """Distance form this node to the given coordinates."""
        return distance.euclidean((self.x, self.y, self.z), (x, y, z))


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
    deck_nodes: DeckNodes, all_support_nodes: AllSupportNodes
) -> List[Node]:
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


class ShellElement:
    """A shell element that can be converted to an OpenSees command.

    NOTE: When this constructor is called additional work is done in setting a
    reference to the given section to all given nodes. Thus associating to each
    given node a section, this information that is attached to nodes is useful
    for creating colored plots of properties of the 3D model.

    Args:
        e_id: int, index for this shell element.
        ni_id: int, index of the node at corner i of this shell element.
        nj_id: int, index of the node at corner j of this shell element.
        nk_id: int, index of the node at corner k of this shell element.
        nl_id: int, index of the node at corner l of this shell element.
        section: Section3D, section that this shell element belongs to.
        support_position_index: Optional[Tuple[int, int, int, int]], a 4-tuple
            of the support index, support wall index, and z and y indices

    """

    def __init__(
        self,
        e_id: int,
        ni_id: int,
        nj_id: int,
        nk_id: int,
        nl_id: int,
        section: Section3D,
        pier: bool,
        nodes_by_id: Dict[int, Node],
        support_position_index: Optional[Tuple[int, int, int, int]] = None,
    ):
        self.e_id = e_id
        self.ni_id = ni_id
        self.nj_id = nj_id
        self.nk_id = nk_id
        self.nl_id = nl_id
        self.pier = pier
        self.section = section
        self.support_position_index = support_position_index
        self.nodes_by_id = nodes_by_id

        # Attach a reference to the section to each 'Node' and note if the node
        # belongs to a pier or to the bridge deck.
        for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
            node = self.nodes_by_id[n_id]
            if pier:
                node.pier_section = self.section
            else:
                node.deck_section = self.section

    def area(self):
        """Assumes a tetrahedron shape."""
        ni = self.nodes_by_id[self.ni_id]
        nj = self.nodes_by_id[self.nj_id]
        nk = self.nodes_by_id[self.nk_id]
        nl = self.nodes_by_id[self.nl_id]

        from fem.run.build.elements.util import poly_area
        return poly_area([
            (ni.x, ni.y, ni.z),
            (nj.x, nj.y, nj.z),
            (nk.x, nk.y, nk.z),
            (nl.x, nl.y, nl.z),
        ])

    def center(self) -> Point:
        """Point at the center of the element."""
        if not hasattr(self, "_center"):
            node_0 = self.nodes_by_id[self.ni_id]
            node_1 = self.nodes_by_id[self.nk_id]
            delta_x = abs(node_0.x - node_1.x)
            delta_y = abs(node_0.y - node_1.y)
            delta_z = abs(node_0.z - node_1.z)
            min_x = min(node_0.x, node_1.x)
            min_y = min(node_0.y, node_1.y)
            min_z = min(node_0.z, node_1.z)
            self._center = Point(
                x=min_x + delta_x / 2, y=min_y + delta_y / 2, z=min_z + delta_z / 2
            )
        return self._center

    def length(self) -> float:
        """The length of this element (longitudinal direction)."""
        if not hasattr(self, "_length"):
            min_x, max_x = np.inf, -np.inf
            for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
                node_x = self.nodes_by_id[n_id].x
                if node_x < min_x:
                    min_x = node_x
                if node_x > max_x:
                    max_x = node_x
            self._length = max_x - min_x
        return self._length

    def width(self) -> float:
        """The width of this element (longitudinal direction)."""
        if not hasattr(self, "_width"):
            min_z, max_z = np.inf, -np.inf
            for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
                node_z = self.nodes_by_id[n_id].z
                if node_z < min_z:
                    min_z = node_z
                if node_z > max_z:
                    max_z = node_z
            self._width = max_z - min_z
        return self._width

    def command_3d(self):
        """OpenSees element command."""
        repr_section = repr(self.section).replace("\n", " ")
        return (
            f"element ShellMITC4 {self.e_id} {self.ni_id} {self.nj_id}"
            + f" {self.nk_id} {self.nl_id} {self.section.id}; # {repr_section}"
        )


# The shell elements that make up a bridge deck. Represented as a matrix of Node
# ordered by z then x position. Only used in 3D modeling.
DeckElements = NewType("DeckElements", List[List[ShellElement]])


# The shell elements that make up a bridge's piers. Represented as a list of
# Node. Only used in 3D modeling. TODO: Avoid loss of structural information.
AllPierElements = NewType("AllPierElements", List[ShellElement])


def bridge_3d_elements(
    deck_elements: DeckElements, all_pier_elements: AllPierElements
) -> List[ShellElement]:
    """All a 3D bridge's shell elements in a deterministic order."""
    all_elements = list(itertools.chain.from_iterable(deck_elements))
    for pier_element in all_pier_elements:
        all_elements.append(pier_element)
    assert isinstance(all_elements[0], ShellElement)
    assert isinstance(all_elements[-1], ShellElement)
    return all_elements
