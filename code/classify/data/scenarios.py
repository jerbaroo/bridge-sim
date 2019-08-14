"""Different scenarios for data generation."""
from model.scenario import TrafficScenario
from vehicles.sample import sample_vehicle

normal_traffic = TrafficScenario(name="normal", vehicle=sample_vehicle)
heavy_traffic = TrafficScenario(name="heavy", vehicle=None)
