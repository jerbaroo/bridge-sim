"""Plot responses from simulation."""
from typing import List, Optional

import numpy as np
import matplotlib.pyplot as plt

from bridge_sim.model import Config, Vehicle
from lib.plot.responses import plot_contour_deck as contour_responses
from lib.plot.geometry import shells, top_view_bridge

__all__ = ["contour_responses", "top_view_bridge"]

from matplotlib import colors, patches as patches


def equal_lims(axis, rows, cols, subplots=None):
    """Set equal x or y limits on subplots."""
    amin, amax = np.inf, -np.inf
    lim_f = plt.ylim if axis == "y" else plt.xlim
    subplots = range(1, rows * cols + 1) if subplots is None else subplots
    for p in subplots:
        plt.subplot(rows, cols, p)
        if lim_f()[0] < amin:
            amin = lim_f()[0]
        if lim_f()[1] > amax:
            amax = lim_f()[1]
    for p in subplots:
        plt.subplot(rows, cols, p)
        lim_f((amin, amax))


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """A truncated version of the given Matplotlib colormap."""
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def top_view_vehicles(
    config: Config,
    vehicles: List[Vehicle],
    time: float,
    all_vehicles: Optional[List[Vehicle]] = None,
    wheels: bool = False,
):
    """Plot vehicles on a bridge in top view at a given time.

    Args:
        config: simulation configuration object.
        vehicles: vehicles currently on the bridge.
        time: time at which to draw each vehicles.
        all_vehicles: vehicles from which to derive
            color scale, if None defaults to "vehicles".
        wheels: plot each wheel as a black dot?

    """
    if all_vehicles is None:
        all_vehicles = vehicles
    for vehicle in vehicles:
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
            for load in points_loads:
                plt.scatter([load.x], [load.z], c="black", s=2, zorder=10)
