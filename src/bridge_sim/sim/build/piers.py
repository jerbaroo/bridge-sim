"""Build a mesh of Bridge supports."""

import math

import numpy as np
from scipy.interpolate import interp1d

from bridge_sim.model import Bridge
from bridge_sim.sim.model import BuildContext, PierNodes


def get_pier_nodes(bridge: Bridge, ctx: BuildContext) -> PierNodes:
    """Nodes for all a bridge's piers.

    NOTE: This function assumes that 'get_deck_nodes' has already been called
    with the same 'BuildContext'.

    """
    pier_nodes = []
    for pier in bridge.supports:
        z_min, z_max = pier.z_min_max_top()

        # Left wall: top nodes.
        xy_nodes_left = ctx.get_nodes_at_xy(x=pier.x_min_max_top()[0], y=0)
        top_nodes_left = sorted(
            [n for n in xy_nodes_left if z_min <= n.z <= z_max], key=lambda n: n.z
        )
        assert any(tn.z == z_min for tn in top_nodes_left)
        assert any(tn.z == z_max for tn in top_nodes_left)

        # Right wall: top nodes.
        xy_nodes_right = ctx.get_nodes_at_xy(x=pier.x_min_max_top()[1], y=0)
        top_nodes_right = sorted(
            [n for n in xy_nodes_right if z_min <= n.z <= z_max], key=lambda n: n.z
        )
        assert any(tn.z == z_min for tn in top_nodes_right)
        assert any(tn.z == z_max for tn in top_nodes_right)

        # Only consider top nodes at z-positions that exist on the left and
        # right. It may be the case, because of refinement, that some additional
        # nodes will exist on one side.
        if len(top_nodes_left) > len(top_nodes_right):
            zs_top_right = set([tn_r.z for tn_r in top_nodes_right])
            top_nodes_left = [tn_l for tn_l in top_nodes_left if tn_l.z in zs_top_right]
        elif len(top_nodes_right) > len(top_nodes_left):
            zs_top_left = set([tn_l.z for tn_l in top_nodes_left])
            top_nodes_right = [
                tn_r for tn_r in top_nodes_right if tn_r.z in zs_top_left
            ]

        # Shared bottom nodes of pier.
        bottom_z_interp = interp1d(
            [top_nodes_left[0].z, top_nodes_left[-1].z], pier.z_min_max_bottom(),
        )
        bottom_nodes = [
            ctx.get_node(
                x=pier.x, y=-pier.height, z=bottom_z_interp(top_node.z), deck=False
            )
            for top_node in top_nodes_left
        ]

        # Determine amount of nodes in longitudinal direction.
        long_dist = top_nodes_left[0].distance_n(bottom_nodes[0])
        num_long_nodes = math.ceil((long_dist / bridge.base_mesh_pier_max_long) + 1)

        # Left wall.
        wall_nodes_left = [[top_node] for top_node in top_nodes_left]
        # For each z index..
        for z_i in range(len(top_nodes_left)):
            # ..then for each position below the top node.
            left_x_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_left[z_i].x, bottom_nodes[z_i].x]
            )
            left_y_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_left[z_i].y, bottom_nodes[z_i].y]
            )
            left_z_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_left[z_i].z, bottom_nodes[z_i].z]
            )
            for x_i in range(1, num_long_nodes - 1):
                wall_nodes_left[z_i].append(
                    ctx.get_node(
                        x=left_x_interp(x_i),
                        y=left_y_interp(x_i),
                        z=left_z_interp(x_i),
                        deck=False,
                    )
                )
            wall_nodes_left[z_i].append(bottom_nodes[z_i])

        # Right wall.
        wall_nodes_right = [[top_node] for top_node in top_nodes_right]
        # For each z index..
        for z_i in range(len(top_nodes_right)):
            # ..then for each position below the top node.
            right_x_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_right[z_i].x, bottom_nodes[z_i].x]
            )
            right_y_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_right[z_i].y, bottom_nodes[z_i].y]
            )
            right_z_interp = interp1d(
                [0, num_long_nodes - 1], [top_nodes_right[z_i].z, bottom_nodes[z_i].z]
            )
            for x_i in range(1, num_long_nodes - 1):
                wall_nodes_right[z_i].append(
                    ctx.get_node(
                        x=right_x_interp(x_i),
                        y=right_y_interp(x_i),
                        z=right_z_interp(x_i),
                        deck=False,
                    )
                )
            wall_nodes_right[z_i].append(bottom_nodes[z_i])
        pier_nodes.append((wall_nodes_left, wall_nodes_right))
    return pier_nodes


def get_pier_shells(bridge: Bridge, pier_nodes: PierNodes, ctx: BuildContext):
    pier_shells = []
    print(np.array(pier_nodes).shape)
    for p_i, a_pier_nodes in enumerate(pier_nodes):
        a_pier_shells = []
        for wall_nodes in a_pier_nodes:
            wall_shells = []
            for z_i in range(len(wall_nodes) - 1):
                x_is = range(len(wall_nodes[0]) - 1)
                for x_i in x_is:
                    node_i = wall_nodes[z_i][x_i]
                    node_j = wall_nodes[z_i][x_i + 1]
                    node_k = wall_nodes[z_i + 1][x_i + 1]
                    node_l = wall_nodes[z_i + 1][x_i]
                    if len(wall_nodes[0]) < 2:
                        raise ValueError(
                            "Need at least 2 nodes in pier wall's longitudinal "
                            f" direction, was {len(wall_nodes[0])}"
                        )
                    frac_long = (
                        0
                        if len(wall_nodes[0]) == 2
                        else (x_i / (len(wall_nodes[0]) - 2))
                    )
                    # Sanity check that the top shell is assigned value 0 and
                    # the bottom is assigned value 1.
                    if x_i == x_is[0]:
                        assert frac_long == 0
                    elif x_i == x_is[-1]:
                        assert frac_long == 1
                    wall_shells.append(
                        ctx.get_shell(
                            ni_id=node_i.n_id,
                            nj_id=node_j.n_id,
                            nk_id=node_k.n_id,
                            nl_id=node_l.n_id,
                            pier=True,
                            section=bridge.pier_section_at_len(
                                p_i=p_i, section_frac_len=frac_long
                            ),
                        )
                    )
            a_pier_shells.append(wall_shells)
        pier_shells.append(a_pier_shells)
    return pier_shells
