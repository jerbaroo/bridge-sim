"""Test model.scenario and classify.data.scenarios."""
from classify.data.scenarios import BridgeScenarioDisplacementCtrl, BridgeScenarioNormal, normal_traffic, heavy_traffic
from model.load import DisplacementCtrl, MvVehicle
from model.scenario import TrafficScenario
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_test_config


def test_scenario():
    # TODO: Fix & test heavy traffic.
    c = bridge_705_test_config(bridge_705_2d)

    traffic_scenarios = [normal_traffic(c)]
    for traffic_scenario in traffic_scenarios:
        assert isinstance(traffic_scenario.name, str)
        vehicle_and_dist = traffic_scenario.mv_vehicle_f()
        assert isinstance(vehicle_and_dist[0], MvVehicle)
        assert (isinstance(vehicle_and_dist[1], float) or
                isinstance(vehicle_and_dist[1], int))

        lane = 0
        mv_vehicles_gen = traffic_scenario.mv_vehicles(lane=lane)
        last_init_x_frac = 0.00000001
        for mv_vehicle in [next(mv_vehicles_gen) for _ in range(3)]:
            assert isinstance(mv_vehicle, MvVehicle)
            assert mv_vehicle.lane == lane
            assert mv_vehicle.init_x_frac < last_init_x_frac
            last_init_x_frac = mv_vehicle.init_x_frac

    BridgeScenarioNormal()
    BridgeScenarioDisplacementCtrl(
        displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1))
