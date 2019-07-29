"""Test the sampling of vehicles."""
from data.normal.a16 import sample_vehicle
from model.bridge_705 import bridge_705_config

def test_sample_vehicle():
    c = bridge_705_config()
    c.vehicle_density = c.vehicle_density[2:]  # Ignore light vehicles.
    vehicle = sample_vehicle(c)
    print(vehicle)
