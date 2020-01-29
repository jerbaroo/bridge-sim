"""Test model.scenario and classify.data.scenarios."""
from timeit import default_timer as timer

from classify.scenario.bridge import HealthyDamage, PierDispDamage
from classify.scenario.traffic import heavy_traffic_1, normal_traffic
from model.load import PierSettlement, MvVehicle
from model.scenario import TrafficScenario, to_traffic, to_traffic_array
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from util import print_i
from vehicles.sample import sample_vehicle

c = bridge_705_config(bridge_705_3d)


def test_traffic_sequence():
    max_time = 10
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, warmed_up_at = traffic_scenario.traffic_sequence(
        bridge=c.bridge, max_time=max_time
    )
    # Time the simulation has warmed up at should be when the first vehicle has
    # left the bridge. Since all vehicles have the same speed, this should at
    # least be greater than the time any vehicle takes until it has begun to
    # leave the bridge (first axle leaving), but depending on vehicle length the
    # time to have entirely have left will be a little different per vehicle.
    vehicle = next(traffic_scenario.mv_vehicles(bridge=c.bridge, lane=0))(0, 0)
    assert warmed_up_at > vehicle.time_leaving_bridge(c.bridge)
    first_vehicle, first_time, first_event = traffic_sequence[0]
    # Time of the first event should be 0, when the first vehicle enters.
    assert first_time == 0
    penul_vehicle, penul_time, penul_event = traffic_sequence[-2]
    final_vehicle, final_time, final_event = traffic_sequence[-1]
    # Time of the last event should be greater than the requested 'max_time' +
    # the time the simulation has 'warmed_up_at', and the second last event
    # should be before less than.
    assert penul_time < max_time + warmed_up_at < final_time


def test_to_traffic_array():
    max_time = 10
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, warmed_up_at = traffic_scenario.traffic_sequence(
        bridge=c.bridge, max_time=max_time
    )
    traffic_array = to_traffic_array(
        c=c,
        traffic_sequence=traffic_sequence,
        warmed_up_at=warmed_up_at,
        max_time=max_time,
    )


# def test_scenario():


#     traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
#     assert isinstance(traffic_scenario.name, str)
#     vehicle_and_dist = traffic_scenario.mv_vehicle_f(time=0, full_lanes=0)
#     assert isinstance(vehicle_and_dist[0], MvVehicle)
#     assert isinstance(vehicle_and_dist[1], float) or isinstance(
#         vehicle_and_dist[1], int
#     )

#     lane = 0
#     # A generator for traffic on one lane.
#     mv_vehicles_gen = traffic_scenario.mv_vehicles(bridge=c.bridge, lane=lane)
#     last_init_x_frac = 0.00000001
#     for mv_vehicle in [next(mv_vehicles_gen)(0, 0) for _ in range(3)]:
#         assert isinstance(mv_vehicle, MvVehicle)
#         assert mv_vehicle.lane == lane
#         # The first 'init_x_frac' is -0, and subsequently decreasing.
#         assert mv_vehicle.init_x_frac < last_init_x_frac
#         last_init_x_frac = mv_vehicle.init_x_frac

#     # Simply check that no errors are created.
#     HealthyDamage()
#     PierDispDamage(displacement_ctrl=PierSettlement(displacement=0.1, pier=1))

#     # Time how long it takes to generate traffic.
#     start = timer()
#     max_time = 5
#     traffic_sequence, start_time = traffic_scenario.traffic_sequence(
#         bridge=c.bridge, max_time=max_time
#     )
#     print_i(
#         f"Generation of {start_time + max_time}s of TrafficSequence took"
#         + f" {timer() - start}"
#     )

#     time_step = 0.01
#     start = timer()
#     traffic = to_traffic(
#         bridge=c.bridge,
#         traffic_sequence=traffic_sequence,
#         max_time=start_time + max_time,
#         time_step=time_step,
#     )
#     # '- 1' because the first time step is t = 0.
#     sim_time = (len(traffic) - 1) * time_step
#     print_i(
#         f"Generation of {sim_time}s of Traffic at {1 / time_step}Hz"
#         + f" ({len(traffic)} steps) took {timer() - start}"
#     )

#     start = timer()
#     traffic_array = to_traffic_array(
#         c=c,
#         traffic_sequence=traffic_sequence,
#         max_time=start_time + max_time,
#         time_step=time_step,
#     )
#     # '- 1' because the first time step is t = 0.
#     sim_time = (len(traffic_array) - 1) * time_step
#     print_i(
#         f"Generation of {sim_time}s of TrafficArray at {1 / time_step}Hz"
#         + f" ({len(traffic)} steps) took {timer() - start}"
#     )

#     from classify.data.responses import (
#         responses_to_traffic_array,
#         responses_to_traffic,
#     )
#     from fem.run.opensees import OSRunner
#     from model.bridge import Point
#     from model.response import ResponseType

#     points = [Point(x=35, y=0, z=9.4)]
#     responses = responses_to_traffic_array(
#         c=c,
#         traffic_array=traffic_array,
#         response_type=ResponseType.YTranslation,
#         points=points,
#         fem_runner=OSRunner(c),
#     )
#     print(responses.shape)

#     responses_2 = responses_to_traffic(
#         c,
#         traffic,
#         HealthyDamage(),
#         start_time=0,
#         time_step=time_step,
#         points=points,
#         response_type=ResponseType.YTranslation,
#         fem_runner=OSRunner(c),
#     )
#     responses_2 = [r.responses[0][35][0][9.4] for r in responses_2]

#     from plot import plt

#     plt.plot(responses.T[0])
#     plt.plot(responses_2)
#     plt.show()
