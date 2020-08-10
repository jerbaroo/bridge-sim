from typing import List

import numpy as np

from bridge_sim.internal.plot import plt
from bridge_sim.internal.plot.geometry.angles import ax_3d
from bridge_sim.sim.model import Node


def node_scatter_3d(nodes: List[Node], new_fig: bool = True):
    # Split into separate arrays of x, y and z position, and colors.
    xs = np.array([n.x for n in nodes])
    ys = np.array([n.y for n in nodes])
    zs = np.array([n.z for n in nodes])

    # Setup a new 3D landscape figure.
    if new_fig:
        fig, ax = ax_3d(xs=xs, ys=zs, zs=ys)
    else:
        ax = plt.gca()

    ax.scatter(xs, zs, ys, marker="o", s=1)
