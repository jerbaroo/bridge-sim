"""Scenarios for the traffic and bridge."""
from typing import Callable, Tuple

from config import Config
from model.load import MovingLoad, Vehicle


class TrafficScenario:
    """A named traffic scenario that generates moving loads.

    The vehicle function must return a tuple of a Vehicle and the distance in
    meters to the vehicle in front at time t=0 (when the simulation starts).

    """
    def __init__(
            self, c: Config, name: str,
            vehicle: Callable[[Config], Tuple[Vehicle, float]]):
        self.c = c
        self.name = name
        self.vehicle = lambda: vehicle(self.c)

    def mv_loads(self, num_vehicles: int, lane: int):
        """A number of moving loads under this traffic scenario."""
        mv_loads = []
        dist = 0  # In meters.
        for _ in range(num_vehicles):
            vehicle, inter_vehicle_dist = self.vehicle()
            mv_loads.append(MovingLoad.from_vehicle(
                x_frac=-self.c.bridge.x_frac(x=dist),
                vehicle=vehicle,
                lane=lane))
            dist += inter_vehicle_dist
            dist += vehicle.length
        return mv_loads


class BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    def __init__(self, name: str):
        self.name = name
