from collections import OrderedDict
from typing import Dict, Tuple

from config import Config
from fem.run.build import ff_mod
from fem.run.build.types import (
    AllSupportNodes,
    AllPierElements,
    DeckElements,
    DeckNodes,
    Node,
    ShellElement,
)
from fem.run.build.elements.sections import (
    section_for_deck_element,
    section_for_pier_element,
)


_elem_id = None

# A dictionary of node's to shell elements.
#
# If you call 'build_model_3d' and then call '.values' on this dictionary it
# provides an easy way to get all 'ShellElement's for the previously built
# model.
shells_by_id: Dict[Tuple[int, int, int, int], ShellElement] = OrderedDict()


def next_elem_id() -> int:
    """Return the next element ID and increment the counter."""
    global _elem_id
    result = _elem_id
    _elem_id = result + 1
    return result


def reset_elem_ids():
    """Reset element IDs to 0, e.g. when building a new model file."""
    global _elem_id
    global shells_by_id
    shells_by_id.clear()
    _elem_id = 1


def ff_elem_ids(mod: int):
    """Fast forward element IDs until divisible by "mod"."""
    global _elem_id
    while _elem_id % mod != 0:
        _elem_id += 1


def get_shell(ni_id: int, nj_id: int, nk_id: int, nl_id: int, **kwargs):
    """Get a 'Shell' if already exists with Node IDs, else create a new one.

    NOTE: Use this to contruct 'Shell's, don't do it directly!

    """
    key = (ni_id, nj_id, nk_id, nl_id)
    if key in shells_by_id:
        raise ValueError("Attempt to get same element twice, with key {key}")
    shells_by_id[key] = ShellElement(
        e_id=next_elem_id(),
        ni_id=ni_id,
        nj_id=nj_id,
        nk_id=nk_id,
        nl_id=nl_id,
        **kwargs,
    )
    return shells_by_id[key]


##### End element IDs #####


def get_deck_elements(
    c: Config, deck_nodes: DeckNodes, nodes_by_id: Dict[int, Node]
) -> DeckElements:
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
                c=c,
                element_x=nodes_by_id[i_node].x,
                element_z=nodes_by_id[i_node].z,
            )
            deck_elements[-1].append(
                get_shell(
                    ni_id=i_node,
                    nj_id=j_node,
                    nk_id=k_node,
                    nl_id=l_node,
                    section=section,
                    pier=False,
                    nodes_by_id=nodes_by_id,
                )
            )
        ff_elem_ids(z_skip)
    return deck_elements


def get_pier_elements(
    c: Config, all_support_nodes: AllSupportNodes, nodes_by_id: Dict[int, Node]
) -> AllPierElements:
    """Shell elements that make up a bridge's piers."""
    pier_elements = []  # The result.
    for s, support_nodes in enumerate(all_support_nodes):
        for w, wall_nodes in enumerate(support_nodes):
            z = 0  # Keep an index of current transverse (z) line.
            # For each pair of (line of nodes in y direction).
            for y_nodes_z_lo, y_nodes_z_hi in zip(
                wall_nodes[:-1], wall_nodes[1:]
            ):
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
                    start_frac_len = y / (len(y_nodes_z_lo) - 2)
                    # print(f"y = {y}, len nodes = {len(y_nodes_z_lo)}, element_start_frac = {element_start_frac_len}")
                    section = section_for_pier_element(
                        c=c,
                        pier=c.bridge.supports[s],
                        start_frac_len=start_frac_len,
                    )
                    pier_elements.append(
                        get_shell(
                            ni_id=y_lo_z_lo.n_id,
                            nj_id=y_hi_z_lo.n_id,
                            nk_id=y_hi_z_hi.n_id,
                            nl_id=y_lo_z_hi.n_id,
                            section=section,
                            pier=True,
                            nodes_by_id=nodes_by_id,
                            support_position_index=(s, w, z, y),
                        )
                    )
                ff_elem_ids(ff_mod)
                z += 1
    return pier_elements
