"""Test scenario.py"""
from model.load import DisplacementCtrl
from model.scenario import TrafficScenario
from model.scenario import BridgeScenarioDisplacement, BridgeScenarioNormal


def test_scenario():
    [ts for ts in TrafficScenario]
    BridgeScenarioNormal()
    BridgeScenarioDisplacement(DisplacementCtrl(0.1, 1))
