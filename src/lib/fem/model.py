from collections import defaultdict
from typing import Callable, Dict, List, NewType, Optional, Tuple

import numpy as np
from scipy.spatial import distance

from lib.model.bridge import Point, Section3D, Support3D
from util import round_m


class Node:
    """A node in a FE model.

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
    ):
        self.n_id = n_id
        self.x = round_m(x)
        self.y = round_m(y)
        self.z = round_m(z)
        self.pier = pier
        self.deck = deck
        self.comment = comment

    def command_3d(self):
        """OpenSees node command."""
        comment = "" if self.comment is None else f"; # {self.comment}"
        return (
            f"node {self.n_id} {round_m(self.x)} {round_m(self.y)}"
            + f" {round_m(self.z)}{comment}"
        )

    def distance(self, x: float, y: float, z: float):
        """Distance (with direction) from this node to coordinates."""
        return distance.euclidean((self.x, self.y, self.z), (x, y, z))

    def distance_n(self, node):
        """Distance (with direction) from this node to another node."""
        return self.distance(x=node.x, y=node.y, z=node.z)


NodesById = NewType("NodesById", Dict[int, Node])

# Nodes for a bridge deck.
DeckNodes = NewType("DeckNodes", List[List[Node]])
# A list of nodes for each shell.
DeckShellNodes = NewType("DeckShellNodes", List[Tuple[Node, Node, Node, Node]])
# Nodes for one wall of a pier. Indexed first by z then by x index.
WallNodes = NewType("WallNodes", List[List[Node]])
# Nodes for both walls of a single pier.
APierNodes = NewType("APierNodes", Tuple[WallNodes, WallNodes])
# Nodes for every pier.
PierNodes = NewType("PierNodes", List[APierNodes])
# Deck and pier nodes.
BridgeNodes = NewType("BridgeNodes", Tuple[DeckShellNodes, PierNodes])


class Shell:
    """A shell element in a FE model.

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
        pier: bool, whether this shell is on a pier.
        nodes_by_id: NodesById, nodes in this build context.

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
        nodes_by_id: NodesById,
    ):
        self.e_id = e_id
        self.ni_id = ni_id
        self.nj_id = nj_id
        self.nk_id = nk_id
        self.nl_id = nl_id
        self.pier = pier
        self.section = section
        self.nodes_by_id = nodes_by_id

        # Attach a reference to the section to each 'Node' and note if the node
        # belongs to a pier or to the bridge deck.
        for n_id in [self.ni_id, self.nj_id, self.nk_id, self.nl_id]:
            node = self.nodes_by_id[n_id]
            if pier:
                node.pier_section = self.section
            else:
                node.deck_section = self.section

    def node_ids(self):
        """IDs of this element's nodes."""
        return [self.ni_id, self.nj_id, self.nk_id, self.nl_id]

    def nodes(self):
        """This element's nodes."""
        return list(map(lambda n_id: self.nodes_by_id[n_id], self.node_ids()))

    def area(self):
        """Assumes a tetrahedron shape."""
        ni = self.nodes_by_id[self.ni_id]
        nj = self.nodes_by_id[self.nj_id]
        nk = self.nodes_by_id[self.nk_id]
        nl = self.nodes_by_id[self.nl_id]

        from fem.run.build.elements.util import poly_area

        return poly_area(
            [
                (ni.x, ni.y, ni.z),
                (nj.x, nj.y, nj.z),
                (nk.x, nk.y, nk.z),
                (nl.x, nl.y, nl.z),
            ]
        )

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


ShellsById = NewType("ShellsById", Dict[int, Shell])

# Shells for a bridge deck.
DeckShells = NewType("DeckShells", List[List[Shell]])
# Shells for one wall of a pier. Indexed first by z then by x index.
WallShells = NewType("WallShells", List[List[Shell]])
# Shells for both walls of a pier.
APierShells = NewType("APierShells", Tuple[WallShells, WallShells])
# Shells for every pier.
PierShells = NewType("PierShells", List[APierShells])
# Deck and pier shells.
BridgeShells = NewType("BridgeShells", Tuple[DeckShells, PierShells])


class BuildContext:
    """Stores nodes and shells for a FEM being built.

    Args:
        add_loads: List[Point], additional grid lines where to add nodes.
        refinement_radii: List[float], radii for sweeps to refine around loads.

    """

    def __init__(
        self,
        add_loads: List[Point],
        refinement_radii: List[float] = [],
        # refinement_radii: List[float] = [2, 1, 0.5],
    ):
        self.next_n_id = 1
        self.nodes_by_id: NodesById = dict()
        self.nodes_by_pos = dict()
        # A dict of x to dict of y to dict of z to Node.
        self.nodes_by_pos_dict = defaultdict(lambda: defaultdict(dict))

        self.next_s_id = 1
        self.shells_by_id: ShellsById = dict()
        self.shells_by_n_ids = dict()

        self.add_loads = add_loads
        for point in self.add_loads:
            assert point.y == 0
        self.refinement_radii = refinement_radii

    def new_n_id(self):
        self.next_n_id += 1
        return self.next_n_id - 1

    def new_s_id(self):
        self.next_s_id += 1
        return self.next_s_id - 1

    def get_node(
        self, x: float, y: float, z: float, deck: bool, comment: Optional[str] = None
    ) -> Node:
        x, y, z = round_m(x), round_m(y), round_m(z)
        pos = (x, y, z)
        if pos not in self.nodes_by_pos:
            n_id = self.new_n_id()
            node = Node(n_id=n_id, x=x, y=y, z=z, deck=deck, comment=comment)
            self.nodes_by_id[n_id] = node
            self.nodes_by_pos[pos] = node
            self.nodes_by_pos_dict[x][y][z] = node
        return self.nodes_by_pos[pos]

    def get_shell(
        self,
        ni_id: int,
        nj_id: int,
        nk_id: int,
        nl_id: int,
        pier: bool,
        section: Section3D,
    ) -> Shell:
        n_ids = (ni_id, nj_id, nk_id, nl_id)
        if n_ids not in self.shells_by_n_ids:
            s_id = self.new_s_id()
            shell = Shell(
                e_id=s_id,
                ni_id=ni_id,
                nj_id=nj_id,
                nk_id=nk_id,
                nl_id=nl_id,
                pier=pier,
                section=section,
                nodes_by_id=self.nodes_by_id,
            )
            self.shells_by_n_ids[n_ids] = shell
            self.shells_by_id[s_id] = shell
        return self.shells_by_n_ids[n_ids]

    def get_nodes_at_xy(self, x: float, y: float):
        x, y = round_m(x), round_m(y)
        return self.nodes_by_pos_dict[x][y].values()
