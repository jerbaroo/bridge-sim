"""Build OpenSees 3D model files."""
from itertools import chain
from collections import OrderedDict, defaultdict
from copy import deepcopy
from typing import Dict, List, NewType, Optional, Tuple, Union

import numpy as np

from config import Config
from fem.params import ExptParams, SimParams
from fem.run.opensees.common import AllPierElements, AllSupportNodes,\
    DeckElements, DeckNodes, Node, ShellElement, bridge_3d_elements,\
    bridge_3d_nodes
from model.bridge import Bridge, Section3D, Support3D
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from util import print_d, print_i, print_w, round_m, st


def assert_sorted(l):
    assert all(l[i] <= l[i+1] for i in range(len(l)-1))


# Print debug information for this file.
D: str = "fem.run.opensees.build.d3"
# D: bool = False

##### Begin node factory #####

# A dictionary of x position to y position to z position to 'Node'.
all_nodes = defaultdict(lambda: defaultdict(dict))

# A dictionary of 'Node' ID to 'Node'.
#
# If you call 'build_model_3d' and then call '.values' on this dictionary it
# provides an easy way to get all 'Node's for the previously built model.
nodes_by_id = dict()


def get_node(
        x: float, y: float, z: float, deck: bool = False, pier: Optional[Support3D] = None,
        comment_str: Optional[str] = None, support: Optional[Support3D] = None):
    """Get a 'Node' if one already exists at position, else create a new one.

    NOTE: Use this to contruct 'Node's, don't do it directly!

    Args:
        deck: bool, whether the requested Node belongs to a deck.
        pier: Optional[Support3D], a pier the requested Node may belong to.

    """
    x = round_m(x)
    y = round_m(y)
    z = round_m(z)
    # Create the new 'Node' if necessary.
    if z not in all_nodes[x][y]:
        new_node = Node(
            n_id=next_node_id(), x=x, y=y, z=z, comment=comment_str,
            support=support, pier=pier, deck=deck)
        all_nodes[x][y][z] = new_node
        nodes_by_id[new_node.n_id] = new_node
    # Return the node and attach deck and pier information.
    node = all_nodes[x][y][z]
    node.deck = node.deck or deck
    node.pier = node.pier if node.pier is not None else pier
    return node


##### End node factory #####
##### Begin node IDs #####

_node_id = None


def next_node_id() -> int:
    """Return the next node ID and increment the counter."""
    global _node_id
    result = _node_id
    _node_id = result + 1
    return result


def reset_nodes():
    """Reset node IDs to 0, e.g. when building a new model file."""
    global _node_id
    _node_id = 1
    global all_nodes
    all_nodes = defaultdict(lambda: defaultdict(dict))
    global nodes_by_id
    nodes_by_id.clear()
    assert len(list(nodes_by_id.values())) == 0


reset_nodes()


# Amount to fast forward Node IDs by.
ff_mod = 10000  # A large default value for testing.


def ff_node_ids():
    """Fast forward node IDs until divisible by 'ff_mod'."""
    global _node_id
    while _node_id % ff_mod != 0:
        _node_id += 1


def set_ff_mod(n: int):
    """Set amount to fast-forward node IDs by.

    'ff_mod' will be set to a power of 10 greater than n.

    """
    pow_10 = 1
    while pow_10 <= n:
        pow_10 = pow_10 * 10
    global ff_mod
    ff_mod = pow_10


##### End node IDs #####
##### Begin element IDs #####

_elem_id = None


def next_elem_id() -> int:
    """Return the next element ID and increment the counter."""
    global _elem_id
    result = _elem_id
    _elem_id = result + 1
    return result


def reset_elem_ids():
    """Reset element IDs to 0, e.g. when building a new model file."""
    global _elem_id
    _elem_id = 1
reset_elem_ids()


def ff_elem_ids(mod: int):
    """Fast forward element IDs until divisible by "mod"."""
    global _elem_id
    while _elem_id % mod != 0:
        _elem_id += 1


##### End element IDs #####
##### Begin some comment-related things #####

opensees_intro = """
# Programatically generated file.
#
# Units:
# - dimension: metre
# - force: newton
#
# Dimension order is
# - x: longitudinal
# - y: vertical
# - z: transverse"""


def comment(c: str, inner: str, units: Optional[str] = None):
    """Add 'Begin c' and 'End c' comments around an inner block.

    Optionally add another 'units' comment before the inner block.

    """
    units_str = "" if units is None else f"# {units}\n"
    return units_str + f"# Begin {c}\n" + inner + f"\n# End {c}"


##### End some comment-related things #####
##### Begin nodes #####

# A list of x and z positions of deck nodes.
DeckPositions = NewType("DeckPositions", Tuple[List[float], List[float]])


def get_x_positions_of_pier_deck_nodes(c: Config) -> List[List[float]]:
    """The x positions of the deck nodes of each pier."""
    x_positions = []
    for support in c.bridge.supports:
        x_positions.append([])
        support_half_length = support.length / 2
        x_positions[-1].append(round_m(support.x - support_half_length))
        x_positions[-1].append(round_m(support.x + support_half_length))
        assert_sorted(x_positions[-1])
    return x_positions


def get_base_mesh_z_positions_of_pier_deck_nodes(c: Config) -> List[List[float]]:
    """The z positions of deck nodes of each pier's base mesh."""
    z_positions = []
    for support in c.bridge.supports:
        z_positions.append([support.z - (support.width_top / 2)])
        z_step = support.width_top / (c.bridge.base_mesh_pier_nodes_z - 1)
        for _ in range(c.bridge.base_mesh_pier_nodes_z - 1):
            z_positions[-1].append(z_positions[-1][-1] + z_step)
        assert_sorted(z_positions[-1])
    return list(map(round_m, z_positions))


