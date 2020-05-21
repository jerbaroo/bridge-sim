"""Plot geometry of a bridge."""
import os

import matplotlib
from bridge_sim.model.config import Config
from lib.plot import plt

# Print debug information for this file.
D: str = "plot.geometry"
# D: bool = False


def top_view_bridge(
    config: Config,
    edges: bool = False,
    abutments: bool = False,
    piers: bool = False,
    lanes: bool = False,
    lane_fill: bool = False,
    landscape: bool = True,
    compass: bool = False,
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
    bridge = config.bridge
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
            x_min, x_max = pier.x_min_max_top()
            plt.vlines([x_min, x_max], z_min_top, z_max_top)
    if lanes:
        for lane in bridge.lanes:
            plt.gca().add_patch(
                matplotlib.patches.Rectangle(
                    (0, lane.z_min),
                    bridge.length,
                    lane.z_max - lane.z_min,
                    facecolor="black" if lane_fill else "none",
                    edgecolor="black",
                )
            )
    if compass:
        ax = plt.gca()  # Reference to the original axis.
        dir_path = os.path.dirname(os.path.abspath(__file__))
        compass_img = plt.imread(os.path.join(dir_path, "compass-rose.png"))
        c_len = max(bridge.width, bridge.length) * 0.2
        ax_c = ax.inset_axes(
            [0, bridge.z_max + (c_len * 0.05), c_len, c_len], transform=ax.transData,
        )
        ax_c.imshow(compass_img)
        ax_c.axis("off")
        plt.sca(ax)  # Return control to the original axis.
    plt.xlabel("X position")
    plt.ylabel("Z position")
