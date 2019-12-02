"""Time series of responses to moving loads."""
from itertools import chain
from typing import List

import numpy as np
from fem.responses.matrix import load_expt_responses
from scipy.interpolate import interp1d

from classify.scenario.bridge import HealthyBridge, PierDispBridge
from config import Config
from fem.params import ExptParams, SimParams
from fem.responses import Responses
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from model.bridge import Point
from model.load import PointLoad, MvVehicle
from model.response import ResponseType
from model.scenario import BridgeScenario, Traffic, TrafficArray
from util import print_i, print_w

# Comment/uncomment to print debug statements for this file.
D: str = "classify.data.responses"
# D: bool = False


def responses_to_traffic(
    c: Config,
    traffic: "Traffic",
    bridge_scenario: BridgeScenario,
    start_time: float,
    time_step: float,
    points: List[Point],
    response_type: ResponseType,
    fem_runner: FEMRunner,
    min_max: bool = False,
    per_axle: bool = False,
) -> List[Responses]:
    """The 'Responses' to 'Traffic' at each simulation step.

    Args:
        c: Config, global configuration object.
        traffic: Traffic, a list of moving vehicles at each simulation step.
        bridge_scenario: BridgeScenario, the damage scenario of the bridge.
        start_time: float, time at which the traffic simulation starts.
        time_step: List[float], time between each step of the simulation.
        points: List[Point], points on the bridge to calculate responses at.
        response_type, ResponseType, the type of sensor response to calculate.
        fem_runner: FEMRunner, the FEM program to run simulations with.
        min_max: bool, if true also return the minimum and maximum responses.

    """
    for t in range(len(traffic)):
        traffic[t] = list(chain.from_iterable(traffic[t]))

    if per_axle:
        raise ValueError("Per axle option is deprecated")

    # Wheel tracks the vehicle's drive on and an ILMatrix for each wheel track.
    z_fracs = sorted(
        set(
            chain.from_iterable(
                vehicle.wheel_tracks(bridge=c.bridge, meters=False)
                for vehicle in chain.from_iterable(traffic)
            )
        )
    )
    il_matrices = {
        z_frac: ILMatrix.load(
            c=c,
            response_type=response_type,
            fem_runner=fem_runner,
            load_z_frac=z_frac,
        )
        for z_frac in z_fracs
    }

    result = []
    time = start_time - time_step  # The current simulation time.
    min_response, max_response = np.inf, -np.inf

    # Iterate through each step of the simulation.
    for t in range(len(traffic)):
        time += time_step
        print_i(f"Responses at time = {time:.3f}", end="\r")
        result.append([[0, point] for point in points])

        # For each vehicle on the bridge at this time step.
        for mv_vehicle in traffic[t]:

            # assert mv_vehicle.on_bridge(time=time, bridge=c.bridge)
            # We get the x and z positions of this vehicle. There is one x
            # position for each axle, and two z positions per vehicle.
            mv_vehicle_x_fracs = [
                x_frac
                for x_frac in mv_vehicle.x_fracs_at(time=time, bridge=c.bridge)
                if 0 <= x_frac <= 1
            ]
            mv_vehicle_z_fracs = mv_vehicle.wheel_tracks(
                bridge=c.bridge, meters=False
            )

            # Update the response at each point due to this vehicle..
            for p, point in enumerate(points):

                # Calculate a response to each wheel on this vehicle. We start
                # by iterating through each wheel track, and then each wheel on
                # that track.
                mv_vehicle_responses = []
                for mv_vehicle_z_frac in mv_vehicle_z_fracs:
                    il_matrix = il_matrices[mv_vehicle_z_frac]
                    for axle, mv_vehicle_x_frac in enumerate(
                        mv_vehicle_x_fracs
                    ):
                        mv_vehicle_responses.append(
                            il_matrix.response_to(
                                load_x_frac=mv_vehicle_x_frac,
                                load=mv_vehicle.kn_per_axle()[axle] / 2,
                                x_frac=c.bridge.x_frac(x=point.x),
                                y_frac=c.bridge.y_frac(y=point.y),
                                z_frac=c.bridge.z_frac(z=point.z),
                            )
                        )

                result[t][p][0] += sum(mv_vehicle_responses)

        # Update max and min recorded response.
        if min_max:
            for p in range(len(points)):
                min_response = min(min_response, result[t][p][0])
                max_response = max(max_response, result[t][p][0])

        result[t] = Responses.from_responses(
            response_type=response_type, many_response=result[t]
        )

    if min_max:
        return result, min_response, max_response
    else:
        return result