# TODO: Experimental, but I think this works.
DECK_NODES_IN_PIER = True


def get_z_positions_of_pier_deck_nodes(
        c: Config, deck_positions: DeckPositions, simple_mesh: bool
        ) -> List[List[float]]:
    """The z positions of deck nodes of each pier (including deck mesh)."""
    assert_sorted(deck_positions[1])
    all_base_pier_z_positions = get_base_mesh_z_positions_of_pier_deck_nodes(c)
    # For each pier, find the z positions from the deck grid which fall within
    # the z positions of that pier's base mesh and include in the list.
    all_pier_z_positions = []
    for p, base_pier_z_positions in enumerate(all_base_pier_z_positions):
        assert_sorted(base_pier_z_positions)
        # Start by including the z positions of the pier's base mesh.
        all_pier_z_positions.append(set(base_pier_z_positions))
        base_pier_min_z_pos = base_pier_z_positions[0]
        base_pier_max_z_pos = base_pier_z_positions[-1]
        print_d(D, f"pier {p}. min, max = {base_pier_min_z_pos}, {base_pier_max_z_pos}")
        # And include z positions from the deck grid within the pier's range.
        assert_sorted(deck_positions[1])
        for deck_z_pos in deck_positions[1]:  # Index '1' are the z positions.
            if simple_mesh or not DECK_NODES_IN_PIER: break
            if base_pier_min_z_pos < deck_z_pos < base_pier_max_z_pos:
                all_pier_z_positions[-1].add(deck_z_pos)
        all_pier_z_positions[-1] = sorted(all_pier_z_positions[-1])
        assert_sorted(all_pier_z_positions[-1])
    return all_pier_z_positions



def get_x_positions_of_pier_bottom_nodes(c: Config) -> List[List[float]]:
    """A (length 1) list of the x position of the bottom nodes for each pier."""
    return [[support.x] for support in c.bridge.supports]


def get_z_positions_of_pier_bottom_nodes(
        c: Config, positions_deck: List[List[float]]
        ) -> List[List[float]]:
    """The z positions of bottom nodes of each pier's base mesh.

    This is achieved by interpolating the top nodes to the bottom, this works
    because the ratios of distances between nodes should remain equal.

    """
    all_z_positions = []
    # Iterate through each pier and apply the interpolation.
    for pier_positions_deck, pier in zip(positions_deck, c.bridge.supports):
        old_min = min(pier_positions_deck)
        old_max = max(pier_positions_deck)
        new_min = pier.z - (pier.width_bottom / 2)
        new_max = pier.z + (pier.width_bottom / 2)
        assert min(pier_positions_deck) == pier_positions_deck[0]
        assert max(pier_positions_deck) == pier_positions_deck[-1]
        all_z_positions.append(np.interp(
            pier_positions_deck, [old_min, old_max], [new_min, new_max]))
        assert_sorted(all_z_positions[-1])
    return list(map(round_m, all_z_positions))


def assert_support_nodes(c: Config, all_support_nodes: AllSupportNodes):
    """Sanity check that support nodes have the correct structure.

    TODO: Remove this function.

    """
    assert len(all_support_nodes) == len(c.bridge.supports)
    for s_nodes in all_support_nodes:
        assert len(s_nodes) == 2
        assert isinstance(s_nodes, tuple)
        for w_nodes in s_nodes:
            assert isinstance(w_nodes, list)
            assert isinstance(w_nodes[0], list)


def get_all_support_nodes(
        c: Config, deck_positions: DeckPositions, simple_mesh: bool
        ) -> AllSupportNodes:
    """All nodes for all a bridge's supports.

    If 'simple_mesh' is passed here, then nodes from bridge deck's mesh will be
    added to the pier's mesh.

    """
    nodes = []
    x_positions_deck = get_x_positions_of_pier_deck_nodes(c)
    z_positions_deck = get_z_positions_of_pier_deck_nodes(
        c=c, deck_positions=deck_positions, simple_mesh=simple_mesh)
    x_positions_bottom = get_x_positions_of_pier_bottom_nodes(c)
    # z_positions_bottom = get_base_mesh_z_positions_of_pier_bottom_nodes(c)
    z_positions_bottom = get_z_positions_of_pier_bottom_nodes(
        c, positions_deck=z_positions_deck)
    for i, support in enumerate(c.bridge.supports):
        walls = ([], [])
        nodes.append(walls)
        assert len(x_positions_deck[i]) == 2
        assert len(x_positions_bottom[i]) == 1
        x_bottom = x_positions_bottom[i][0]
        # For each wall of one support, starting with x at the deck.
        for w, x_deck in enumerate(x_positions_deck[i]):
            wall = walls[w]
            # For each transverse z position at the deck, we move down along
            # one transverse line updating x, y, z.
            for z, z_deck in enumerate(z_positions_deck[i]):
                ff_node_ids()
                z_bottom = z_positions_bottom[i][z]
                wall.append([])
                # Starting positions along this transverse line.
                x_pos = x_deck
                y_pos = 0  # Start at the top.
                z_pos = z_deck
                # Difference for each x, y, z as we move down the wall. Remember
                # that the walls may be tapered.
                x_diff = (x_bottom - x_deck) / (c.bridge.base_mesh_pier_nodes_y - 1)
                y_diff = -support.height / (c.bridge.base_mesh_pier_nodes_y - 1)
                z_diff = (z_bottom - z_deck) / (c.bridge.base_mesh_pier_nodes_y - 1)

                def append_wall_node(y):
                    """Append another node with current positions."""
                    wall[-1].append(get_node(
                        x=x_pos, y=y_pos, z=z_pos, pier=support,
                        support=support, comment_str=(
                            f"support {i + 1}{st(i + 1)} wall {w + 1}{st(w + 1)} z {z + 1} "
                            + f"y {y + 2}{st(y + 2)}")))

                # Append the first wall node for the current fixed z value then
                # iterate through the remaining nodes in y direction.
                append_wall_node(-1)
                for y in range(c.bridge.base_mesh_pier_nodes_y - 1):
                    x_pos += x_diff
                    y_pos += y_diff
                    z_pos += z_diff
                    append_wall_node(y)
    assert_support_nodes(c, nodes)
    return nodes


