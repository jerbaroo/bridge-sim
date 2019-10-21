"""Plot loads and vehicles in different views."""
from typing import List

import matplotlib.patches as patches

from model.bridge import Bridge
from model.load import MvVehicle, PointLoad
from plot import Color, plt


def top_view_vehicles(bridge: Bridge, mv_vehicles: List[MvVehicle]):
    """Plot vehicles on a bridge in top view."""
    for mv_vehicle in mv_vehicles:
        # Left position on x-axis of vehicle.
        xl = bridge.x(mv_vehicle.init_x_frac)
        z_center = bridge.lanes[mv_vehicle.lane].z_center()
        # Bottom position on z-axis of vehicle.
        zb = z_center - (mv_vehicle.axle_width / 2)
        print(
            f"xl = {xl}, zb = {zb}, length = {mv_vehicle.length}, width = {mv_vehicle.axle_width}")
        plt.gca().add_patch(patches.Rectangle(
            (xl, zb), mv_vehicle.length, mv_vehicle.axle_width,
            facecolor=Color.load))
