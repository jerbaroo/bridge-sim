"""Scenarios for the traffic and bridge."""
from typing import Callable, Tuple

from config import Config
from model.load import Vehicle


class TrafficScenario:
    """A named traffic scenario that generates vehicles.

    The vehicle function must return a tuple of a Vehicle and the distance in
    meters to the vehicle in front.
    """
    def __init__(
            self, name: str,
            vehicle: Callable[[Config], Tuple[Vehicle, float]]):
        self.name = name
        self.vehicle = vehicle


class BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    def __init__(self, name: str):
        self.name = name
