"""Different scenarios for data generation."""
from model.scenario import TrafficScenario
from vehicles.sample import sample_vehicle

normal_traffic = TrafficScenario(name="normal", vehicle=sample_vehicle)
heavy_traffic = TrafficScenario(name="heavy", vehicle=None)

"""Idea for a Python library:

A dataclass X with a decorator, or a subclass of dataclass.

Creates a method with the same arguments getX, and if saved to a file return
it, else generates the data with a method makeX and save to a file.

"""
