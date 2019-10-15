"""Build OpenSees 3D model files."""
import itertools
import math
from collections import OrderedDict, defaultdict
from typing import List, Optional, Tuple

import numpy as np

from config import Config
from fem.params import ExptParams, FEMParams
from fem.run.opensees.common import AllPierElements, AllSupportNodes, DeckElements, DeckNodes, Node, ShellElement, bridge_3d_elements, bridge_3d_nodes, num_deck_nodes
from model.bridge import Section3D, Support3D
from model.load import PointLoad
from model.response import ResponseType
from util import round_m, print_d, print_i, print_w

# Print debug information for this file.
D: str = "fem.run.opensees.build.d3"
# D: bool = False

# The letters that come after a number e.g. in 1st, 2nd, 3rd.
st = lambda n: "%s" % ("tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

##### Begin node factory #####

# A dictionary of x position to y position to z position to Node.
all_nodes = defaultdict(lambda: defaultdict(dict))

# A dictionary of Node ID to Node.
nodes_by_id = dict()


def get_node(
        x: float, y: float, z: float, comment_str: Optional[str] = None,
        support: Optional[Support3D] = None):
    """Get a node if it already exists, else create and return.

    NOTE: Use this to contruct Nodes, don't do it directly!

    """
    x = round_m(x)
    y = round_m(y)
    z = round_m(z)
    if z not in all_nodes[x][y]:
        new_node = Node(
            n_id=next_node_id(), x=x, y=y, z=z, comment=comment_str,
            support=support)
        all_nodes[x][y][z] = new_node
        nodes_by_id[new_node.n_id] = new_node
    return all_nodes[x][y][z]


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
    nodes_by_id = dict()


reset_nodes()


# Amount to fast forward Node IDs by.
ff_mod = None


def ff_node_ids(mod: int):
    """Fast forward node IDs until divisible by "mod"."""
    global _node_id
    while _node_id % mod != 0:
        _node_id += 1


def next_pow_10(n: int):
    """Power of 10 greater than n."""
    pow_10 = 1
    while pow_10 <= n:
        pow_10 = pow_10 * 10
    return pow_10


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


def x_positions_of_deck_support_nodes(c: Config) -> List[float]:
    """A list of sorted x positions where the supports have deck nodes.

    TODO: There is loss of information in the returned type (sortof), should be
        List[List[float]], a list of length 2 for each support.

    """
    x_positions = []
    for support in c.bridge.supports:
        x_positions.append([])
        support_half_length = support.length / 2
        x_positions[-1].append(round_m(support.x - support_half_length))
        x_positions[-1].append(round_m(support.x + support_half_length))
    return x_positions


def z_positions_of_deck_support_nodes(c: Config) -> List[List[float]]:
    """A list of sorted z positions where each support has deck nodes."""
    z_positions = []
    for support in c.bridge.supports:
        z_positions.append([])
        z_0 = support.z - (support.width_top / 2)
        z_positions[-1].append(round_m(z_0))
        z_step = support.width_top / (c.os_support_num_nodes_z - 1)
        for _ in range(c.os_support_num_nodes_z - 1):
            z_0 += z_step
            z_positions[-1].append(round_m(z_0))
    return z_positions


def x_positions_of_bottom_support_nodes(c: Config) -> List[List[float]]:
    """A list of sorted x positions of the bottom nodes for each support."""
    return [[support.x] for support in c.bridge.supports]


def z_positions_of_bottom_support_nodes(c: Config) -> List[List[float]]:
    """A list of sorted z positions of the bottom nodes for each support."""
    z_positions = []
    for support in c.bridge.supports:
        z_positions.append([])
        z_0 = support.z - (support.width_bottom / 2)
        # print_w(f"support_z = {support.z}")
        z_positions[-1].append(round_m(z_0))
        z_step = support.width_bottom / (c.os_support_num_nodes_z - 1)
        for _ in range(c.os_support_num_nodes_z - 1):
            z_0 += z_step
            z_positions[-1].append(round_m(z_0))
    return z_positions


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


def get_all_support_nodes(c: Config) -> AllSupportNodes:
    """All nodes for all a bridge's supports."""
    nodes = []
    x_positions_deck = x_positions_of_deck_support_nodes(c)
    z_positions_deck = z_positions_of_deck_support_nodes(c)
    x_positions_bottom = x_positions_of_bottom_support_nodes(c)
    z_positions_bottom = z_positions_of_bottom_support_nodes(c)
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
                ff_node_ids(ff_mod)
                z_bottom = z_positions_bottom[i][z]
                wall.append([])
                # Starting positions along this transverse line.
                x_pos = x_deck
                y_pos = 0  # Start at the top.
                z_pos = z_deck
                # Determine difference for each x, y, z as we move down the wall.
                x_diff = (x_bottom - x_deck) / (c.os_support_num_nodes_y - 1)
                y_diff = -support.height / (c.os_support_num_nodes_y - 1)
                z_diff = (z_bottom - z_deck) / (c.os_support_num_nodes_y - 1)

                def append_wall_node(y):
                    """Append another node with current positions."""
                    wall[-1].append(get_node(
                        x=x_pos, y=y_pos, z=z_pos, support=support,
                        comment_str=(
                            f"support {i + 1}{st(i + 1)} wall {w + 1}{st(w + 1)} z {z + 1} "
                            + f"y {y + 2}{st(y + 2)}")))

                # Append the first wall node for the current fixed z value then
                # iterate through the remaining nodes in y direction.
                append_wall_node(-1)
                for y in range(c.os_support_num_nodes_y - 1):
                    x_pos += x_diff
                    y_pos += y_diff
                    z_pos += z_diff
                    append_wall_node(y)
    assert_support_nodes(c, nodes)
    return nodes


def opensees_support_nodes(
        c: Config, deck_nodes: DeckNodes, all_support_nodes: AllSupportNodes
        ) -> str:
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
    deck_nodes = set(itertools.chain.from_iterable(deck_nodes))
    nodes = OrderedDict()
    # For each support.
    for s_nodes in all_support_nodes:
        # For each wall of the support (there are two).
        for w_nodes in s_nodes:
            # For each ~vertical line of nodes for a z position at top of wall.
            for y_nodes in w_nodes:
                # For each nde in the ~vertical line.
                for node in y_nodes:
                    # Insert the node, if not part of the deck nodes.
                    if node not in deck_nodes:
                        # A dictionary is used incase the node is already added,
                        # incase it is a bottom node shared by both walls.
                        nodes[node] = None
    return comment(
        "support nodes", "\n".join(map(lambda n: n.command_3d(), nodes.keys())),
        units="node nodeTag x y z")


def get_deck_nodes(
        c: Config, include_support_nodes: bool) -> Tuple[str, List[List[Node]]]:
    """OpenSees nodes that belong to the bridge deck.

    Args:
        c: Config, global configuration object.
        include_support_nodes: bool, for testing, if False don't include the
            nodes for the supports.

    """
    # First collect all z and x positions.
    z_positions = set()
    x_positions = set()
    # Collect positions of deck nodes without deck support nodes.
    z_pos = c.bridge.z_min
    z_positions.add(z_pos)
    num_deck_nodes_x, num_deck_nodes_z = num_deck_nodes(c)
    for num_z in range(num_deck_nodes_z - 1):
        z_pos += c.os_node_step_z
        z_positions.add(z_pos)
        x_pos = c.bridge.x_min
        x_positions.add(x_pos)
        for num_x in range(num_deck_nodes_x - 1):
            x_pos += c.os_node_step
            x_positions.add(x_pos)
    # If necessary add positions of deck support nodes.
    x_positions_supports, z_positions_supports = None, None
    if include_support_nodes:
        # z positions of deck nodes that are also supports.
        z_positions_supports = list(itertools.chain.from_iterable(
            z_positions_of_deck_support_nodes(c)))
        # Add these support z positions to the deck z positions.
        for z_pos in z_positions_supports:
            z_positions.add(z_pos)
        # x positions of deck nodes that are also supports.
        x_positions_supports = list(itertools.chain.from_iterable(
            x_positions_of_deck_support_nodes(c)))
        # Add these support x positions to the deck z positions.
        for x_pos in x_positions_supports:
            x_positions.add(x_pos)
    x_positions = sorted(list(x_positions))
    z_positions = sorted(list(z_positions))


    def is_support_node(x_: float, z_: float):
        """Is a node's position that of one of the support nodes?"""
        return (
            x_positions_supports is not None
            and z_positions_supports is not None
            and x_ in x_positions_supports
            and z_ in z_positions_supports)


    global ff_mod
    ff_mod = next_pow_10(len(x_positions))
    nodes = []
    for z_pos in z_positions:
        # Fast forward node IDs on each transverse (z) increment.
        ff_node_ids(ff_mod)
        nodes.append([])
        for x_pos in x_positions:
            # If the deck node also belongs to a support then add a comment.
            comment_str = (
                "support node" if is_support_node(x_=x_pos, z_=z_pos)
                else None)
            nodes[-1].append(get_node(
                x=x_pos, y=0, z=z_pos, comment_str=comment_str))
    return nodes


def opensees_deck_nodes(
        c: Config, include_support_nodes: bool) -> Tuple[str, List[List[Node]]]:
    """OpenSees node commands for a bridge deck.

    Args:
        c: Config, global configuratin object.
        include_support_nodes: bool, for testing, if False don't include the
            nodes for the supports.

    """
    deck_nodes = get_deck_nodes(
        c=c, include_support_nodes=include_support_nodes)
    node_strings = []
    node_strings += list(map(
        lambda node: node.command_3d(),
        list(itertools.chain.from_iterable(deck_nodes))))
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
    def __init__(self, node: Node, comment_: Optional[str] = None):
        self.node = node
        self.comment = comment_

    def command_3d(self):
        """The command in string format for a TCL file."""
        # TODO: Update comment to include support ID.
        comment_ = "" if self.comment is None else f"; # {self.comment}"
        if self.node.support is None:
            return f"fix {self.node.n_id} 1 1 1 0 0 0{comment_}"
        else:
            # print(f"******************")
            # print(f"Fixed support node")
            return (
                f"fix {self.node.n_id}"
                + f" {int(self.node.support.fix_x_translation)}"
                + f" {int(self.node.support.fix_y_translation)}"
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


def opensees_fixed_support_nodes(
        c: Config, all_support_nodes: AllSupportNodes) -> str:
    """OpenSees fix commands for fixed support nodes."""
    fixed_nodes: List[FixNode] = []
    # For each support.
    for s, s_nodes in enumerate(all_support_nodes):
        # For each ~vertical line of nodes for a z position at top of wall.
        for z, z_nodes in enumerate(s_nodes[0]):  
            # We will fix the bottom node.
            fixed_nodes.append(FixNode(
                node=z_nodes[-1], comment_=f"support {s+1} z {z+1}"))
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
            +" poisson_ratio depth mass_density"))


