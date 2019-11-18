from typing import List

import numpy as np

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.data.traffic import load_traffic_array
from classify.scenario.bridge import HealthyBridge, PierDispBridge
from classify.scenario.traffic import normal_traffic
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.load import DisplacementCtrl
from model.response import ResponseType
from model.scenario import BridgeScenario
from plot.responses import plot_distributions


def load_normal_traffic_array(c: Config):
    """Distribution plots currently use this for normal traffic."""
    traffic_scenario = normal_traffic(c, 5, 2)
    return (load_traffic_array(
        c=c, traffic_scenario=traffic_scenario, max_time=60*5),
            traffic_scenario)


def distribution_plots(c: Config):
    """Make all distribution plots."""
    pier_disp_scenarios = [
        PierDispBridge(DisplacementCtrl(displacement=1, pier=pier_index))
        for pier_index, pier in enumerate(c.bridge.supports)
    ]
    lane_distribution_plots(
        c=c, bridge_scenarios=[HealthyBridge()] + pier_disp_scenarios,
        response_type=ResponseType.YTranslation)


def lane_distribution_plots(
        c: Config, bridge_scenarios: List[BridgeScenario],
        response_type: ResponseType, num: int=25):
    """For each 'BridgeScenario' plot response distributions along each lane.

    This is currently only for the normal traffic scenario, but can extend it.

    """
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)

    # For each bridge scenario and lane combination.
    for bridge_scenario in bridge_scenarios:
        for lane_index, lane in enumerate(c.bridge.lanes):

            # For the full lane.
            points = [
                Point(x=x, y=0, z=lane.z_center())
                for x in np.linspace(c.bridge.x_min, c.bridge.x_max / 2, num)]
            response_array = responses_to_traffic_array(
                c=c, traffic_array=normal_traffic_array,
                response_type=response_type, bridge_scenario=bridge_scenario,
                points=points, fem_runner=OSRunner(c))
            plot_distributions(
                response_array=response_array, response_type=response_type,
                titles=[
                    f"{response_type.name()}"
                    + f"\nat x, z = {point.x:.2f}, {point.z:2f}"
                    + f"\nunder {traffic_scenario.name}"
                    for point in points],
                save=c.get_image_path(
                    "distributions",
                    f"distributions-{traffic_scenario.name}"
                    + f"-{bridge_scenario.name}-lane-{lane_index}"))


# def make_distribution_plots(c: Config):
#     max_time, time_step, lam, min_d = 20, 0.01, 5, 2
#     points = [Point(x=35, y=0, z=8.4), Point(x=35, y=0, z=-8.4)]
#     response_type = ResponseType.YTranslation

#     # Generate heavy traffic.
#     heavy_traffic, start_index = heavy_traffic_1(
#         c=c, lam=lam, min_d=min_d, prob_heavy=0.01
#     ).traffic(bridge=c.bridge, max_time=max_time, time_step=time_step)

#     # Filter out any normal traffic so it's just one heavy vehicle.
#     for t, t_traffic in enumerate(heavy_traffic):
#         heavy_traffic[t] = [v for v in t_traffic if v.kn == 500]
#         assert len(heavy_traffic[t]) <= 1
#         print(len(heavy_traffic[t]))
#     assert any(len(t_traffic) == 1 for t_traffic in heavy_traffic)
#     assert len(heavy_traffic[-1]) == 0

#     heavy_responses = responses_to_traffic(
#         c=c,
#         traffic=heavy_traffic,
#         bridge_scenario=BridgeScenarioNormal(),
#         start_time=start_index * time_step,
#         time_step=time_step,
#         points=points,
#         response_type=response_type,
#         fem_runner=OSRunner(c),
#     )
#     heavy_responses_values = [
#         [r.responses[0][point.x][point.y][point.z] for r in heavy_responses]
#         for point in points
#     ]

#     # heavy_responses_values[0] = [r for r in heavy_responses_values[0] if r != 0]
#     # heavy_responses_values[1] = [r for r in heavy_responses_values[1] if r != 0]

#     print("first lane")
#     [print(v) for v in heavy_responses_values[0] if v != 0]
#     print("second lane")
#     [print(v) for v in heavy_responses_values[1] if v != 0]

#     plt.plot(heavy_responses_values[0])
#     plt.show()
#     plt.plot(heavy_responses_values[1])
#     plt.show()
