"""Test model.scenario and classify.data.scenarios."""
from timeit import default_timer as timer

from classify.scenario.bridge import HealthyBridge, PierDispBridge
from classify.scenario.traffic import heavy_traffic_1, normal_traffic
from model.load import DisplacementCtrl, MvVehicle
from model.scenario import TrafficScenario
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from util import print_i


def test_scenario():

    c = bridge_705_test_config(bridge_705_3d)

    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    assert isinstance(traffic_scenario.name, str)
    vehicle_and_dist = traffic_scenario.mv_vehicle_f(
        traffic=[], time=0, full_lanes=0)
    assert isinstance(vehicle_and_dist[0], MvVehicle)
    assert (isinstance(vehicle_and_dist[1], float) or
            isinstance(vehicle_and_dist[1], int))

    lane = 0
    # A generator for traffic on one lane.
    mv_vehicles_gen = traffic_scenario.mv_vehicles(bridge=c.bridge, lane=lane)
    last_init_x_frac = 0.00000001
    for mv_vehicle in [next(mv_vehicles_gen)([], 0, 0) for _ in range(3)]:
        assert isinstance(mv_vehicle, MvVehicle)
        assert mv_vehicle.lane == lane
        # The first 'init_x_frac' is -0, and subsequently decreasing.
        assert mv_vehicle.init_x_frac < last_init_x_frac
        last_init_x_frac = mv_vehicle.init_x_frac

    # Simply check that no errors are created.
    HealthyBridge()
    PierDispBridge(
        displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1))

    # Time how long it takes to generate traffic.
    start = timer()
    max_time, time_step = 30, 0.01
    traffic, start_index = traffic_scenario.traffic(
        bridge=c.bridge, max_time=max_time, time_step=time_step)
    # '- 1' because the first time step is t = 0.
    sim_time = (len(traffic) - 1) * time_step
    # '+ 1' to include the time step at t = 0.
    sim_steps = (sim_time / time_step) + 1
    print_i(
        f"Generation of {sim_time}s of Traffic at {1 / time_step}Hz"
        + f" ({sim_steps} steps) took {timer() - start}")