def opensees_support_nodes(
        c: Config, deck_nodes: DeckNodes, all_support_nodes: AllSupportNodes,
        simple_mesh: bool) -> str:
    """Opensees node commands for the supports (ignoring deck).

    By 'ignoring deck' we mean that nodes that belong to both supports and the
    deck will not be returned by this function but instead by
    'opensees_deck_nodes'.

    Args:
        c: Config, global configuration object.
        deck_nodes: DeckNodes, to check for already added support nodes.
        all_support_nodes: AllSupportNodes, all support nodes to generate
            commands for.

    """
    # We want to avoid generating commands for support nodes that also belong to
    # the deck, thus we create a set for fast indexing to allow this check.
    deck_nodes = set(chain.from_iterable(deck_nodes))
    nodes = OrderedDict()
    # For each support.
    for s_nodes in all_support_nodes:
        # For each wall of the support (there are two).
        for w_nodes in s_nodes:
            # For each ~vertical line of nodes for a z position at top of wall.
            for y_nodes in w_nodes:
                # For each node in the ~vertical line.
                for y, node in enumerate(y_nodes):
                    # Sanity check that all (and only these) of the pier's top
                    # nodes are part of the deck
                    if not simple_mesh:
                        assert (node in deck_nodes) == (y == 0)
                    # Insert the node, if not part of the deck nodes.
                    if node not in deck_nodes:
                        # A dictionary is used incase the node is already added,
                        # incase it is a bottom node shared by both walls.
                        nodes[node] = None
    return comment(
        "support nodes", "\n".join(map(lambda n: n.command_3d(), nodes.keys())),
        units="node nodeTag x y z")


def get_base_mesh_deck_positions(bridge: Bridge) -> DeckPositions:
    """The x and z positions of deck nodes in the base mesh."""
    x_positions, z_positions = [bridge.x_min], [bridge.z_min]
    x_step = bridge.length / (bridge.base_mesh_deck_nodes_x - 1)
    z_step = bridge.width / (bridge.base_mesh_deck_nodes_z - 1)
    for _ in range(bridge.base_mesh_deck_nodes_x - 1):
        x_positions.append(round_m(x_positions[-1] + x_step))
    for _ in range(bridge.base_mesh_deck_nodes_z - 1):
        z_positions.append(round_m(z_positions[-1] + z_step))
    return x_positions, z_positions


def get_pier_deck_positions(c: Config) -> DeckPositions:
    """The x and z positions of deck nodes that belong to piers."""
    return (
        sorted(chain.from_iterable(
            get_x_positions_of_pier_deck_nodes(c))),
        sorted(chain.from_iterable(
            get_base_mesh_z_positions_of_pier_deck_nodes(c))))


def get_load_deck_positions(
        bridge: Bridge, fem_params: SimParams) -> DeckPositions:
    """The x and z positions of deck nodes that belong to loads."""
    # TODO: Loading position for displacement control?
    return (
        [round_m(bridge.x(pload.x_frac)) for pload in fem_params.ploads],
        [round_m(bridge.z(pload.z_frac)) for pload in fem_params.ploads])


# The x and y deck positions after each stage of building.
DeckStagesInfo = NewType("DeckStagesInfo", Dict[str, DeckPositions])


def get_deck_positions(
        c: Config, fem_params: SimParams, simple_mesh: bool) -> DeckPositions:
    """The x and z positions of deck nodes.

    NOTE: This function will attach 'DeckStagesInfo' to the given 'FEMParams'
    under the attribute 'deck_stages_info.

    Args:
        c: Config, global configuration object.

    """
    # First collect positions from the base mesh.
    x_positions, z_positions = get_base_mesh_deck_positions(c.bridge)
    x_positions = set(map(round_m, x_positions))
    z_positions = set(map(round_m, z_positions))

    # Start creating the 'DeckStagesInfo', it is attached to the 'FEMParams'.
    deck_stages_info = OrderedDict([
        ("base", (deepcopy(x_positions), deepcopy(z_positions)))])
    fem_params.deck_stages_info = deck_stages_info

    # If requested, collect positions from piers.
    x_positions_piers, z_positions_piers = get_pier_deck_positions(c=c)
    assert_sorted(x_positions_piers); assert_sorted(z_positions_piers)
    if not simple_mesh:
        for x_pos in x_positions_piers:
            x_positions.add(round_m(x_pos))
        for z_pos in z_positions_piers:
            z_positions.add(round_m(z_pos))

    # Update the 'DeckStagesInfo' with pier information.
    deck_stages_info["piers"] = (deepcopy(x_positions), deepcopy(z_positions))

    # Collect loading positions.
    x_positions_loads, z_positions_loads = get_load_deck_positions(
        bridge=c.bridge, fem_params=fem_params)
    assert_sorted(x_positions_loads); assert_sorted(z_positions_loads)
    print_d(D, f"deck x positions from loads = {x_positions_loads})")
    print_d(D, f"deck z positions from loads = {z_positions_loads})")
    if not simple_mesh:
        for x_pos in x_positions_loads:
            print_d(D, f"load x pos already in x positions {x_pos in x_positions}")
            x_positions.add(round_m(x_pos))
        for z_pos in z_positions_loads:
            print_d(D, f"load z pos already in x positions {z_pos in z_positions}")
            z_positions.add(round_m(z_pos))

    # Update the 'DeckStagesInfo' with pier information.
    deck_stages_info["loads"] = (deepcopy(x_positions), deepcopy(z_positions))

    return sorted(x_positions), sorted(z_positions)


