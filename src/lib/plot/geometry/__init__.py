"""Plot geometry of a bridge."""
import os
from typing import Optional

import matplotlib
from bridge_sim.model import Bridge, Config
from bridge_sim.sim.build import get_bridge_shells
from bridge_sim.sim.model import SimParams
from lib.plot import plt

# Print debug information for this file.
# D: str = "plot.geometry"
D: bool = False


def top_view_bridge(
    bridge: Bridge,
    abutments: bool = False,
    edges: bool = False,
    piers: bool = False,
    lanes: bool = False,
    lane_fill: bool = False,
    landscape: bool = True,
    compass: bool = False,
    units: Optional[str] = None,
):
    """Plot the top view of a bridge's geometry.

    Args:
        bridge: the bridge top to plot.
        landscape: orient the plot in landscape (16 x 10) ?
        abutments: plot the bridge's abutments?
        edges: plot the longitudinal edges?
        piers: plot where the piers connect to the deck?
        lanes: plot lanes on the bridge?
        lane_fill: plot fill or only outline?
        compass: plot a compass rose?
        units: units of bridge width and height (axes labels).

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
    units_str = "" if units is None else f" ({units})"
    plt.xlabel(f"X position{units_str}")
    plt.ylabel(f"Z position{units_str}")


def shells(config: Config, sim_params: SimParams = SimParams()):
    deck_shells, _pier_shells = get_bridge_shells(
        bridge=config.bridge, ctx=sim_params.build_ctx()
    )
    for shell in deck_shells:
        ni, nj, nk, nl = shell.nodes()
        plt.plot([ni.x, nj.x, nk.x, nl.x], [ni.z, nj.z, nk.z, nl.z], c="black", lw=0.1)
