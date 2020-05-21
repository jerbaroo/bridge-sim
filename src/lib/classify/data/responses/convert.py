from typing import List

import numpy as np

from bridge_sim.model import Config
from bridge_sim.model.vehicle import PointLoad
from util import print_d

D: str = "classify.responses.convert"
D: bool = False


def x_to_wheel_track_index(c: Config):
    """Return a function from x position to wheel track index."""
    wheel_track_xs = c.bridge.wheel_track_xs(c)

    def wheel_track_index(x: float):
        wheel_x_ind = np.searchsorted(wheel_track_xs, x)
        if wheel_x_ind == 0:
            return wheel_x_ind
        wheel_x = wheel_track_xs[wheel_x_ind]
        wheel_x_lo = wheel_track_xs[wheel_x_ind - 1]
        if wheel_x_ind < len(wheel_track_xs) - 1:
            assert abs(x - wheel_track_xs[wheel_x_ind + 1]) > abs(x - wheel_x)
        if abs(x - wheel_x_lo) < abs(x - wheel_x):
            return wheel_x_ind - 1
        return wheel_x_ind

    return wheel_track_index


def loads_to_traffic_array(c: Config, loads: List[List[PointLoad]]):
    """Convert a list of loads per timestep to a 'TrafficArray'."""
    times = len(loads)
    wheel_track_zs = c.bridge.wheel_track_zs(c)
    num_load_positions = c.il_num_loads * len(wheel_track_zs)
    traffic_array = np.zeros((times, num_load_positions))
    wheel_track_index_f = x_to_wheel_track_index(c)
    for time, time_loads in enumerate(loads):
        # For each load, find the wheel track it's on, and then fill the ULM.
        for load in time_loads:
            wheel_track_found = False
            load_z = c.bridge.z(load.z_frac)
            for w, wheel_track_z in enumerate(wheel_track_zs):
                if not wheel_track_found and np.isclose(wheel_track_z, load_z):
                    wheel_track_found = True
                    load_x = c.bridge.x(load.x_frac)
                    print_d(D, f"load z = {load_z}")
                    print_d(D, f"load x = {load_x}")
                    x_ind = wheel_track_index_f(load_x)
                    j = (w * c.il_num_loads) + x_ind
                    print_d(D, f"x_ind = {x_ind}")
                    print_d(D, f"j = {j}")
                    traffic_array[time][j] += load.kn
            if not wheel_track_found:
                raise ValueError(f"No wheel track for point load at z = {load_z}")
    return traffic_array
