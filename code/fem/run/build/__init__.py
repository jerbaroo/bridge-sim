"""Shared functionality for building FEMs."""
from itertools import chain
from copy import deepcopy
from collections import OrderedDict, defaultdict
from typing import Dict, List, NewType, Optional, Tuple

import numpy as np

from config import Config
from fem.params import SimParams
from fem.run.build.assert_ import (
    assert_all_pier_nodes,
    assert_deck_in_pier_pier_in_deck,
)
from fem.run.build.types import AllSupportNodes, DeckNodes, Node
from fem.run.build.util import print_mesh_info
from model.bridge import Bridge, Section3D, Support3D
from util import print_d, round_m, st

# TODO: Experimental, but I think this works.
DECK_NODES_IN_PIER = True

# Print debug information for this file.
D: str = "fem.run.build"
# D: bool = False


def assert_sorted(l):
    assert all(l[i] <= l[i + 1] for i in range(len(l) - 1))


##### Begin node factory #####

# A dictionary of x position to y position to z position to 'Node'.
all_nodes = defaultdict(lambda: defaultdict(dict))

# A dictionary of 'Node' ID to 'Node'.
#
# If you call 'build_model_3d' and then call '.values' on this dictionary it
# provides an easy way to get all 'Node's for the previously built model.
nodes_by_id = dict()


def get_node(
    x: float,
    y: float,
    z: float,
    deck: bool = False,
    pier: Optional[Support3D] = None,
    comment_str: Optional[str] = None,
    support: Optional[Support3D] = None,
):
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
            n_id=next_node_id(),
            x=x,
            y=y,
            z=z,
            comment=comment_str,
            support=support,
            pier=pier,
            deck=deck,
        )
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


# A list of x and z positions of deck nodes.
DeckPositions = NewType("DeckPositions", Tuple[List[float], List[float]])


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
        all_z_positions.append(
            np.interp(pier_positions_deck, [old_min, old_max], [new_min, new_max])
        )
        assert_sorted(all_z_positions[-1])
    return list(map(round_m, all_z_positions))


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
        print_d(
            D, f"pier {p}. min, max = {base_pier_min_z_pos}, {base_pier_max_z_pos}",
        )
        # And include z positions from the deck grid within the pier's range.
        assert_sorted(deck_positions[1])
        for deck_z_pos in deck_positions[1]:  # Index '1' are the z positions.
            if simple_mesh or not DECK_NODES_IN_PIER:
                break
            if base_pier_min_z_pos < deck_z_pos < base_pier_max_z_pos:
                all_pier_z_positions[-1].add(deck_z_pos)
        all_pier_z_positions[-1] = sorted(all_pier_z_positions[-1])
        assert_sorted(all_pier_z_positions[-1])
    return all_pier_z_positions


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


def get_base_mesh_z_positions_of_pier_deck_nodes(c: Config,) -> List[List[float]]:
    """The z positions of deck nodes of each pier's base mesh."""
    z_positions = []
    for support in c.bridge.supports:
        z_positions.append([support.z - (support.width_top / 2)])
        z_step = support.width_top / (c.bridge.base_mesh_pier_nodes_z - 1)
        for _ in range(c.bridge.base_mesh_pier_nodes_z - 1):
            z_positions[-1].append(z_positions[-1][-1] + z_step)
        assert_sorted(z_positions[-1])
    return list(map(round_m, z_positions))


def get_base_mesh_deck_positions(bridge: Bridge) -> DeckPositions:
    """X and z positions of deck nodes in the base mesh.

    This is just a grid of evenly spaced positions across the deck.

    """
    x_positions, z_positions = [bridge.x_min], [bridge.z_min]
    x_step = bridge.length / (bridge.base_mesh_deck_nodes_x - 1)
    z_step = bridge.width / (bridge.base_mesh_deck_nodes_z - 1)
    for _ in range(bridge.base_mesh_deck_nodes_x - 1):
        x_positions.append(round_m(x_positions[-1] + x_step))
    for _ in range(bridge.base_mesh_deck_nodes_z - 1):
        z_positions.append(round_m(z_positions[-1] + z_step))
    assert np.isclose(x_positions[-1], bridge.x_max)
    assert np.isclose(z_positions[-1], bridge.z_max)
    return x_positions, z_positions