def responses_to_traffic_array(
    c: Config,
    traffic_array: TrafficArray,
    response_type: ResponseType,
    bridge_scenario: BridgeScenario,
    points: List[Point],
    fem_runner: FEMRunner,
    j=None,
):
    """The magic function.

    TODO: Make 'TrafficArray' optional.
    TODO: Find references ot 'j' and remove.

    """
    # The unit load simulations that are loaded depend on whether the bridge is
    # healthy or cracked. TODO

    wheel_zs = c.bridge.wheel_tracks(c)
    ulm_shape = (len(wheel_zs) * c.il_num_loads, len(points))

    if np.count_nonzero(traffic_array) > 0:
        # First collect the unit load simulations per wheel track.
        il_matrices = {
            wheel_z: ILMatrix.load(
                c=c,
                response_type=response_type,
                fem_runner=fem_runner,
                load_z_frac=c.bridge.z_frac(wheel_z),
            )
            for wheel_z in wheel_zs
        }

        # Create a matrix of unit load simulation (rows) * point (columns).
        print_i(f"Calculating unit load matrix...")
        unit_load_matrix = np.empty(ulm_shape)
        for w, wheel_z in enumerate(wheel_zs):
            i = w * c.il_num_loads  # Row index.
            il_matrix = il_matrices[wheel_z]
            # For each unit load simulation.
            for sim_responses in il_matrix.expt_responses:
                for j, point in enumerate(points):
                    unit_load_matrix[i][j] = sim_responses._at(
                        x=point.x, y=point.y, z=point.z
                    )
                i += 1
            print_i(f"Calculated unit load matrix for wheel track {w}")
        # Divide by the load of the unit load simulations, so the value at a
        # cell is the response to 1 kN. Then multiple the traffic and unit load
        # matrices to get the responses.
        unit_load_matrix /= c.il_unit_load_kn
        if j is not None:
            print(f"j = {j}, uls[j][0] = {unit_load_matrix[j][0]}")
    else:
        unit_load_matrix = np.zeros(ulm_shape)

    responses = np.matmul(traffic_array, unit_load_matrix)

    pd_responses = np.zeros(responses.shape)
    if isinstance(bridge_scenario, PierDispBridge):
        pd_responses = pd_responses.T  # Transpose so indexed by point first.
        pd_matrix = DCMatrix.load(
            c=c, response_type=response_type, fem_runner=fem_runner
        )
        assert len(pd_responses) == len(points)
        for p, point in enumerate(points):
            for pier_displacement in bridge_scenario.pier_disps:
                pd_responses[p] += pd_matrix.sim_response(
                    expt_frac=np.interp(
                        pier_displacement.pier,
                        [0, len(c.bridge.supports) - 1],
                        [0, 1],
                    ),
                    x_frac=c.bridge.x_frac(point.x),
                    y_frac=c.bridge.y_frac(point.y),
                    z_frac=c.bridge.z_frac(point.z),
                ) * (pier_displacement.displacement / c.pd_unit_disp)
        pd_responses = pd_responses.T

    return responses + pd_responses


def responses_to_loads(
    c: Config,
    loads: List[PointLoad],
    response_type: ResponseType,
    bridge_scenario: BridgeScenario,
    points: List[Point],
    fem_runner: FEMRunner,
):
    """Responses to point loads."""
    # Create an empty 'TrafficArray' with one time step.
    wheel_track_zs = c.bridge.wheel_tracks(c)
    num_load_positions = c.il_num_loads * len(wheel_track_zs)
    traffic_array = np.zeros((1, num_load_positions))

    # Insert the point loads into the 'TrafficArray'.
    interp = interp1d(
        [0, c.bridge.length], [0, c.il_num_loads - 1], fill_value="extrapolate"
    )
    for load in loads:
        wheel_track_found = False
        load_z = c.bridge.z(load.z_frac)
        for w, wheel_track_z in enumerate(wheel_track_zs):
            if np.isclose(wheel_track_z, load_z):
                wheel_track_found = True
                x_ind = int(interp(c.bridge.x(load.x_frac)))
                j = w * c.il_num_loads + x_ind
                print(f"j = {j}")
                traffic_array[0][j] = load.kn
        if not wheel_track_found:
            print(wheel_track_zs)
            raise ValueError(f"No wheel track for point load at z = {load_z}")

    print([(point.x, point.z, point.y) for point in points])

    return responses_to_traffic_array(
        c=c,
        traffic_array=traffic_array,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        j=j,
        fem_runner=fem_runner,
    )


def responses_to_loads_(
    c: Config,
    loads: List[List[PointLoad]],
    response_type: ResponseType,
    bridge_scenario: BridgeScenario,
    points: List[Point],
    sim_runner: FEMRunner,
):
    """Like 'responses_to_loads' but responses are via direct simulation.

    Returns a numPy array of shape len(loads) * len(points).

    """
    if not isinstance(bridge_scenario, HealthyBridge):
        raise ValueError("Only HealthyBridge supported in direct simulation")
    expt_responses = load_expt_responses(
        c=c,
        expt_params=ExptParams(
            [
                SimParams(response_types=[response_type], ploads=loads_)
                for loads_ in loads
            ]
        ),
        response_type=ResponseType.YTranslation,
        sim_runner=sim_runner,
    )
    result = []
    for sim_responses in expt_responses:
        result.append(
            [
                sim_responses.at(
                    x_frac=c.bridge.x_frac(point.x),
                    z_frac=c.bridge.z_frac(point.z),
                )
                for point in points
            ]
        )
    return np.array(result)


def responses_to_vehicles_(
    c: Config,
    mv_vehicles: List[MvVehicle],
    times: List[float],
    response_type: ResponseType,
    bridge_scenario: BridgeScenario,
    points: List[Point],
    sim_runner: FEMRunner,
):
    """Responses to vehicles via direct simulation."""
    print_w("TODO: converting vehicle to point loads")
    loads = [
        list(
            chain.from_iterable(
                chain.from_iterable(
                    v.to_point_loads(time=time, bridge=c.bridge)
                )
                for v in mv_vehicles
            )
        )
        for time in times
    ]
    assert isinstance(loads, list)
    assert isinstance(loads[0], list)
    assert isinstance(loads[0][0], PointLoad)
    return responses_to_loads_(
        c=c,
        loads=loads,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        sim_runner=sim_runner,
    )
