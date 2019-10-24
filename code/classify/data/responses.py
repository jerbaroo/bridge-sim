"""Time series of responses to moving loads."""
from itertools import chain
from typing import List, Optional, Tuple

import numpy as np

from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from model import Response
from model.bridge import Bridge, Point
from model.load import MvVehicle
from model.response import ResponseType
from model.scenario import BridgeScenario
from util import print_d

# Comment/uncomment to print debug statements for this file.
D: str = "classify.data.responses"
# D: bool = False


def responses_to_traffic(
        c: Config, traffic: "Traffic", bridge_scenario: BridgeScenario,
        start_index: float, time_step: float, points: List[Point],
        response_type: ResponseType, fem_runner: FEMRunner,
        per_axle: bool = False) -> List[Tuple[float, Point]]:
    """The responses to traffic over a number of simulation steps.

    Returns a list of Respoon per simulation time step.

    Args:
        c: Config, global configuration object.
        traffic: Traffic, a list of moving vehicles at each simulation step.
        bridge_scenario: BridgeScenario, the damage scenario of the bridge.
        start_time: float, time at which the traffic simulation starts.
        time_step: List[float], time between each step of the simulation.
        points: List[Point], points on the bridge to calculate responses at.
        response_type, ResponseType, the type of sensor response to calculate.
        fem_runner: FEMRunner, the FEM program to run simulations with.

    """
    if per_axle:
        raise ValueError("Per axle option is deprecated")

    result = []
    time = (start_index * time_step) - time_step  # The simulation time.
    z_fracs = sorted(set(chain.from_iterable(
        vehicle.wheel_tracks(bridge=c.bridge, meters=False)
        for vehicle in chain.from_iterable(traffic))))
    print(z_fracs)
    il_matrices = {  # An ILMatrix for each wheel track.
        z_frac: ILMatrix.load(
            c=c, response_type=response_type, fem_runner=fem_runner,
            load_z_frac=z_frac)
        for z_frac in z_fracs}

    # Iterate through each step of the simulation.
    for t in range(len(traffic)):
        result.append([0 for _ in range(len(points))])
        time += time_step

        # For each vehicle on the bridge at this time step.
        for mv_vehicle in traffic[t]:
            mv_vehicle_x_frac = mv_vehicle.x_frac_at(time=time, bridge=c.bridge)
            mv_vehicle_z_fracs = mv_vehicle.wheel_tracks(
                bridge=c.bridge, meters=False)
            lane_center = c.bridge.lanes[mv_vehicle.lane].z_center()
            print_d(D, f"lane center = {lane_center}")
            print_d(D, f"lane center as frac = {c.bridge.z_frac(lane_center)}")
            print_d(D, f"z_fracs = {mv_vehicle_z_fracs}")

            # Update the response at each point due to this vehicle..
            for p, point in enumerate(points):

                # ..calculating a response due to each axle and wheel.
                axle_responses = []
                for axle_index in range(mv_vehicle.num_axles):
                    # Update x position of the response for each axle.
                    if axle_index != 0:
                        axle_distance = mv_vehicle.axle_distances[
                            axle_index - 1] / 100
                        mv_vehicle_x_frac += c.bridge.x_frac(axle_distance)
                    # Get a response for each wheel on this axle.
                    responses_for_one_axle = []
                    for mv_vehicle_z_frac in mv_vehicle_z_fracs:
                        il_matrix = il_matrices[mv_vehicle_z_frac]
                        responses_for_one_axle.append(il_matrix.response_to(
                            x_frac=c.bridge.x_frac(x=point.x),
                            load_x_frac=mv_vehicle_x_frac,
                            load=mv_vehicle.kn))
                    axle_responses.append(sum(responses_for_one_axle))

                result[t][p] += sum(axle_responses)

        results[-1] = list(map(
            lambda value, i: (value, points[i]), enumerate(results[-1])))

    return results
