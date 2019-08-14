"""Scenarios for the traffic and bridge."""
from enum import Enum

from model.load import DisplacementCtrl


class TrafficScenario(Enum):
    Normal = "Normal"
    Heavy = "Heavy"


class _BridgeScenario:
    pass


class BridgeScenarioNormal(_BridgeScenario):
    pass


class BridgeScenarioDisplacement(_BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        self.displacement_ctrl = displacement_ctrl
