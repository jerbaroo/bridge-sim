"""Test the sampling of vehicles."""
from data.normal.a16 import sample_vehicle
from model.bridge_705 import bridge_705_config

def test_sample_vehicle():
    c = bridge_705_config()
    vehicle = sample_vehicle(c)
    print(vehicle)