def print_mesh_info(
        bridge: Bridge, fem_params: SimParams, all_pier_nodes: AllSupportNodes):
    """Print information about the mesh after each stage of building."""
    to_lens = lambda x: np.array(list(map(len, x)))
    base = to_lens(fem_params.deck_stages_info["base"])
    piers = to_lens(fem_params.deck_stages_info["piers"])
    loads = to_lens(fem_params.deck_stages_info["loads"])

    loads -= piers
    piers -= base
    print_i(
        "Deck nodes (x * z)"
        + f"\n\tbase mesh  = {base[0]} * {base[1]}"
        + f"\n\tfrom piers = {piers[0]} * {piers[1]}"
        + f"\n\tfrom loads = {loads[0]} * {loads[1]}")

    num_pier_nodes_z, num_pier_nodes_y = [], []
    for pier_nodes in all_pier_nodes:
        for wall_nodes in pier_nodes:
            wall_shape = np.array(wall_nodes).shape
            num_pier_nodes_z.append(wall_shape[0])
            num_pier_nodes_y.append(wall_shape[1])
    base = [bridge.base_mesh_pier_nodes_y, bridge.base_mesh_pier_nodes_z]
    piers = np.array([np.mean(num_pier_nodes_y), np.mean(num_pier_nodes_z)])
    piers -= np.array(base)
    print_i(
        "Pier nodes (y * z)"
        + f"\n\tbase mesh  = {base[0]} * {base[1]}"
        + f"\n\tfrom piers = {piers[0]} * {piers[1]} (mean)")


def get_deck_nodes(
        c: Config, fem_params: SimParams, deck_positions: DeckPositions
        ) -> Tuple[str, List[List[Node]]]:
    """OpenSees nodes that belong to the bridge deck.

    The nodes are created based on given positions of deck nodes.

    Args:
        c: Config, global configuration object.

    """
    # Unpack x and z positions of nodes on the deck.
    x_positions, z_positions = deck_positions

    # Get positions of pier nodes on the deck.
    x_positions_piers, z_positions_piers = get_pier_deck_positions(c=c)

    def is_pier_node(x_: float, z_: float):
        """Is a deck node from a pier?"""
        return (x_ in x_positions_piers and z_ in z_positions_piers)

    set_ff_mod(len(x_positions))
    nodes = []
    for z_pos in z_positions:
        # Fast forward node IDs when we move to a new z position.
        ff_node_ids()
        nodes.append([])
        for x_pos in x_positions:
            comment_str = (
                "support node" if is_pier_node(x_=x_pos, z_=z_pos)
                else None)
            nodes[-1].append(get_node(
                x=x_pos, y=0, z=z_pos, deck=True, comment_str=comment_str))
    return nodes


def opensees_deck_nodes(
        c: Config, fem_params: SimParams, deck_positions: DeckPositions
        ) -> Tuple[str, List[List[Node]]]:
    """OpenSees node commands for a bridge deck.

    The nodes are created based on given positions of deck nodes.

    Args:
        c: Config, global configuratin object.

    """
    deck_nodes = get_deck_nodes(
        c=c, fem_params=fem_params, deck_positions=deck_positions)
    node_strings = []
    node_strings += list(map(
        lambda node: node.command_3d(),
        list(chain.from_iterable(deck_nodes))))
    return (comment(
            "deck nodes", "\n".join(node_strings), units="node nodeTag x y z"),
        deck_nodes)


##### End nodes #####
##### Begin fixed nodes #####


class FixNode:
    """A command to fix a node in some degrees of freedom (dof).

    Args:
        node: Node, the node with dof to fix specified.
        comment_: Optional[str], an optional comment for the command.

    """
    def __init__(
            self, node: Node, free_y: bool = False,
            comment: Optional[str] = None):
        self.node = node
        self.free_y = free_y
        self.comment = comment

    def command_3d(self):
        """The command in string format for a TCL file."""
        # TODO: Update comment to include support ID.
        comment_ = "" if self.comment is None else f"; # {self.comment}"
        if self.node.support is None:
            return f"fix {self.node.n_id} 1 1 1 0 0 0{comment_}"
        else:
            # print(f"******************")
            # print(f"Fixed support node")
            y_trans_fix = self.node.support.fix_y_translation
            if self.free_y:
                y_trans_fix = False
            return (
                f"fix {self.node.n_id}"
                + f" {int(self.node.support.fix_x_translation)}"
                + f" {int(y_trans_fix)}"
                + f" {int(self.node.support.fix_z_translation)}"
                + f" {int(self.node.support.fix_x_rotation)}"
                + f" {int(self.node.support.fix_y_rotation)}"
                + f" {int(self.node.support.fix_z_rotation)}"
                + f"{comment_}")