def get_pier_deck_positions(c: Config) -> DeckPositions:
    """The x and z positions of deck nodes that belong to piers."""
    return (
        sorted(chain.from_iterable(get_x_positions_of_pier_deck_nodes(c))),
        sorted(chain.from_iterable(get_base_mesh_z_positions_of_pier_deck_nodes(c))),
    )


def get_deck_load_positions(bridge: Bridge, fem_params: SimParams) -> DeckPositions:
    """The x and z positions of deck nodes that belong to loads."""
    return (
        sorted([round_m(bridge.x(load.x_frac)) for load in fem_params.ploads]),
        sorted([round_m(bridge.z(load.z_frac)) for load in fem_params.ploads]),
    )


def get_deck_section_positions(bridge: Bridge):
    """The x and z positions where material properties change on the deck."""
    if callable(bridge.sections):
        print_w(
            "Not adding additional nodes to bridge deck based on changing"
            " material properties"
        )
        return [], []
    x_positions, z_positions = set(), set()
    for section in chain.from_iterable(bridge.sections):
        x_positions.add(round_m(bridge.x(section.start_x_frac)))
        z_positions.add(round_m(bridge.z(section.start_z_frac)))
    return sorted(x_positions), sorted(z_positions)


def get_deck_nodes(
    c: Config, fem_params: SimParams, deck_positions: DeckPositions
) -> Tuple[str, DeckNodes]:
    """OpenSees nodes that belong to the bridge deck.

    The nodes are created based on given positions of deck nodes.

    Args:
        c: Config, global configuration object.

    """
    # Unpack x and z positions of nodes on the deck.
    x_positions, z_positions = deck_positions

    # Get positions of pier nodes that are on the deck, to check if a deck node
    # also belongs to the pier. The check is only to add a comment.
    x_positions_piers, z_positions_piers = get_pier_deck_positions(c=c)
    is_pier_node = lambda x_, z_: (x_ in x_positions_piers and z_ in z_positions_piers)

    set_ff_mod(len(x_positions))
    nodes = []
    for z_pos in z_positions:
        # Fast forward node IDs when we move to a new z position.
        ff_node_ids()
        nodes.append([])
        for x_pos in x_positions:
            comment_str = "support node" if is_pier_node(x_=x_pos, z_=z_pos) else None
            nodes[-1].append(
                get_node(x=x_pos, y=0, z=z_pos, deck=True, comment_str=comment_str)
            )
    return nodes


# The x and y deck positions after each stage of building.
DeckStagesInfo = NewType("DeckStagesInfo", Dict[str, DeckPositions])


