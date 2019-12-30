import math
from itertools import chain
from typing import List, NewType, Tuple

import numpy as np

from fem.model import BuildContext, DeckNodes, DeckShellNodes, DeckShells, Node, Shell
from model.bridge import Bridge, Section3D
from util import assert_sorted, flatten, print_i, round_m

# A list of x positions, and a list of z positions.
DeckGrid = NewType("DeckPositions", Tuple[List[float], List[float]])


def get_deck_section_grid(bridge: Bridge) -> DeckGrid:
    """Grid where material properties change on the deck."""
    if callable(bridge.sections):
        print_w(
            "Not adding additional nodes to bridge deck because material "
            " properties are given as a potentially continuous function"
        )
        return [], []
    xs, zs = set(), set()
    for section in bridge.sections:
        xs.add(round_m(bridge.x(section.start_x_frac)))
        zs.add(round_m(bridge.z(section.start_z_frac)))
    return sorted(xs), sorted(zs)


def get_deck_xs(bridge: Bridge, ctx: BuildContext) -> List[float]:
    all_xs = set()

    # From piers.
    for pier in bridge.supports:
        for x in pier.x_min_max():
            all_xs.add(round_m(x))
    print(f"pier_xs = {all_xs}")

    # Bridge ends.
    all_xs.add(round_m(bridge.x_min))
    all_xs.add(round_m(bridge.x_max))

    # From loads.
    for point in ctx.add_loads:
        all_xs.add(round_m(point.x))

    # From material propertes.
    for x in get_deck_section_grid(bridge)[0]:
        all_xs.add(round_m(x))

    all_xs = sorted(all_xs)
    print(f"all_xs = {all_xs}")
    deck_xs = set()
    for i in range(len(all_xs) - 1):
        x0, x1 = all_xs[i], all_xs[i + 1]
        num = math.ceil((x1 - x0) / bridge.base_mesh_deck_max_x) + 1
        print(f"x0, x1, num = {x0}, {x1}, {num}")
        for x in np.linspace(x0, x1, num=num):
            deck_xs.add(round_m(x))
    return sorted(deck_xs)


def get_deck_zs(bridge: Bridge, ctx: BuildContext) -> List[float]:
    all_zs = set()

    # From piers.
    for pier in bridge.supports:
        for z in pier.z_min_max_top():
            all_zs.add(round_m(z))
    print(f"pier_zs = {all_zs}")

    # Bridge ends.
    all_zs.add(round_m(bridge.z_min))
    all_zs.add(round_m(bridge.z_max))

    # From loads.
    for point in ctx.add_loads:
        all_zs.add(round_m(point.z))

    # From material propertes.
    for z in get_deck_section_grid(bridge)[1]:
        all_zs.add(round_m(z))

    all_zs = sorted(all_zs)
    print(f"all_zs = {all_zs}")
    deck_zs = set()
    for i in range(len(all_zs) - 1):
        z0, z1 = all_zs[i], all_zs[i + 1]
        num = math.ceil((z1 - z0) / bridge.base_mesh_deck_max_z) + 1
        print(f"z0, z1, num = {z0}, {z1}, {num}")
        for z in np.linspace(z0, z1, num=num):
            deck_zs.add(round_m(z))
    return sorted(deck_zs)


def get_deck_grid(bridge: Bridge, ctx: BuildContext) -> DeckGrid:
    return get_deck_xs(bridge=bridge, ctx=ctx), get_deck_zs(bridge=bridge, ctx=ctx)


def get_base_deck_nodes(bridge: Bridge, ctx: BuildContext) -> DeckNodes:
    """Deck nodes without refinement."""
    deck_grid = get_deck_grid(bridge=bridge, ctx=ctx)
    nodes = []
    for z in deck_grid[1]:
        nodes.append([])
        for x in deck_grid[0]:
            nodes[-1].append(ctx.get_node(x=x, y=0, z=z, deck=True))
    return nodes


