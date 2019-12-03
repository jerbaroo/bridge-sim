"""Plot geometry of a bridge."""
import os
from typing import Callable, List, Optional

import matplotlib.patches as patches
import numpy as np

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from config import Config
from fem.params import ExptParams, SimParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d, nodes_by_id
from model.bridge import Bridge, Section3D
from plot import Color, plt

# Print debug information for this file.
D: str = "plot.geom"
# D: bool = False


def top_view_bridge(
    bridge: Bridge,
    edges: bool = False,
    abutments: bool = False,
    piers: bool = False,
    lanes: bool = False,
    lane_fill: bool = False,
    landscape: bool = True,
    compass: bool = True,
):
    """Plot the top view of a bridge's geometry.

    Args:
        bridge: Bridge, the bridge top to plot.
        landscape: bool, whether to orient the plot in landscape.
        edges: bool, whether to plot the longitudinal edges.
        abutments: bool, whether to plot the bridge's abutments.
        piers: bool, whether to plot where the piers connect to the deck.
        lanes: bool, whether to plot lanes on the bridge.
        lane_fill: bool, whether to plot fill or only outline.
        compass: bool, whether to plot a compass rose.

    """
    if landscape:
        plt.landscape()
    plt.axis("equal")
    if edges:
        plt.hlines([bridge.z_min, bridge.z_max], 0, bridge.length)
    if abutments:
        plt.vlines([0, bridge.length], bridge.z_min, bridge.z_max)
    if piers:
        for pier in bridge.supports:
            z_min_top, z_max_top = pier.z_min_max_top()
            x_min, x_max = pier.x_min_max()
            plt.vlines([x_min, x_max], z_min_top, z_max_top)
    if lanes:
        for lane in bridge.lanes:
            plt.gca().add_patch(
                patches.Rectangle(
                    (0, lane.z_min),
                    bridge.length,
                    lane.z_max - lane.z_min,
                    facecolor="black" if lane_fill else "none",
                )
            )
    if compass:
        ax = plt.gca()  # Reference to the original axis.
        dir_path = os.path.dirname(os.path.abspath(__file__))
        compass_img = plt.imread(os.path.join(dir_path, "compass-rose.png"))
        c_len = max(bridge.width, bridge.length) * 0.2
        ax_c = ax.inset_axes(
            [0, bridge.z_max + (c_len * 0.05), c_len, c_len],
            transform=ax.transData,
        )
        ax_c.imshow(compass_img)
        ax_c.axis("off")
        plt.sca(ax)  # Return control to the original axis.
    plt.xlabel("x position (m)")
    plt.ylabel("z position (m)")


def plot_cloud_of_nodes(
    c: Config,
    equal_axis: bool,
    save: str,
    node_prop: Optional[Callable[[Section3D], float]] = None,
    deck: bool = True,
    piers: bool = True,
):
    """A scatter plot of the nodes of a 3D FEM."""
    # TODO: Create method for these three lines in d3/__init__.py
    build_model_3d(
        c=c, expt_params=ExptParams([SimParams([], [])]), os_runner=OSRunner(c)
    )
    nodes = list(nodes_by_id.values())

    # This is a sanity check (or a test in the wrong place) that all nodes that
    # belong to a pier also belong to a shell element on the pier. And that all
    # nodes that belong only to the deck also belong to a shell element on the
    # deck. Any node that belongs to a shell element will have a section
    # assigned, either as deck_dection or pier_section.
    for node in nodes:
        if node.pier is not None:
            assert hasattr(node, "pier_section")
        else:
            assert hasattr(node, "deck_section")

    nodes = [
        n
        for n in nodes
        if (deck and n.deck) or (piers and (n.pier is not None))
    ]
    nodes = sorted(nodes, key=lambda n: (n.deck, not n.pier))

    # Split into separate arrays of x, y and z position, and colors.
    xs = np.array([n.x for n in nodes])
    ys = np.array([n.y for n in nodes])
    zs = np.array([n.z for n in nodes])
    cs = None
    if node_prop is not None:
        cs = []
        for node in nodes:
            if deck and piers:
                # If both deck and pier Nodes are requested, and a Node belongs
                # to both then we prioritize the deck section.
                cs.append(
                    node.deck_section
                    if hasattr(node, "deck_section")
                    else node.pier_section
                )
            else:
                cs.append(node.deck_section if deck else node.pier_section)
        cs = np.array([node_prop(section) for section in cs])

    def plot_and_save(fig, ax, append: str = ""):
        """Plot the cloud of points with optional additional operation."""
        plt.set_cmap("coolwarm")
        p = ax.scatter(xs, zs, ys, c=cs, s=1)
        if cs is not None:
            fig.colorbar(p)
        deck_str = "-deck" if deck else ""
        piers_str = "-piers" if piers else ""
        plt.savefig(f"{save}{deck_str}{piers_str}{append}")

    equal_axis_str = "-equalaxis" if equal_axis else "-fullaxis"

    for fig, ax, angle in angles_3d(equal_axis=equal_axis, xs=xs, ys=ys, zs=zs):
        plot_and_save(fig, ax, append=equal_axis_str + f"-no-rotate")

    for fig, ax, angle in angles_3d(
        angles=range(0, 360, 90),
        equal_axis=equal_axis,
        elev=0,
        xs=xs,
        ys=ys,
        zs=zs,
    ):
        plot_and_save(fig, ax, append=equal_axis_str + f"-{angle}")


def angles_3d(
    equal_axis: bool,
    xs: List[float],
    ys: List[float],
    zs: List[float],
    angles: Optional[List[float]] = None,
    elev: Optional[float] = None,
):
    """Rotate a plot in 3D, yielding the axis and angle.

    Args:
        angles: Optional[List[float]], angles to plot at, if None use default.
        elev: Optional[float], elevation used if 'angles' is given.
    """
    # Determine values for scaling axes.
    max_range = (
        np.array(
            [xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()]
        ).max()
        / 2.0
    )
    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5

    # Ensure at least one angle in default case.
    if angles is None:
        angles = [None]
    # Plot for different angles.
    for ii in angles:
        plt.close()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
        if equal_axis:
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        if ii is not None:
            ax.view_init(elev=elev, azim=ii)
        yield fig, ax, ii
