"""Build a mesh of a Bridge deck."""

import math
from typing import List, NewType, Tuple

import numpy as np

from bridge_sim.model import Bridge
from bridge_sim.sim.model import (
    BuildContext,
    DeckNodes,
    DeckShellNodes,
    DeckShells,
    Node,
)
from bridge_sim.util import assert_sorted, flatten, print_i, print_w, round_m

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
        xs.add(round_m(bridge.x(section.end_x_frac)))
        zs.add(round_m(bridge.z(section.start_z_frac)))
        zs.add(round_m(bridge.z(section.end_z_frac)))
    return sorted(xs), sorted(zs)


def get_deck_xs(bridge: Bridge, ctx: BuildContext) -> List[float]:
    all_xs = set()

    # From piers.
    for pier in bridge.supports:
        for x in pier.x_min_max_top():
            all_xs.add(round_m(x))

    # Bridge ends.
    all_xs.add(round_m(bridge.x_min))
    all_xs.add(round_m(bridge.x_max))

    # From loads.
    for point in ctx.add_loads:
        all_xs.add(round_m(point.x))

    # From material propertes.
    for x in get_deck_section_grid(bridge)[0]:
        all_xs.add(round_m(x))

    # Additional nodes requested by the Bridge.
    for x in bridge.additional_xs:
        all_xs.add(round_m(x))

    all_xs = sorted(all_xs)
    print(f"all_xs = {all_xs}")
    deck_xs = set()
    for i in range(len(all_xs) - 1):
        x0, x1 = all_xs[i], all_xs[i + 1]
        num = math.ceil((x1 - x0) / bridge.base_mesh_deck_max_x) + 1
        for x in np.linspace(x0, x1, num=num):
            deck_xs.add(round_m(x))
    return sorted(deck_xs)


def get_deck_zs(bridge: Bridge, ctx: BuildContext) -> List[float]:
    all_zs = set()

    # From piers.
    for pier in bridge.supports:
        for z in pier.z_min_max_top():
            all_zs.add(round_m(z))
    pier_zs = set(all_zs)
    print(f"pier_zs = {pier_zs}")

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
        # print(f"z0, z1, num = {z0}, {z1}, {num}")
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

    # Convert to 'DeckShellNodes'.
    deck_shell_nodes = []
    for z_i in range(len(deck_nodes) - 1):
        for x_i in range(len(deck_nodes[0]) - 1):
            node_i = deck_nodes[z_i][x_i]
            node_j = deck_nodes[z_i][x_i + 1]
            node_k = deck_nodes[z_i + 1][x_i + 1]
            node_l = deck_nodes[z_i + 1][x_i]
            deck_shell_nodes.append((node_i, node_j, node_k, node_l))

    if len(ctx.refinement_radii) > 0:
        raise NotImplementedError("Refinement not implemented!")
    return deck_shell_nodes


def get_deck_shells(
    bridge: Bridge, deck_shell_nodes: DeckShellNodes, ctx: BuildContext
) -> DeckShells:
    shells = []
    for node_i, node_j, node_k, node_l in deck_shell_nodes:
        center_x = round_m(node_i.x + (node_i.distance_n(node_j) / 2))
        center_z = round_m(node_i.z + (node_i.distance_n(node_l) / 2))
        section = bridge.deck_section_at(x=center_x, z=center_z)
        shells.append(
            ctx.get_shell(
                ni_id=node_i.n_id,
                nj_id=node_j.n_id,
                nk_id=node_k.n_id,
                nl_id=node_l.n_id,
                pier=False,
                section=section,
            )
        )
    return shells
