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
from model.response import ResponseType, resize_units
from model.scenario import BridgeScenario
from plot.responses import plot_distributions
from util import safe_str


def load_normal_traffic_array(c: Config):
    """Distribution plots currently use this for normal traffic."""
    traffic_scenario = normal_traffic(c, 5, 2)
    return (load_traffic_array(
        c=c, traffic_scenario=traffic_scenario, max_time=60*5),
            traffic_scenario)


# Each pier displaced by 1mm.
pier_disp_scenarios = lambda c: [
    PierDispBridge(DisplacementCtrl(displacement=0.001, pier=pier_index))
    for pier_index, pier in enumerate(c.bridge.supports)
]


def distribution_plots(c: Config):
    """Make all distribution plots."""
    lane_distribution_plots(
        c=c, bridge_scenarios=[HealthyBridge()] + pier_disp_scenarios(c),
        response_type=ResponseType.YTranslation)
    pier_displacement_distribution_plots(
        c=c, response_type=ResponseType.YTranslation)


def lane_distribution_plots(
        c: Config, bridge_scenarios: List[BridgeScenario],
        response_type: ResponseType, num: int=25):
    """For each 'BridgeScenario' plot response distributions along each lane.

    All simulations are under the normal traffic scenario.

    Args:
        c: Config, global configuration object.
        bridge_scenarios: List[BridgeScenario], each bridge scenario for which
            to plot the distribution of responses.
        response_type: ResponseType, the type of sensor response to record.
        num: int, the number of points at which to record responses.

    """
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)

    response_arrays = []
    amin, amax = np.inf, -np.inf
    # Collect responses for each bridge scenario and lane combination.
    for bridge_scenario in bridge_scenarios:
        for lane_index, lane in enumerate(c.bridge.lanes):
            # For points along half the lane.
            points = [
                Point(x=x, y=0, z=lane.z_center())
                for x in np.linspace(c.bridge.x_min, c.bridge.x_max / 2, num)]
            response_arrays.append(responses_to_traffic_array(
                c=c, traffic_array=normal_traffic_array,
                response_type=response_type, bridge_scenario=bridge_scenario,
                points=points, fem_runner=OSRunner(c)))
            resized, _ = resize_units(response_arrays[-1], response_type)
            maybe_min = np.amin(resized)
            maybe_max = np.amax(resized)
            if maybe_min < amin:
                amin = maybe_min
            if maybe_max > amax:
                amax = maybe_max

    index = 0
    for bridge_scenario in bridge_scenarios:
        for lane_index, lane in enumerate(c.bridge.lanes):
            plot_distributions(
                response_array=response_arrays[index],
                response_type=response_type,
                titles=[
                    f"x, z = {point.x:.2f}, {point.z:.2f}" for point in points],
                save=c.get_image_path(
                    "distributions",
                    safe_str(
                        f"distributions-{traffic_scenario.name}"
                        + f"-{response_type.name()}"
                        + f"-{bridge_scenario.name}-lane-{lane_index}")),
                xlim=(amin, amax))
            index += 1


def pier_displacement_distribution_plots(
        c: Config, response_type: ResponseType, num: int = 19):
    """Distribution of responses in x direction along each displaced pier.

    All simulations are under the normal traffic scenario.

    Args:
        c: Config, global configuration object.
        response_type: ResponseType, the type of sensor response to record.

    """
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    max_dist = 5

    response_arrays, all_points = [], []
    amin, amax = np.inf, -np.inf
    # Collect responses for each displaced pier...
    for bridge_scenario in pier_disp_scenarios(c):
        pier = c.bridge.supports[bridge_scenario.displacement_ctrl.pier]
        # ...for points along the pier.
        points = [
            Point(x=x, y=0, z=pier.z)
            for x in np.linspace(pier.x - max_dist, pier.x + max_dist, num)]
        all_points.append(points)
        response_arrays.append(responses_to_traffic_array(
            c=c, traffic_array=normal_traffic_array,
            response_type=response_type, bridge_scenario=bridge_scenario,
            points=points, fem_runner=OSRunner(c)))
        resized, _ = resize_units(response_arrays[-1], response_type)
        maybe_min = np.amin(resized)
        maybe_max = np.amax(resized)
        if maybe_min < amin:
            amin = maybe_min
        if maybe_max > amax:
            amax = maybe_max

    index = 0
    for bridge_scenario in pier_disp_scenarios(c):
        points = all_points[index]
        plot_distributions(
            response_array=response_arrays[index],
            response_type=response_type,
            titles=[
                f"x, z = {point.x:.2f}, {point.z:.2f}" for point in points],
            save=c.get_image_path(
                "distributions",
                safe_str(
                    f"pier-distributions-{traffic_scenario.name}"
                    + f"-{response_type.name()}"
                    + f"-{bridge_scenario.name}")))
        index += 1



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