def get_deck_nodes(bridge: Bridge, ctx: BuildContext) -> DeckShellNodes:
    """Deck nodes with refinement."""
    deck_nodes = get_base_deck_nodes(bridge=bridge, ctx=ctx)
    assert_sorted([nodes[0].z for nodes in deck_nodes])
    assert_sorted([len(nodes) for nodes in deck_nodes])  # All should be equal.
    assert_sorted([node.x for node in deck_nodes[0]])
    print_i(f"Nodes before refinement = {len(flatten(deck_nodes, Node))}")

    # Convert to 'DeckShellNodes' (+ refinement information).
    deck_shell_nodes = []
    for z_i in range(len(deck_nodes) - 1):
        for x_i in range(len(deck_nodes[0]) - 1):
            node_i = deck_nodes[z_i][x_i]
            node_j = deck_nodes[z_i][x_i + 1]
            node_k = deck_nodes[z_i + 1][x_i + 1]
            node_l = deck_nodes[z_i + 1][x_i]
            deck_shell_nodes.append((node_i, node_j, node_k, node_l, 0))

    # If  not refining, return the 'DeckShellNodes'.
    if not ctx.refine_loads:
        return list(map(lambda ns: ns[:-1], deck_shell_nodes))

    def refine_shell(nodes: List[Node], max_dist: float):
        """Should the shell be refined?"""
        for point in ctx.add_loads:
            for node in nodes:
                if abs(node.distance(x=point.x, y=point.y, z=point.z)) <= max_dist:
                    return True
        return False

    # For each refinement pass..
    for refinement_iter, max_dist in enumerate(ctx.refinement_radii):
        # Construct a new 'DeckShellNodes' and iterate over the previous one.
        new_deck_shell_nodes = []
        for node_i, node_j, node_k, node_l, num_refined in deck_shell_nodes:
            # If not refining, keep the existing shell.
            if (
                    (not refine_shell([node_i, node_j, node_k, node_l], max_dist))
                    or (num_refined > refinement_iter)
            ):
                new_deck_shell_nodes.append((node_i, node_j, node_k, node_l, num_refined))
            # Else if refining, construct 5 new nodes, and 4 new shells.
            else:
                center_x = round_m(node_i.x + (node_i.distance_n(node_j) / 2))
                center_z = round_m(node_i.z + (node_i.distance_n(node_l) / 2))
                # Construct the 5 new nodes.
                center_node, bottom_node, top_node, left_node, right_node = [
                    ctx.get_node(x=x, y=0, z=z, deck=True)
                    for z, x in
                    [
                        (center_z, center_x), # Center node.
                        (node_i.z, center_x), # Bottom node.
                        (node_l.z, center_x), # Top node.
                        (center_z, node_i.x), # Left node.
                        (center_z, node_j.x), # Right node.
                    ]
                ]
                # Construct the 4 new shells.
                for shell_nodes in [
                        (node_i, bottom_node, center_node, left_node),  # Bottom left.
                        (bottom_node, node_j, right_node, center_node),  # Bottom right.
                        (left_node, center_node, top_node, node_l),  # Top left.
                        (center_node, right_node, node_k, top_node),  # Top right.
                ]:
                    new_deck_shell_nodes.append(shell_nodes + (num_refined + 1,))
        deck_shell_nodes = new_deck_shell_nodes

    deck_shell_nodes = list(map(lambda ns: ns[:-1], deck_shell_nodes))
    print_i(f"Nodes after refinement = {len(set(flatten(deck_shell_nodes, Node)))}")
    return deck_shell_nodes


def get_deck_shells(bridge: Bridge, deck_shell_nodes: DeckShellNodes, ctx: BuildContext) -> DeckShells:
    shells = []
    for node_i, node_j, node_k, node_l in deck_shell_nodes:
        center_x = round_m(node_i.x + (node_i.distance_n(node_j) / 2))
        center_z = round_m(node_i.z + (node_i.distance_n(node_l) / 2))
        section = bridge.deck_section_at(x=center_x, z=center_z)
        shells.append(ctx.get_shell(
            ni_id=node_i.n_id,
            nj_id=node_j.n_id,
            nk_id=node_k.n_id,
            nl_id=node_l.n_id,
            pier=False,
            section=section
        ))
    return shells
