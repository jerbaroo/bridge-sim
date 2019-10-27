"""Plot geometry of a bridge."""
from typing import Callable, Optional

import matplotlib.patches as patches
import numpy as np
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from config import Config
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.common import Node
from fem.run.opensees.build.d3 import build_model_3d, nodes_by_id
from model.bridge import Bridge, Section3D
from model.load import PointLoad
from plot import Color, plt
from util import print_d, print_w

# Print debug information for this file.
D: str = "plot.bridge"
# D: bool = False


def top_view_bridge(
        bridge: Bridge, lanes: bool = True, lane_fill: bool = True, piers: bool=True):
    """Plot the top view of a bridge's geometry.

    Args:
        bridge: Bridge, the bridge top to plot.
        lanes: bool, whether to plot lanes on the bridge.
        lane_fill: bool, whether to plot fill or only outline.
        piers: bool, whether to plot where the piers connect to the deck.

    """
    plt.hlines(
        [bridge.z_min, bridge.z_max], 0, bridge.length, color=Color.bridge)
    plt.vlines(
        [0, bridge.length], bridge.z_min, bridge.z_max, color=Color.bridge)
    if lanes:
        for lane in bridge.lanes:
            plt.gca().add_patch(patches.Rectangle(
                (0, lane.z_min), bridge.length, lane.z_max - lane.z_min,
                edgecolor=Color.bridge,
                facecolor=Color.bridge if lane_fill else "none"))
    if piers:
        for pier in bridge.supports:
            z_min_top, z_max_top = pier.z_min_max_top()
            x_min, x_max = pier.x_min_max()
            plt.vlines([x_min, x_max], z_min_top, z_max_top)
    plt.axis("equal")
    plt.xlabel("x position (m)")
    plt.ylabel("z position (m)")


def plot_cloud_of_nodes(
        c: Config, equal_axis: bool = False,
        node_prop: Optional[Callable[[Section3D], float]] = None,
        deck: bool = True, piers: bool = True, save: Optional[str] = None, show: bool = False):
    """A scatter plot of the nodes of a 3D FEM."""
    # TODO: Create method for these three lines in d3/__init__.py
    build_model_3d(c=c, expt_params=ExptParams([FEMParams(
        [PointLoad(0.1, 0.1, 100)], [])]), os_runner=OSRunner(c))
    nodes = list(nodes_by_id.values())
    print(len(nodes))

    print_w(f"Total amount of nodes = {len(nodes)}")
    nodes = [n for n in nodes if (deck and n.deck) or (piers and (n.pier is not None))]
    print_w(f"Total amount of nodes = {len(nodes)}")

    # Split into separate arrays of x, y and z position, and colors.
    xs = np.array([n.x for n in nodes])
    ys = np.array([n.y for n in nodes])
    zs = np.array([n.z for n in nodes])
    assert all(n.foobar for n in nodes)
    cs = None if node_prop is None else np.array([
        node_prop(n.deck_section if deck else n.pier_section) for n in nodes])

    # Axis to be referenced by function f in plot_and_save.
    ax = None

    # Determine values for scaling axes.
    max_range = np.array(
        [xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()]
    ).max() / 2.0
    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5

    def plot_and_save(f: Callable[[], None], append: str = ""):
        """Plot the cloud of points with optional additional operation.

        Args:
            f: Callable[[], None], additional operation called before plotting.
            append: str, string to append to the file name.

        """
        fig = plt.figure()
        nonlocal ax
        ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
        f()
        # TODO: Move this to plot module.
        plt.set_cmap("coolwarm")
        p = ax.scatter(xs, zs, ys, c=cs, s=1)
        if equal_axis:
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        if cs is not None:
            fig.colorbar(p)
        deck_str = "-deck" if deck else ""
        piers_str = "-piers" if piers else ""
        if save: plt.savefig(f"{save}{deck_str}{piers_str}{append}")
        if show: plt.show()
        if save or show: plt.close()

    equal_axis_str = "equal-axis" if equal_axis else "full-axis"
    # Plot without angle change.
    plot_and_save(lambda: None, append=equal_axis_str + "no-rotation")

    # Plot for different angles.
    for ii in range(0, 360, 90):
        plot_and_save(
            f=lambda: ax.view_init(elev=0, azim=ii),
            append=equal_axis_str + f"-{ii}")
