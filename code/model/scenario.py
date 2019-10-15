"""Scenarios for the traffic and bridge."""
from typing import Callable, Tuple

from config import Config
from model.load import MvVehicle


class TrafficScenario:
    """A named traffic scenario that generates moving vehicles.

    Args:
        c: Config, global configuration object.
        name: str, the name of this traffic scenario.
        mv_vehicle_F: Callable[[], Tuple[MvVehicle]], function that returns a
            tuple 'MvVehicle' and distance in meters to the vehicle in front at
            time t=0, note that the position ('lane' and 'init_x_frac') of this
            'MvVehicle' will be overridden.

    """
    def __init__(
            self, c: Config, name: str,
            mv_vehicle_f: Callable[[], Tuple[MvVehicle, float]]):
        self.c = c
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, lane: int):
        """Yield moving vehicles under this traffic scenario.

        The first vehicle will start at 'init_x_frac' 0 if traffic on the lane
        moves from left to right, otherwise at bridge length if from right to.
        left

        Args:
            lane: int, index of a lane on the bridge.

        """
        dist = 0  # In meters.
        while True:
            mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f()
            mv_vehicle.lane = lane
            mv_vehicle.init_x_frac = -self.c.bridge.x_frac(x=dist)
            yield mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length


class BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    def __init__(self, name: str):
        self.name = name
