import math
from typing import List, NewType, Tuple

import numpy as np

from fem.model import BuildContext, DeckNodes, DeckShells, Node, Shell
from model.bridge import Bridge, Section3D
from util import assert_sorted, round_m

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


def get_deck_nodes(bridge: Bridge, ctx: BuildContext) -> DeckNodes:
    deck_grid = get_deck_grid(bridge=bridge, ctx=ctx)
    nodes = []
    for x in deck_grid[0]:
        nodes.append([])
        for z in deck_grid[1]:
            nodes[-1].append(ctx.get_node(x=x, y=0, z=z, deck=True))
    return nodes


def get_deck_shells(bridge: Bridge, deck_nodes: DeckNodes, ctx: BuildContext) -> DeckShells:
    # A quick check that the deck nodes are 'somewhat' sorted.
    xs = [nodes[0].x for nodes in deck_nodes]
    assert_sorted(xs)
    zs = [node.z for node in deck_nodes[0]]
    print(zs)
    assert_sorted(zs)

    shells = []
    for x_i in range(len(xs) - 1):
        shells.append([])
        for z_i in range(len(zs) - 1):
            node_i = deck_nodes[x_i][z_i]
            node_j = deck_nodes[x_i + 1][z_i]
            node_k = deck_nodes[x_i + 1][z_i + 1]
            node_l = deck_nodes[x_i][z_i + 1]
            delta_x = node_j.x - node_i.x
            delta_z = node_l.z - node_i.z
            center_x = node_i.x + delta_x
            center_z = node_i.z + delta_z
            section = bridge.deck_section_at(x=center_x, z=center_z)
            shells[-1].append(ctx.get_shell(
                ni_id=node_i.n_id,
                nj_id=node_j.n_id,
                nk_id=node_k.n_id,
                nl_id=node_l.n_id,
                pier=False,
                section=section))
    return shells
