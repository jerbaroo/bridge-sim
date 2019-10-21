"""Plot loads and vehicles in different views."""
from typing import List

import numpy as np

import matplotlib.cm as cm
import matplotlib.patches as patches
from matplotlib.colors import Normalize

from model.bridge import Bridge
from model.load import MvVehicle, PointLoad
from plot import Color, plt


def top_view_vehicles(bridge: Bridge, mv_vehicles: List[MvVehicle]):
    """Plot vehicles on a bridge in top view."""
    if len(mv_vehicles) > 0:
        cmap = cm.get_cmap("Reds")
        kns = [v.kn for v in mv_vehicles]
        norm = Normalize(vmin=min(kns), vmax=max(kns))
    for mv_vehicle in mv_vehicles:
        # Left position on x-axis of vehicle.
        xl = bridge.x(mv_vehicle.init_x_frac)
        z_center = bridge.lanes[mv_vehicle.lane].z_center()
        # Bottom position on z-axis of vehicle.
        zb = z_center - (mv_vehicle.axle_width / 2)
        plt.gca().add_patch(patches.Rectangle(
            (xl, zb), mv_vehicle.length, mv_vehicle.axle_width,
            facecolor=cmap(np.interp(norm(mv_vehicle.kn), [0, 1], [0.5, 1]))))