def opensees_fixed_deck_nodes(c: Config, deck_nodes: DeckNodes) -> str:
    """OpenSees fix commands for fixed deck nodes."""
    fixed_nodes: List[FixNode] = []
    for x_nodes in deck_nodes:
        assert len(x_nodes) >= 2
        fixed_nodes.append(FixNode(x_nodes[0]))
        fixed_nodes.append(FixNode(x_nodes[-1]))
    return comment(
        "fixed deck nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz")


def opensees_fixed_pier_nodes(
        c: Config, all_support_nodes: AllSupportNodes,
        pier_disp: Optional[DisplacementCtrl] = None) -> str:
    """OpenSees fix commands for fixed support nodes."""
    fixed_nodes: List[FixNode] = []
    # Iterate through each pier. Note that p_nodes is a tuple of nodes for each
    # pier wall. And each wall is a 2-d array of nodes.
    for p, p_nodes in enumerate(all_support_nodes):
        # If pier displacement for this pier then select the bottom central node
        # for the integrator command, and attach it to the pier.
        free_y = False
        if (pier_disp is not None) and (p == pier_disp.pier):
            free_y = True
            pier = c.bridge.supports[pier_disp.pier]
            pier.disp_node = p_nodes[0][len(p_nodes[0]) // 2][-1]
            if len(p_nodes[0]) % 2 == 0:
                raise ValueError(
                    "Pier displacement requires odd number of nodes along pier"
                    " in the transverse direction")
        # For each ~vertical line of nodes for a z position at top of wall.
        for y, y_nodes in enumerate(p_nodes[0]):
            # We will fix the bottom node.
            fixed_nodes.append(FixNode(
                node=y_nodes[-1], free_y=free_y,
                comment=f"support {p+1} y {y+1}"))
    return comment(
        "fixed support nodes",
        "\n".join(map(lambda f: f.command_3d(), fixed_nodes)),
        units="fix nodeTag x y z rx ry rz")


##### End fixed nodes #####
##### Begin sections #####


def opensees_section(section: Section3D):
    """OpenSees ElasticMembranePlateSection command for a Section3D."""
    return (
        f"section ElasticMembranePlateSection {section.id}"
        + f" {section.youngs * 1E6} {section.poissons} {section.thickness}"
        + f" {section.density * 1E-3}")


def opensees_deck_sections(c: Config):
    """Sections used in the bridge deck."""
    return comment(
        "deck sections", "\n".join([
            opensees_section(section) for section in c.bridge.sections]),
        units=(
            "section ElasticMembranePlateSection secTag youngs_modulus"
            + " poisson_ratio depth mass_density"))


def opensees_pier_sections(c: Config):
    """Sections used in the bridge's piers."""
    # Some pier's may refer to the same section so we create a set to avoid
    # rendering duplicate section definitions into the .tcl file.
    pier_sections = set()
    for pier in c.bridge.supports:
        for section in pier.sections:
            pier_sections.add(section)
    return comment(
        "pier sections", "\n".join([
            opensees_section(section) for section in pier_sections]),
        units=(
            "section ElasticMembranePlateSection secTag youngs_modulus"
            + " poisson_ratio depth mass_density"))


def section_for_deck_element(
        c: Config, element_x: float, element_z: float) -> int:
    """Section for a shell element on the deck.

    Creates a list (if not already created) of all section's x positions to z
    position to Section3D. Then iterate through sorted x positions finding last
    one less than or equal to the given element's lowest x position, then do the
    same for the z position, then the section is found.

    Args:
        c: Config, global configuration object.
        element_x: float, x position which belongs in some section.
        element_z: float, z position which belongs in some section.

    """
    # Create the dictionary if not already created.
    if not hasattr(c.bridge, "deck_sections_dict"):
        c.bridge.deck_sections_dict = defaultdict(dict)
        for section in c.bridge.sections:
            c.bridge.deck_sections_dict[
                round_m(c.bridge.x(section.start_x_frac))][
                    round_m(c.bridge.z(section.start_z_frac))] = section

    # print(sorted(c.bridge.deck_sections_dict.keys()))
    # print(sorted(c.bridge.deck_sections_dict[0.0].keys()))

    element_x, element_z = round_m(element_x), round_m(element_z)
    # Find the last x position less than element_x.
    section_x = None
    for next_section_x in sorted(c.bridge.deck_sections_dict.keys()):
        if next_section_x <= element_x:
            section_x = next_section_x
        else:
            break
    # print(f"section_x = {section_x}")

    # Find the last z position less than element_z.
    section_z = None
    for next_section_z in sorted(c.bridge.deck_sections_dict[section_x].keys()):
        if next_section_z <= element_z:
            section_z = next_section_z
        else:
            break
        # print(f"next_section_z = {next_section_z}")
    # print(f"section_z = {section_z}")

    return c.bridge.deck_sections_dict[section_x][section_z]


def section_for_pier_element(
        c: Config, pier: Support3D, element_start_frac_len: float) -> int:
    """Section for a shell element on a pier.

    Args:
        c: Config, global configuration object.
        pier: Support3DPier, the pier from which to select a section.
        element_start_frac_len: float, fraction of pier wall length.

    """
    # Find the last section of a pier where the fraction of the pier wall's
    # length is less than element_start_frac_len.
    section = None
    for next_section in sorted(pier.sections, key=lambda s: s.start_frac_len):
        if next_section.start_frac_len <= element_start_frac_len:
            section = next_section
        else:
            break
    return section


##### End sections #####
##### Begin shell elements #####


def get_deck_elements(c: Config, deck_nodes: DeckNodes) -> DeckElements:
    """Shell elements that make up a bridge deck."""

    first_node_z_0 = deck_nodes[0][0].n_id
    first_node_z_1 = deck_nodes[-1][0].n_id
    last_node_z_0 = deck_nodes[0][-1].n_id
    z_skip = deck_nodes[1][0].n_id - deck_nodes[0][0].n_id
    # print_d(D, f"first_node_z_0 = {first_node_z_0}")
    # print_d(D, f"first_node_z_1 = {first_node_z_1}")
    # print_d(D, f"last_node_z_0 = {last_node_z_0}")
    # print_d(D, f"z_skip = {z_skip}")

    deck_elements = []  # The result.
    # Shell nodes are input in counter-clockwise order starting bottom left
    # with i, then bottom right with j, top right k, top left with l.

    # From first until second last node along z (when x == 0).
    for z_node in range(first_node_z_0, first_node_z_1, z_skip):
        deck_elements.append([])
        # print_d(D, f"deck element z_node = {z_node}")
        # Count from first node at 0 until second last node along x.
        for x_node in range(last_node_z_0 - first_node_z_0):
            # print_d(D, f"deck element x_node = {x_node}")
            # i is the bottom left node, j the bottom right, k the top right
            # and l the top left.
            i_node, j_node = z_node + x_node, z_node + x_node + 1
            k_node, l_node = j_node + z_skip, i_node + z_skip
            # print_d(D, f"i, j, k, l = {i_node}, {j_node}, {k_node}, {l_node}")
            section = section_for_deck_element(
                c=c, element_x=nodes_by_id[i_node].x,
                element_z=nodes_by_id[i_node].z)
            deck_elements[-1].append(ShellElement(
                e_id=next_elem_id(), ni_id=i_node, nj_id=j_node, nk_id=k_node,
                nl_id=l_node, section=section, pier=False,
                nodes_by_id=nodes_by_id))
        ff_elem_ids(z_skip)
    return deck_elements


def opensees_deck_elements(c: Config, deck_elements: DeckElements) -> str:
    """OpenSees element commands for a bridge deck."""
    deck_elements = chain.from_iterable(deck_elements)
    return comment(
        "deck shell elements",
        "\n".join(map(lambda e: e.command_3d(), deck_elements)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag")


def get_pier_elements(
        c: Config, all_support_nodes: AllSupportNodes) -> AllPierElements:
    """Shell elements that make up a bridge's piers."""
    pier_elements = []  # The result.
    for s, support_nodes in enumerate(all_support_nodes):
        for w, wall_nodes in enumerate(support_nodes):
            z = 0  # Keep an index of current transverse (z) line.
            # For each pair of (line of nodes in y direction).
            for y_nodes_z_lo, y_nodes_z_hi in zip(
                    wall_nodes[:-1], wall_nodes[1:]):
                assert len(y_nodes_z_lo) == len(y_nodes_z_hi)
                # For each element (so for each node - 1) on the line of nodes
                # in y direction.
                for y in range(len(y_nodes_z_lo) - 1):
                    y_lo_z_lo: Node = y_nodes_z_lo[y]
                    y_hi_z_lo: Node = y_nodes_z_lo[y + 1]
                    y_lo_z_hi: Node = y_nodes_z_hi[y]
                    y_hi_z_hi: Node = y_nodes_z_hi[y + 1]
                    assert isinstance(y_lo_z_lo, Node)
                    for other_node in [y_hi_z_lo, y_lo_z_hi, y_hi_z_hi]:
                        assert other_node.y <= y_lo_z_lo.y
                    assert y_lo_z_lo.z < y_lo_z_hi.z
                    assert y_hi_z_lo.z < y_hi_z_hi.z
                    # print(f"Section ID ={s}")
                    # The reason we do "- 2" is because: if len(y_nodes_z_lo) is
                    # 5 then the max value of range(len(y_nodes_z_lo) - 1) is 3.
                    element_start_frac_len = y / (len(y_nodes_z_lo) - 2)
                    # print(f"y = {y}, len nodes = {len(y_nodes_z_lo)}, element_start_frac = {element_start_frac_len}")
                    section = section_for_pier_element(
                        c=c, pier=c.bridge.supports[s],
                        element_start_frac_len=element_start_frac_len)
                    pier_elements.append(ShellElement(
                        e_id=next_elem_id(), ni_id=y_lo_z_lo.n_id,
                        nj_id=y_hi_z_lo.n_id, nk_id=y_hi_z_hi.n_id,
                        nl_id=y_lo_z_hi.n_id, section=section, pier=True,
                        nodes_by_id=nodes_by_id,
                        support_position_index=(s, w, z, y)))
                ff_elem_ids(ff_mod)
                z += 1
    return pier_elements


def opensees_pier_elements(c: Config, all_pier_elements: AllPierElements) -> str:
    """OpenSees element commands for a bridge's piers."""
    return comment(
        "pier shell elements",
        "\n".join(map(lambda e: e.command_3d(), all_pier_elements)),
        units="element ShellMITC4 eleTag iNode jNode kNode lNode secTag")


##### End shell elements #####
##### Begin loads #####


def opensees_load(
        c: Config, pload: PointLoad, deck_nodes: DeckNodes, simple_mesh: bool,
        pier_disp: Optional[DisplacementCtrl] = None):
    """An OpenSees load command."""
    pload_z = c.bridge.z(z_frac=pload.z_frac)
    pload_x = c.bridge.x(x_frac=pload.x_frac)
    assert deck_nodes[0][0].y == 0
    assert deck_nodes[-1][-1].y == 0
    best_node = sorted(
        chain.from_iterable(deck_nodes),
        key=lambda node: node.distance(x=pload_x, y=0, z=pload_z))[0]

    if pier_disp is not None:
        pier = c.bridge.supports[pier_disp.pier]
        print_w(
            f"Distance of pier (under displacement) center to deck node"
            + f" {best_node.distance(x=pier.x, y=0, z=pier.z):.4f}m")

    assert np.isclose(best_node.y, 0)
    # If we have a proper mesh then this should be the exact node.
    if not simple_mesh:
        assert np.isclose(best_node.x, pload_x)
        assert np.isclose(best_node.z, pload_z)

    return f"load {best_node.n_id} 0 {pload.kn * 1000} 0 0 0 0"


def opensees_loads(
        c: Config, ploads: List[PointLoad], deck_nodes: DeckNodes,
        simple_mesh: bool, pier_disp: Optional[DisplacementCtrl]):
    """OpenSees load commands for a .tcl file."""
    # In case of pier displacement apply load at the pier's central bottom node,
    # the load intensity doesn't matter though, only the position matters.
    if pier_disp is not None:
        node = c.bridge.supports[pier_disp.pier].disp_node
        load_str = f"load {node.n_id} 0 {c.pd_unit_load_kn * 1000} 0 0 0 0"
    # Otherwise find the deck nodes which best suit given point loads.
    else:
        load_str = "\n".join(
            opensees_load(
                c=c, pload=pload, deck_nodes=deck_nodes,
                simple_mesh=simple_mesh, pier_disp=pier_disp)
            for pload in ploads)

    return comment(
        "loads", load_str,
        units="load nodeTag N_x N_y N_z N_rx N_ry N_rz")


##### End loads #####
##### Begin recorders #####


def opensees_translation_recorders(
        c: Config, fem_params: SimParams, os_runner: "OSRunner") -> str:
    """OpenSees recorder commands for translation."""
    deck_nodes = fem_params.deck_nodes
    all_support_nodes = fem_params.all_support_nodes

    # A list of tuples of ResponseType and OpenSees direction index, for
    # translation response types, if requested in fem_params.response_types.
    translation_response_types = []
    if ResponseType.XTranslation in fem_params.response_types:
        x_path = os_runner.x_translation_path(fem_params)
        translation_response_types.append((x_path, 1))
        print_i(f"OpenSees: saving x translation at {x_path}")
    if ResponseType.YTranslation in fem_params.response_types:
        y_path = os_runner.y_translation_path(fem_params)
        translation_response_types.append((y_path, 2))
        print_i(f"OpenSees: saving y translation at {y_path}")
    if ResponseType.ZTranslation in fem_params.response_types:
        z_path = os_runner.z_translation_path(fem_params)
        translation_response_types.append((z_path, 3))
        print_i(f"OpenSees: saving z translation at {z_path}")

    # Append a recorder string for each response type (recording nodes).
    recorder_strs = []
    node_str = " ".join(
        str(n.n_id) for n in bridge_3d_nodes(
            deck_nodes=deck_nodes, all_support_nodes=all_support_nodes))
    for response_path, direction in translation_response_types:
        print(response_path)
        import sys; sys.exit();
        print_d(D, f"Adding response path to build: {response_path}")
        recorder_strs.append(
            f"recorder Node -file {response_path} -node {node_str} -dof"
            + f" {direction} disp")
    return comment(
        "translation recorders", "\n".join(recorder_strs),
        units="recorder Node -file path -node nodeTags -dof direction disp")


def opensees_stress_recorder(
        c: Config, fem_params: SimParams, os_runner: "OSRunner") -> str:
    """OpenSees recorder command for stresses."""
    all_elements = bridge_3d_elements(
        deck_elements=fem_params.deck_elements,
        all_pier_elements=fem_params.all_pier_elements)
    ele_str = " ".join(str(e.e_id) for e in all_elements)
    recorder_str = (
        f"recorder Element -file test.out -ele {ele_str} stresses")
    return comment("element recorders", recorder_str, units="TODO units")


def opensees_recorders(
        c: Config, fem_params: SimParams, os_runner: "OSRunner"):
    """OpenSees recorder commands for translation and stresses."""
    return "\n".join([
        opensees_translation_recorders(
            c=c, fem_params=fem_params, os_runner=os_runner),
        opensees_stress_recorder(
            c=c, fem_params=fem_params, os_runner=os_runner)])


def opensees_integrator(c: Config, pier_disp: Optional[DisplacementCtrl]):
    """The integrator command to use based on FEMParams."""
    if pier_disp is None:
        return "integrator LoadControl 1"
    node = c.bridge.supports[pier_disp.pier].disp_node
    return (f"integrator DisplacementControl {node.n_id} 2"
        + f" {pier_disp.displacement}")


def opensees_algorithm(pier_disp: Optional[DisplacementCtrl]):
    """The algorithm command to use based on FEMParams."""
    if pier_disp is None:
        return "algorithm Linear"
    return "algorithm Newton"


def opensees_test(pier_disp: Optional[DisplacementCtrl]):
    """The test command to use based on FEMParams."""
    if pier_disp is None:
        return ""
    return "test NormDispIncr 1.0e-12 1000"


##### End recorders #####


def assert_deck_in_pier_pier_in_deck(
        deck_nodes: DeckNodes, all_pier_nodes: AllSupportNodes):
    """The number of top nodes per pier must equal that range in the mesh."""
    # First create a list of deck nodes sorted by x then z position.
    sorted_deck_nodes = sorted(
        chain.from_iterable(deck_nodes), key=lambda n: (n.x, n.z))
    for pier_nodes in all_pier_nodes:
        for wall_nodes in pier_nodes:
            # Get the top line of nodes of the wall and assert we got them
            # correctly.
            wall_top_nodes = list(map(lambda ys: ys[0], wall_nodes))
            for z, node in enumerate(wall_top_nodes):
                assert node.y > wall_nodes[z][1].y
            x = wall_top_nodes[0].x
            for x_index in range(1, len(wall_top_nodes)):
                assert x == wall_top_nodes[x_index].x
            # Find the deck nodes with the correct x position and range of z.
            min_z = wall_top_nodes[0].z
            max_z = wall_top_nodes[-1].z
            deck_in_range = len(list(
                n for n in sorted_deck_nodes
                if n.x == x and n.z >= min_z and n.z <= max_z))
            assert deck_in_range == len(wall_top_nodes)


def build_model_3d(
        c: Config, expt_params: ExptParams, os_runner: "OSRunner",
        simple_mesh: bool = False):
    """Build OpenSees 3D model files.

    Args:
        c: Config, global configuration object.
        simple_mesh: bool, whether meshes for deck and for piers are based on
            simple grids of nodes without any refinement, for testing.

    """
    # Read in the template model file.
    with open(c.os_3d_model_template_path) as f:
        in_tcl = f.read()

    # Build a model file for each simulation.
    for fem_params in expt_params.sim_params:

        # Reset before building.
        reset_nodes()
        reset_elem_ids()

        # Displacement control is not supported yet in 3D.
        if fem_params.displacement_ctrl is not None:
            print("OpenSees: Displacement not supported in 3D")

        # Calculate nodes for the bridge deck and piers.
        deck_positions = get_deck_positions(
            c=c, fem_params=fem_params, simple_mesh=simple_mesh)
        deck_nodes_str, deck_nodes = opensees_deck_nodes(
            c=c, fem_params=fem_params, deck_positions=deck_positions)
        all_support_nodes = get_all_support_nodes(
            c, deck_positions=deck_positions, simple_mesh=simple_mesh)
        assert_support_nodes(c=c, all_support_nodes=all_support_nodes)

        # Print info on, and assert the generated mesh.
        print_mesh_info(
            bridge=c.bridge, fem_params=fem_params,
            all_pier_nodes=all_support_nodes)
        if not simple_mesh:
            assert_deck_in_pier_pier_in_deck(
                deck_nodes=deck_nodes, all_pier_nodes=all_support_nodes)

        # Attach deck and pier nodes and elements to the FEMParams to be
        # available when converting raw responses to responses with positions
        # attached.
        #
        # NOTE: there is some overlap between deck nodes and pier nodes, and
        # some over lap between nodes of both walls of one pier (at the bottom
        # where they meet).
        fem_params.deck_nodes = deck_nodes
        fem_params.all_support_nodes = all_support_nodes
        fem_params.deck_elements = get_deck_elements(c=c, deck_nodes=deck_nodes)
        fem_params.all_pier_elements = get_pier_elements(
            c=c, all_support_nodes=all_support_nodes)

        # Build the 3D model file by replacing each placeholder in the model
        # template file with OpenSees commands.
        out_tcl = (
            in_tcl
            .replace("<<INTRO>>", opensees_intro)
            .replace("<<DECK_NODES>>", deck_nodes_str)
            .replace("<<SUPPORT_NODES>>", opensees_support_nodes(
                c=c, deck_nodes=deck_nodes,
                all_support_nodes=all_support_nodes, simple_mesh=simple_mesh))
            .replace("<<FIX_DECK>>", opensees_fixed_deck_nodes(
                c=c, deck_nodes=deck_nodes))
            .replace("<<FIX_SUPPORTS>>", opensees_fixed_pier_nodes(
                c=c, all_support_nodes=all_support_nodes,
                pier_disp=fem_params.displacement_ctrl))
            .replace("<<LOAD>>", opensees_loads(
                c=c, ploads=fem_params.ploads, deck_nodes=deck_nodes,
                simple_mesh=simple_mesh, pier_disp=fem_params.displacement_ctrl))
            .replace("<<SUPPORTS>>", "")
            .replace("<<DECK_SECTIONS>>", opensees_deck_sections(c=c))
            .replace("<<PIER_SECTIONS>>", opensees_pier_sections(c=c))
            .replace("<<RECORDERS>>", opensees_recorders(
                c=c, fem_params=fem_params, os_runner=os_runner))
            .replace("<<DECK_ELEMENTS>>", opensees_deck_elements(
                c=c, deck_elements=fem_params.deck_elements))
            .replace("<<PIER_ELEMENTS>>", opensees_pier_elements(
                c=c, all_pier_elements=fem_params.all_pier_elements))
            .replace("<<INTEGRATOR>>", opensees_integrator(
                c=c, pier_disp=fem_params.displacement_ctrl))
            .replace("<<ALGORITHM>>", opensees_algorithm(
                fem_params.displacement_ctrl))
            .replace("<<TEST>>", opensees_test(fem_params.displacement_ctrl)))

        # Write the generated model file.
        model_path = os_runner.fem_file_path(fem_params=fem_params, ext="tcl")
        with open(model_path, "w") as f:
            f.write(out_tcl)
        print_i(f"OpenSees: saved 3D model file to {model_path}")

    print(len(list(nodes_by_id.values())))
    return expt_params
