"""Plot loads and vehicles in different views."""
from typing import List

import matplotlib.patches as patches
import numpy as np

from model.bridge import Bridge
from model.load import MvVehicle, PointLoad, Vehicle
from plot import Color, plt


def top_view_vehicles(
        bridge: Bridge, mv_vehicles: List[MvVehicle],
        all_vehicles: List[Vehicle], time: float):
    """Plot vehicles on a bridge in top view at a given time.

    Args:
        bridge: Bridge, bridge on which to draw the vehicles.
        mv_vehicles: List[MvVehicle], vehicles currently on the bridge.
        all_vehicles: List[Vehicle], vehicles from which to derive color scale.
        time: float, time at which to draw each vehicle.

    """
    for mv_vehicle in mv_vehicles:
        # Left-most position of each vehicle axle.
        print(f"time = {time}")
        xl = min(mv_vehicle.xs_at(time=time, bridge=bridge))
        # Center of the lane.
        z_center = bridge.lanes[mv_vehicle.lane].z_center()
        # Bottom position on z-axis of vehicle.
        zb = z_center - (mv_vehicle.axle_width / 2)
        plt.gca().add_patch(patches.Rectangle(
            (xl, zb), mv_vehicle.length, mv_vehicle.axle_width,
            facecolor=mv_vehicle.color(all_vehicles)))
