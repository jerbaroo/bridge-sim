"""Plot responses from simulation."""

import itertools
import os
from typing import List, Optional, Tuple, Callable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches as patches

from bridge_sim.internal.plot import default_cmap, plt, axis_cmap_r
from bridge_sim.model import Config, Vehicle, PointLoad, Point, Bridge
from bridge_sim.sim.build import get_bridge_shells
from bridge_sim.sim.model import Responses, SimParams, Shell

import bridge_sim.plot.animate as animate


def top_view_vehicles(
    config: Config,
    vehicles: List[Vehicle],
    time: float,
    all_vehicles: Optional[List[Vehicle]] = None,
    wheels: bool = False,
    body: bool = True,
    label_wheels: bool = True,
):
    """Plot vehicles on a bridge in top view at a given time.

    Args:
        config: simulation configuration object.
        vehicles: vehicles currently on the bridge.
        time: time at which to draw each vehicles.
        all_vehicles: vehicles from which to derive
            color scale, if None defaults to "vehicles".
        wheels: plot each wheel as a black dot?
        body: plot the body of the vehicle?
        label_wheels: add a legend label for the wheels?

    """
    if all_vehicles is None:
        all_vehicles = vehicles
    for v_i, vehicle in enumerate(vehicles):
        if body:
            # Left-most position of each vehicles axle.
            xl = min(vehicle.xs_at(times=[time], bridge=config.bridge)[0])
            # Center of the lane.
            z_center = config.bridge.lanes[vehicle.lane].z_center
            # Bottom position on z-axis of vehicles.
            zb = z_center - (vehicle.axle_width / 2)
            # Length, not allowed to extend beyond the bridge.
            length = vehicle.length
            if xl + length <= config.bridge.x_min:
                continue
            if xl >= config.bridge.x_max:
                continue
            if xl < config.bridge.x_min:
                length -= abs(config.bridge.x_min - xl)
                xl = config.bridge.x_min
            if xl + length > config.bridge.x_max:
                length -= abs(xl + length - config.bridge.x_max)
            plt.gca().add_patch(
                patches.Rectangle(
                    (xl, zb),
                    length,
                    vehicle.axle_width,
                    facecolor=vehicle.color(all_vehicles),
                )
            )
        if wheels:
            points_loads = vehicle.point_load_pw(config, time, list=True)
            for l_i, load in enumerate(points_loads):
                plt.scatter(
                    [load.x],
                    [load.z],
                    c="black",
                    s=5,
                    zorder=10,
                    label=(
                        None if (not label_wheels or v_i > 0 or l_i > 0) else "wheels"
                    ),
                )


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
    set_lims: bool = False,
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
        set_lims: increase plot limits to bridge edges and abutments.

    """
    if set_lims:
        x_min, x_max = plt.xlim()
        plt.xlim(min(x_min, bridge.x_min), max(x_max, bridge.x_max))
        y_min, y_max = plt.ylim()
        plt.ylim(min(y_min, bridge.z_min), max(y_max, bridge.z_max))
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
                patches.Rectangle(
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


def contour_responses(
    config: Config,
    responses: Responses,
    point_loads: List[PointLoad] = [],
    cmap=axis_cmap_r,
    norm=None,
    scatter: bool = False,
    levels: int = 14,
    interp: Optional[Tuple[int, int]] = None,
    mm_legend: bool = True,
    mm_legend_without_f: Optional[Callable[[Point], bool]] = None,
    sci_format: bool = False,
    decimals: int = 4,
    cbar: bool = True,
):
    """Contour or scatter plot of simulation responses.

    Args:
        config: simulation configuration object.
        responses: the simulation responses to plot.
        point_loads: point loads to plot (black dots).
        cmap: Matplotlib colormap to use for colouring responses.
        norm: Matplotlib norm to use for colouring responses.
        scatter: scatter plot instead of contour plot?
        levels: levels in the contour plot.
        interp: interpolate responses onto an n x m grid.
        mm_legend: plot a legend of min and max values?
        mm_legend_without_f: function to filter points considered in the legend.
        sci_format: force scientific formatting (E) in the legend.
        decimals: round legend values to this many decimals.
        cbar: add a colorbar?

    """
    if interp:
        points = [
            Point(x=x, z=z)
            for x, z, in list(
                itertools.product(
                    np.linspace(config.bridge.x_min, config.bridge.x_max, interp[0]),
                    np.linspace(config.bridge.z_min, config.bridge.z_max, interp[1]),
                )
            )
        ]
        responses = Responses(
            response_type=responses.response_type,
            responses=list(zip(responses.at_decks(points), points)),
            units=responses.units,
        ).without_nan_inf()

    amax, amax_x, amax_z = -np.inf, None, None
    amin, amin_x, amin_z = np.inf, None, None
    X, Z, H = [], [], []  # X and Z coordinates, and height.

    def structure_data(responses):
        nonlocal amax, amax_x, amax_z, amin, amin_x, amin_z
        nonlocal X, Z, H
        for h, (x, y, z) in responses.values(point=True):
            X.append(x)
            Z.append(z)
            H.append(h)
            if H[-1] > amax:
                amax = H[-1]
                amax_x, amax_z = X[-1], Z[-1]
            if H[-1] < amin:
                amin = H[-1]
                amin_x, amin_z = X[-1], Z[-1]

    structure_data(responses)
    if len(X) == 0:
        raise ValueError(f"No fem for contour plot")

    # Plot fem, contour or scatter plot.
    if scatter:
        cs = plt.scatter(x=X, y=Z, c=H, cmap=cmap, norm=norm, s=1)
    else:
        cs = plt.tricontourf(X, Z, H, levels=levels, cmap=cmap, norm=norm)

    # Colourbar, maybe using given norm.
    if cbar:
        clb = plt.colorbar(cs, norm=norm)
        if responses.units is not None:
            clb.ax.set_title(responses.units)

    # Plot point loads.
    for pload in point_loads:
        unit_str = "" if pload.units is None else f" {pload.units}"
        plt.scatter(
            [pload.x],
            [pload.z],
            label=f"{pload.load}{unit_str} load",
            marker="o",
            color="black",
        )

    # Begin: min, max legend.
    if mm_legend or mm_legend_without_f is not None:
        if mm_legend_without_f is not None:
            structure_data(responses.without(mm_legend_without_f))
        # Plot min and max fem.
        amin_s = (
            f"{amin:.{decimals}g}" if sci_format else f"{np.around(amin, decimals)}"
        )
        amax_s = (
            f"{amax:.{decimals}g}" if sci_format else f"{np.around(amax, decimals)}"
        )
        aabs_s = (
            f"{amin - amax:.{decimals}g}"
            if sci_format
            else f"{np.around(abs(amin - amax), decimals)}"
        )
        units_str = "" if responses.units is None else f" {responses.units}"
        for point, label, color, alpha in [
            ((amin_x, amin_z), f"min = {amin_s}{units_str}", "orange", 0),
            ((amax_x, amax_z), f"max = {amax_s}{units_str}", "green", 0),
            ((amin_x, amin_z), f"|min-max| = {aabs_s}{units_str}", "red", 0),
        ]:
            plt.scatter(
                [point[0]],
                [point[1]],
                label=label,
                marker="o",
                color=color,
                alpha=alpha,
            )
    # End: min, max legend.


def shells(
    config: Config,
    sim_params: SimParams = SimParams(),
    lw: float = 0.1,
    color_f: Callable[[Shell], float] = None,
    cmap=axis_cmap_r,
    norm=None,
    ret_cmap_norm: bool = False,
):
    """Plot a bridge deck's shells.

    Args:
        config: simulation configuration object.
        sim_params: the built model (and shells) depend on this.
        color_f: function from shell to color.
        cmap: Matplotlib colormap for shell facecolours.
        norm: Matplotlib norm to use, else scale color_f across all shells.
        ret_cmap_norm: return a tuple of cmap and norm.

    """
    deck_shells, _pier_shells = get_bridge_shells(
        bridge=config.bridge, ctx=sim_params.build_ctx()
    )
    c_min, c_max = np.inf, -np.inf
    if color_f:
        for shell in deck_shells:
            c = color_f(shell)
            if c < c_min:
                c_min = c
            if c > c_max:
                c_max = c
        if norm is None:
            norm = mpl.colors.Normalize(vmin=c_min, vmax=c_max)
    for shell in deck_shells:
        ni, nj, nk, nl = shell.nodes()
        plt.gca().add_patch(
            patches.Rectangle(
                (ni.x, ni.z),
                nj.x - ni.x,
                nl.z - ni.z,
                linewidth=lw,
                edgecolor="black",
                facecolor=cmap(norm(color_f(shell))) if color_f else "none",
            )
        )
    if ret_cmap_norm:
        return cmap, norm
