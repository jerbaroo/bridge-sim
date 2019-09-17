"""Test model.scenario and classify.data.scenarios."""
from classify.data.scenarios import BridgeScenarioDisplacementCtrl, BridgeScenarioNormal, normal_traffic, heavy_traffic
from model.load import DisplacementCtrl, MovingLoad, Vehicle
from model.scenario import TrafficScenario
from model.bridge.bridge_705 import bridge_705_test_config


def test_scenario():
    # TODO: Fix & test heavy traffic.
    c = bridge_705_test_config()

    traffic_scenarios = [normal_traffic(c)]
    for traffic_scenario in traffic_scenarios:
        assert isinstance(traffic_scenario.name, str)
        vehicle_and_dist = traffic_scenario.vehicle()
        assert isinstance(vehicle_and_dist[0], Vehicle)
        assert (isinstance(vehicle_and_dist[1], float) or
                isinstance(vehicle_and_dist[1], int))

        num_vehicles = 2
        lane = 0
        mv_loads = traffic_scenario.mv_loads(
            num_vehicles=num_vehicles, lane=lane)
        assert len(mv_loads) == num_vehicles
        last_x_frac = 0
        for mv_load in mv_loads:
            assert mv_load.load.lane == lane
            assert mv_load.load.x_frac <= last_x_frac
            last_x_frac = mv_load.load.x_frac
            assert isinstance(mv_load, MovingLoad)

    BridgeScenarioNormal()
    BridgeScenarioDisplacementCtrl(
        displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1))
