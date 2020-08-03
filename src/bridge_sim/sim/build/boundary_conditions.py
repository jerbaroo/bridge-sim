"""Build a mesh of Bridge boundary conditions."""

from typing import List

import numpy as np
from scipy.interpolate import interp1d

from bridge_sim.model import Bridge
from bridge_sim.sim.model import BuildContext


def get_boundary_condition_nodes(bridge: Bridge, ctx: BuildContext) -> List:
    """Nodes for all boundary conditions at bridge's piers.
    Creates a duplicate of each node at the bottom of each pier for the zero-length element

    NOTE: This function assumes that 'get_deck_nodes' and `get_pier_nodes`
    has already been called with the same 'BuildContext'.

    """
    bc_nodes = []
    for index, support_spring in enumerate(bridge.support_springs):
        pier = support_spring.connected_to
        z_min, z_max = pier.z_min_max_bottom()
        x_bottom = pier.x
        y_min = pier.y_min_max()[0]

        # Pier bottom nodes
        xy_nodes = ctx.get_nodes_at_xy(x=x_bottom, y=y_min)
        bc_pier_nodes = []
        for xy_node in xy_nodes:
            if z_min <= xy_node.z <= z_max:
                bc_pier_nodes.append(
                    ctx.get_node(
                        x=xy_node.x,
                        y=xy_node.y,
                        z=xy_node.z,
                        deck=False,
                        comment=f"BC, pier: {index+1}",
                        allow_identical_pos=True,
                    )
                )
                # print(f"X:{xy_node.x}, Y:{xy_node.y}, Z:{xy_node.z}")

        # twice the same node position because we use zero-length elements
        bc_nodes.append(bc_pier_nodes)
    return bc_nodes
