"""Scenarios for the traffic and bridge."""
from typing import Callable

from model.load import DisplacementCtrl, Vehicle


class TrafficScenario:
    """A named traffic scenario that generates vehicles."""
    def __init__(self, name: str, vehicle: Callable[[Config], Vehicle]):
        self.name = name
        self.vehicle = vehicle


class _BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    pass


class BridgeScenarioNormal(_BridgeScenario):
    pass


class BridgeScenarioDisplacement(_BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        self.displacement_ctrl = displacement_ctrl
