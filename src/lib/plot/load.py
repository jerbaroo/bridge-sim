"""Plot loads and vehicles in different views."""
from typing import List, Optional

import matplotlib.patches as patches
import numpy as np

from model.bridge import Bridge
from model.load import MvVehicle, PointLoad, Vehicle
from plot import Color, plt


def top_view_vehicles(
    bridge: Bridge,
    mv_vehicles: List[MvVehicle],
    time: float,
    all_vehicles: Optional[List[Vehicle]] = None,
):
    """Plot vehicles on a bridge in top view at a given time.

    Args:
        bridge: Bridge, bridge on which to draw the vehicles.
        mv_vehicles: List[MvVehicle], vehicles currently on the bridge.
        time: float, time at which to draw each vehicles.
        all_vehicles: Optional[List[Vehicle]], vehicles from which to derive
            color scale, if None default is 'mv_vehicles'.

    """
    if all_vehicles is None:
        all_vehicles = mv_vehicles
    for mv_vehicle in mv_vehicles:
        # Left-most position of each vehicles axle.
        xl = min(mv_vehicle.xs_at(time=time, bridge=bridge))
        # Center of the lane.
        z_center = bridge.lanes[mv_vehicle.lane].z_center
        # Bottom position on z-axis of vehicles.
        zb = z_center - (mv_vehicle.axle_width / 2)
        # Length, not allowed to extend beyond the bridge.
        length = mv_vehicle.length
        if xl + length <= bridge.x_min:
            continue
        if xl >= bridge.x_max:
            continue
        if xl < bridge.x_min:
            length -= abs(bridge.x_min - xl)
            xl = bridge.x_min
        if xl + length > bridge.x_max:
            length -= abs(xl + length - bridge.x_max)
        plt.gca().add_patch(
            patches.Rectangle(
                (xl, zb),
                length,
                mv_vehicle.axle_width,
                facecolor=mv_vehicle.color(all_vehicles),
            )
        )