def get_deck_positions(
    c: Config, fem_params: SimParams, simple_mesh: bool
) -> DeckPositions:
    """The x and z positions of deck nodes.

    NOTE: This function will attach 'DeckStagesInfo' to the given 'FEMParams'
    under the attribute 'deck_stages_info'.

    Args:
        c: Config, global configuration object.

    """
    # First collect positions from the base mesh.
    x_positions, z_positions = get_base_mesh_deck_positions(c.bridge)
    x_positions = set(map(round_m, x_positions))
    z_positions = set(map(round_m, z_positions))

    # Start creating the 'DeckStagesInfo', it is attached to the 'FEMParams'.
    deck_stages_info = OrderedDict(
        [("base", (deepcopy(x_positions), deepcopy(z_positions)))]
    )
    fem_params.deck_stages_info = deck_stages_info

    # If requested, collect positions from piers.
    x_positions_piers, z_positions_piers = get_pier_deck_positions(c=c)
    assert_sorted(x_positions_piers)
    assert_sorted(z_positions_piers)
    if not simple_mesh:
        for x_pos in x_positions_piers:
            x_positions.add(round_m(x_pos))
        for z_pos in z_positions_piers:
            z_positions.add(round_m(z_pos))

    # Update the 'DeckStagesInfo' with pier information.
    deck_stages_info["piers"] = (deepcopy(x_positions), deepcopy(z_positions))

    # Collect loading positions.
    x_positions_loads, z_positions_loads = get_deck_load_positions(
        bridge=c.bridge, fem_params=fem_params
    )
    assert_sorted(x_positions_loads)
    assert_sorted(z_positions_loads)
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

    # Collect positions from material properties.
    x_positions_sections, z_positions_sections = get_deck_section_positions(c.bridge)
    if not simple_mesh:
        for x_pos in x_positions_sections:
            x_positions.add(x_pos)
        for z_pos in z_positions_sections:
            z_positions.add(z_pos)

    # Update the 'DeckStagesInfo' with material property information.
    deck_stages_info["sections"] = (
        deepcopy(x_positions),
        deepcopy(z_positions),
    )

    return sorted(x_positions), sorted(z_positions)


def get_all_pier_nodes(
    c: Config, deck_positions: DeckPositions, simple_mesh: bool
) -> AllSupportNodes:
    """All nodes for all a bridge's supports.

    If 'simple_mesh' is passed here, then nodes from bridge deck's mesh will be
    added to the pier's mesh.

    """
    nodes = []
    x_positions_deck = get_x_positions_of_pier_deck_nodes(c)
    z_positions_deck = get_z_positions_of_pier_deck_nodes(
        c=c, deck_positions=deck_positions, simple_mesh=simple_mesh
    )
    x_positions_bottom = get_x_positions_of_pier_bottom_nodes(c)
    # z_positions_bottom = get_base_mesh_z_positions_of_pier_bottom_nodes(c)
    z_positions_bottom = get_z_positions_of_pier_bottom_nodes(
        c, positions_deck=z_positions_deck
    )
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
                    wall[-1].append(
                        get_node(
                            x=x_pos,
                            y=y_pos,
                            z=z_pos,
                            pier=support,
                            support=support,
                            comment_str=(
                                f"support {i + 1}{st(i + 1)} wall {w + 1}{st(w + 1)} z {z + 1} "
                                + f"y {y + 2}{st(y + 2)}"
                            ),
                        )
                    )

                # Append the first wall node for the current fixed z value then
                # iterate through the remaining nodes in y direction.
                append_wall_node(-1)
                for y in range(c.bridge.base_mesh_pier_nodes_y - 1):
                    x_pos += x_diff
                    y_pos += y_diff
                    z_pos += z_diff
                    append_wall_node(y)
    assert_all_pier_nodes(c, nodes)
    return nodes


def get_all_nodes(
    c: Config, sim_params: SimParams, simple_mesh: bool, print_mesh: bool = True
) -> Tuple[DeckNodes, AllSupportNodes, Dict[int, Node]]:
    """Returns all the nodes of a new mesh."""
    reset_nodes()
    deck_positions = get_deck_positions(
        c=c, fem_params=sim_params, simple_mesh=simple_mesh
    )
    deck_nodes = get_deck_nodes(
        c=c, fem_params=sim_params, deck_positions=deck_positions
    )
    all_pier_nodes = get_all_pier_nodes(
        c, deck_positions=deck_positions, simple_mesh=simple_mesh
    )
    assert_all_pier_nodes(c=c, all_pier_nodes=all_pier_nodes)

    if print_mesh:
        print_mesh_info(
            bridge=c.bridge, sim_params=sim_params, all_pier_nodes=all_pier_nodes,
        )
    if not simple_mesh:
        assert_deck_in_pier_pier_in_deck(
            deck_nodes=deck_nodes, all_pier_nodes=all_pier_nodes
        )
    return deck_nodes, all_pier_nodes, nodes_by_id