def section_for_deck_element(
        c: Config, element_x: float, element_z: float) -> int:
    """Section for a shell element on the deck.

    Creates a dictionary (if not already created) of all section's x positions
    to z position to Section3D. Then iterate through sorted x positions finding
    last one less than or equal to the given element's lowest x position, then
    do the same for the z position, then the section is found. The element is
    given as List[Nodes], from which the lowest x and z position's are found.

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
                c.bridge.x(section.start_x_frac)][
                c.bridge.z(section.start_z_frac)] = section

    # Find the last x position less than element_x.
    section_x = None
    for next_section_x in sorted(c.bridge.deck_sections_dict.keys()):
        # print(f"next_section_x = {next_section_x}")
        if next_section_x > element_x:
            break
        section_x = next_section_x
    # print(f"section_x = {section_x}")

    # Find the last z position less than element_z.
    section_z = None
    for next_section_z in sorted(
            c.bridge.deck_sections_dict[section_x].keys()):
        # print(f"next_section_z = {next_section_z}")
        if next_section_z > element_z:
            break
        section_z = next_section_z
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
        if next_section.start_frac_len > element_start_frac_len:
            return section
        section = next_section
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
            i_node = z_node + x_node
            j_node = i_node + 1
            k_node, l_node = j_node + z_skip, i_node + z_skip
            # print_d(D, f"i, j, k, l = {i_node}, {j_node}, {k_node}, {l_node}")
            section = section_for_deck_element(
                c=c, element_x=nodes_by_id[i_node].x,
                element_z=nodes_by_id[i_node].z)
            deck_elements[-1].append(ShellElement(
                e_id=next_elem_id(), ni_id=i_node, nj_id=j_node, nk_id=k_node,
                nl_id=l_node, section=section))
        ff_elem_ids(z_skip)
    return deck_elements


def opensees_deck_elements(c: Config, deck_elements: DeckElements) -> str:
    """OpenSees element commands for a bridge deck."""
    deck_elements = itertools.chain.from_iterable(deck_elements)
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
                    element_start_frac_len = y / len(y_nodes_z_lo)
                    # print(f"y = {y}, len nodes = {len(y_nodes_z_lo)}, element_start_frac = {element_start_frac_len}")
                    section = section_for_pier_element(
                        c=c, pier=c.bridge.supports[s],
                        element_start_frac_len=element_start_frac_len)
                    pier_elements.append(ShellElement(
                        e_id=next_elem_id(), ni_id=y_lo_z_lo.n_id,
                        nj_id=y_hi_z_lo.n_id, nk_id=y_hi_z_hi.n_id,
                        nl_id=y_lo_z_hi.n_id, section=section,
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


def opensees_load(c: Config, pload: PointLoad, deck_nodes: DeckNodes):
    """An OpenSees load command."""
    min_z_diff = np.inf  # Minimum difference in z of node to load.
    min_x_diff = np.inf  # Minimum difference in x of node to load.
    # print_d(D, f"load.z_frac = {load.z_frac}")
    pload_z = c.bridge.z(z_frac=pload.z_frac)
    pload_x = c.bridge.x(x_frac=pload.x_frac)
    best_node = None
    # The deck nodes are first sorted by z position, then by x position. First
    # iterate through the z positions to find best line of nodes...
    best_x_nodes = None
    for x_nodes in deck_nodes:
        # print_d(D, f"x_nodes[0].z = {x_nodes[0].z}")
        # print_d(D, f"load_z = {load_z}")
        if abs(x_nodes[0].z - pload_z) < min_z_diff:
            min_z_diff = abs(x_nodes[0].z - pload_z)
            # print_d(D, f"min_z_diff = {min_z_diff}")
            best_x_nodes = x_nodes
        else:
            break
    # print_d(D, f"best_x_nodes.x = {best_x_nodes[0].x}")
    # print_d(D, f"best_x_nodes.z = {best_x_nodes[0].z}")
    # ...then iterate through x positions to find the best point.
    for x_ind, node in enumerate(best_x_nodes):
        if abs(node.x - pload_x) < min_x_diff:
            min_x_diff = abs(node.x - pload_x)
            best_node = node
            # print_d(D, f"min_x_diff = {min_x_diff}")
            # print_d(D, f"{x_ind / len(x_nodes)}")
            # print_d(D, f"load_x = {load_x}")
        else:
            break
    # print_d(D, f"best_node.x = {best_node.x}")
    # print_d(D, f"best_node.z = {best_node.z}")
    # print_d(D, f"Generating OpenSees load command for {load}")
    return f"load {best_node.n_id} 0 {pload.kn * 1000} 0 0 0 0"


def opensees_loads(c: Config, ploads: List[PointLoad], deck_nodes: DeckNodes):
    """OpenSees load commands for a .tcl file."""
    return comment(
        "loads",
        "\n".join(
            opensees_load(c=c, pload=pload, deck_nodes=deck_nodes)
            for pload in ploads),
        units="load nodeTag N_x N_y N_z N_rx N_ry N_rz")


##### End loads #####
##### Begin recorders #####


def opensees_translation_recorders(
        c: Config, fem_params: FEMParams, os_runner: "OSRunner") -> str:
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
        print_d(D, f"Adding response path to build: {response_path}")
        recorder_strs.append(
            f"recorder Node -file {response_path} -node {node_str} -dof"
            + f" {direction} disp")
    return comment(
        "translation recorders", "\n".join(recorder_strs),
        units="recorder Node -file path -node nodeTags -dof direction disp")


def opensees_stress_recorder(
        c: Config, fem_params: FEMParams, os_runner: "OSRunner") -> str:
    """OpenSees recorder command for stresses."""
    all_elements = bridge_3d_elements(
        deck_elements=fem_params.deck_elements,
        all_pier_elements=fem_params.all_pier_elements)
    ele_str = " ".join(str(e.e_id) for e in all_elements)
    recorder_str = (
        f"recorder Element -file test.out -ele {ele_str} stresses")
    return comment("element recorders", recorder_str, units="TODO units")


def opensees_recorders(
        c: Config, fem_params: FEMParams, os_runner: "OSRunner"):
    """OpenSees recorder commands for translation and stresses."""
    return "\n".join([
        opensees_translation_recorders(
            c=c, fem_params=fem_params, os_runner=os_runner),
        opensees_stress_recorder(
            c=c, fem_params=fem_params, os_runner=os_runner)])


##### End recorders #####


def build_model_3d(
        c: Config, expt_params: ExptParams, os_runner: "OSRunner",
        include_support_nodes: bool = True):
    """Build OpenSees 3D model files.

    Args:
        c: Config, global configuratin object.
        include_support_nodes: bool, for testing, if False don't include the
            nodes for the supports.

    """
    # Read in the template model file.
    with open(c.os_3d_model_template_path) as f:
        in_tcl = f.read()
    # Build a model file for each simulation.
    for fem_params in expt_params.fem_params:
        num_nodes_x, num_nodes_z = num_deck_nodes(c)
        print_i(
            f"OpenSees: building 3D model, {num_nodes_x} * {num_nodes_z} deck"
            + " nodes")
        # Displacement control is not supported yet in 3D.
        if fem_params.displacement_ctrl is not None:
            raise ValueError("OpenSees: Displacement not supported in 3D")
        # Reset IDs before building.
        reset_nodes()
        reset_elem_ids()
        # Attach deck nodes and pier nodes to the FEMParams to be available when
        # converting raw responses to responses with positions attached. Note,
        # that there are some overlap between deck nodes and pier nodes, and
        # some over lap between nodes of both walls of one pier (at the bottom
        # where they meet).
        deck_nodes_str, deck_nodes = opensees_deck_nodes(
            c=c, include_support_nodes=include_support_nodes)
        all_support_nodes = []
        if include_support_nodes:
            all_support_nodes = get_all_support_nodes(c)
            print(len(all_support_nodes))
            assert_support_nodes(c=c, all_support_nodes=all_support_nodes)
        fem_params.deck_nodes = deck_nodes
        fem_params.all_support_nodes = all_support_nodes
        # Attach deck elements and pier elements to the FEMParams to be
        # available when converting raw responses to responses with positions
        # attached.
        fem_params.deck_elements = get_deck_elements(
            c=c, deck_nodes=fem_params.deck_nodes)
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
                all_support_nodes=all_support_nodes))
            .replace("<<LOAD>>", opensees_loads(
                c=c, ploads=fem_params.ploads, deck_nodes=deck_nodes))
            .replace("<<FIX_DECK>>", opensees_fixed_deck_nodes(
                c=c, deck_nodes=deck_nodes))
            .replace("<<FIX_SUPPORTS>>", opensees_fixed_support_nodes(
                c=c, all_support_nodes=all_support_nodes))
            .replace("<<SUPPORTS>>", "")
            .replace("<<DECK_SECTIONS>>", opensees_deck_sections(c=c))
            .replace("<<PIER_SECTIONS>>", opensees_pier_sections(c=c))
            .replace("<<RECORDERS>>", opensees_recorders(
                c=c, fem_params=fem_params, os_runner=os_runner))
            .replace("<<DECK_ELEMENTS>>", opensees_deck_elements(
                c=c, deck_elements=fem_params.deck_elements))
            .replace("<<PIER_ELEMENTS>>", opensees_pier_elements(
                c=c, all_pier_elements=fem_params.all_pier_elements)))
        # Write the generated model file.
        model_path = os_runner.fem_file_path(fem_params=fem_params, ext="tcl")
        print(model_path)
        with open(model_path, "w") as f:
            f.write(out_tcl)
        print_i(f"OpenSees: saved 3D model file to {model_path}")
    return expt_params
