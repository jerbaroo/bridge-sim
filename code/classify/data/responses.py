"""Time series of responses to moving loads."""
from typing import List, Optional

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


def response_to_mv_vehicle(
        c: Config, mv_vehicle: MvVehicle, bridge_scenario: BridgeScenario,
        time: float, at: Point, response_type: ResponseType,
        fem_runner: FEMRunner, per_axle: bool = False) -> Response:
    """The response to one moving vehicle at one simulation time.

    Args:
        c: Config, global configuration object.
        mv_vehicle: MvVehicle, the moving vehicle to calculate a response to.
        bridge_scenario: BridgeScenario, the damage scenario of the bridge.
        time: float, in combination with vehicle speed this determines the
            position of the moving vehicle, in seconds.
        at: Point, the point at which to calculate a response to the vehicle.
        response_type, ResponseType, the sensor type of response to calculate.
        fem_runner: FEMRunner, the FEM program to run simulations with.
        per_axle: bool, if true then return a list of response per axle,
            otherwise return a single response for the vehicle.

    """
    assert on_bridge(bridge=c.bridge, mv_vehicle=mv_vehicle, time=time)

    mv_vehicle_x_frac = mv_vehicle.x_frac_at(time=time, bridge=c.bridge)
    mv_vehicle_z_fracs = mv_vehicle.wheel_tracks(bridge=c.bridge, meters=False)

    lane_center = c.bridge.lanes[mv_vehicle.lane].z_center()
    print_d(D, f"lane center = {lane_center}")
    print_d(D, f"lane center as frac = {c.bridge.z_frac(lane_center)}")
    print_d(D, f"z_fracs = {mv_vehicle_z_fracs}")

    # An ILMatrix for each wheel track.
    il_matrices = [
        ILMatrix.load(
            c=c, response_type=response_type, fem_runner=fem_runner,
            load_z_frac=mv_vehicle_z_frac)
        for mv_vehicle_z_frac in mv_vehicle_z_fracs]

    axle_responses = []
    for axle_index in range(mv_vehicle.num_axles):
        # Update x position of the response for each axle.
        if axle_index != 0:
            axle_distance = mv_vehicle.axle_distances[axle_index - 1] / 100
            mv_vehicle_x_frac += c.bridge.x_frac(axle_distance)
        # Get a response for each wheel on this axle.
        responses_for_one_axle = []
        for z_index, mv_vehicle_z_frac in enumerate(mv_vehicle_z_fracs):
            il_matrix = il_matrices[z_index]
            responses_for_one_axle.append(il_matrix.response_to(
                x_frac=c.bridge.x_frac(x=at.x), load_x_frac=mv_vehicle_x_frac,
                load=mv_vehicle.kn))
        axle_responses.append(sum(responses_for_one_axle))

    return axle_responses if per_axle else sum(axle_responses)


def response_to_mv_vehicles(
        c: Config, mv_vehicles: List[MvVehicle],
        bridge_scenario: BridgeScenario, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner, per_axle: bool = False
        ) -> Response:
    """The response to one or more moving vehicles at one simulation time.

    Args:
        per_axle: bool, if true then return a list of response per axle,
            otherwise return a single response for the vehicle.

    """
    lane = mv_vehicles[0].lane
    for mv_vehicle in mv_vehicles:
        if mv_vehicle.lane != lane:
            raise ValueError("Only single lane is supported per simulation")

    responses = [
        response_to_mv_vehicle(
            c=c, mv_vehicle=mv_vehicle, bridge_scenario=bridge_scenario,
            time=time, at=at, response_type=response_type,
            fem_runner=fem_runner, per_axle=per_axle)
        for mv_vehicle in mv_vehicles
        if on_bridge(bridge=c.bridge, mv_vehicle=mv_vehicle, time=time)]

    return responses if per_axle else np.sum(responses)


def responses_to_mv_vehicles(
        c: Config, mv_vehicles: List[MvVehicle],
        bridge_scenario: BridgeScenario, response_types: List[ResponseType],
        fem_runner: FEMRunner, at: List[Point], per_axle: bool = False,
        times: Optional[List[float]] = None):
    """The responses to one or more moving vehicles for a number of time steps.

    Returns either a 4 or 5 dimensional numpy array, of shape:
        (len(times), len(at), len(response_types), len(mv_loads))
    if per_axle is False, else of shape:
        (len(times), len(at), len(response_types), len(mv_loads), #axles).

    Args:
        per_axle: bool, if true then return a response per axle, otherwise
            return a single response for the vehicle.
        times: Optional[List[float]], times to record responses at. If None
            (default) then select all times when a MovingLoad is on the bridge.

    """
    assert isinstance(c, Config)
    assert isinstance(mv_vehicles[0], MvVehicle)
    assert isinstance(response_types[0], ResponseType)
    assert isinstance(fem_runner, FEMRunner)
    assert isinstance(at, list)
    assert isinstance(at[0], Point)

    if times is None:
        times = list(times_on_bridge(c=c, mv_vehicles=mv_vehicles))

    result = np.array([
        [[response_to_mv_vehicles(
            c=c, mv_vehicles=mv_vehicles, bridge_scenario=bridge_scenario,
            time=time, at=at_, response_type=response_type,
            fem_runner=fem_runner, per_axle=per_axle)
          for response_type in response_types]
         for at_ in at]
        for time in times])

    assert len(result.shape) == 5 if per_axle else 4
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    assert result.shape[2] == len(response_types)
    return result


def on_bridge(bridge: Bridge, mv_vehicle: MvVehicle, time: float):
    """Whether a moving load is on a bridge at a given time."""
    # Find leftmost and rightmost points of the load.
    left_x_frac = mv_vehicle.x_frac_at(time, bridge)
    right_x_frac = left_x_frac + bridge.x_frac(mv_vehicle.length)
    return 0 <= left_x_frac <= 1 and 0 <= right_x_frac <= 1


def times_on_bridge(c: Config, mv_vehicles: List[MvVehicle]) -> List[float]:
    """Yield the times when a moving load is on a bridge."""
    time = 0
    while any(
            on_bridge(bridge=c.bridge, mv_vehicle=mv_vehicle, time=time)
            for mv_vehicle in mv_vehicles):
        yield time
        time += c.time_step
