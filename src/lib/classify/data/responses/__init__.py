"""Time series of responses to moving loads."""
from __future__ import annotations

from itertools import chain
from typing import Callable, List

import numpy as np

from lib.classify.scenario.bridge import HealthyDamage, PierDispDamage
from lib.fem.params import ExptParams, SimParams
from lib.fem.responses import Responses
from lib.fem.responses.matrix import load_expt_responses
from lib.fem.responses.matrix.dc import DCMatrix
from lib.fem.responses.matrix.il import ILMatrix
from lib.fem.run import FEMRunner
from lib.fem.run.opensees import OSRunner
from bridge_sim.model import Point, Config
from bridge_sim.model.vehicle import PointLoad, MvVehicle
from lib.model.response import ResponseType
from util import flatten, print_i, print_w

# Comment/uncomment to print debug statements for this file.
D: str = "classify.data.responses"
D: bool = False

############################
##### Via wheel tracks #####
############################


def responses_to_traffic_array(
    c: Config,
    traffic_array: "TrafficArray",
    response_type: ResponseType,
    damage_scenario: "DamageScenario",
    points: List[Point],
    sim_runner: Callable[[Config], FEMRunner] = OSRunner,
):
    """The magic function.

    Args:
        c: Config, global configuration object.
        traffic_array: TrafficArray, ....
        damage_scenario: DamageScenario, the scenarios scenario of the bridge.
        response_type, ResponseType, the type of sensor response to calculate.
        points: List[Point], points on the bridge to calculate responses at.
        sim_runner: Callable[[Config], FEMRunner], the FEM program to run
            simulations with.

    """
    use_c = damage_scenario.use(c)[0]
    unit_load_matrix = ILMatrix.load_ulm(
        c=use_c,
        response_type=response_type,
        points=points,
        sim_runner=sim_runner(use_c),
    )
    print(traffic_array.shape)
    print(unit_load_matrix.shape)
    responses = np.matmul(traffic_array, unit_load_matrix)

    # Calculate the response at each point due to pier settlement.
    pd_responses = np.zeros(responses.shape).T
    assert len(pd_responses) == len(points)
    if isinstance(damage_scenario, PierDispDamage):
        pd_expt = list(
            DCMatrix.load(c=c, response_type=response_type, fem_runner=sim_runner(c))
        )
        for point_i, point in enumerate(points):
            for pier_displacement in damage_scenario.pier_disps:
                pd_sim_responses = pd_expt[pier_displacement.pier]
                pd_responses[point_i] += pd_sim_responses.at_deck(
                    point, interp=False
                ) * (pier_displacement.displacement / c.pd_unit_disp)

    return responses + pd_responses.T


def responses_to_traffic(
    c: Config,
    traffic: "Traffic",
    bridge_scenario: "DamageScenario",
    start_time: float,
    time_step: float,
    points: List[Point],
    response_type: ResponseType,
    sim_runner: FEMRunner,
    min_max: bool = False,
) -> List[Responses]:
    """The 'Responses' to 'Traffic' at each simulation step.

    """
    print_w(
        "Deprecated 'responses_to_traffic': no need to be using this function",
        flush=True,
    )
    import sys

    sys.exit()
    for t in range(len(traffic)):
        traffic[t] = list(chain.from_iterable(traffic[t]))

    # Wheel tracks the vehicles's drive on and an ILMatrix for each wheel track.
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
            c=c, response_type=response_type, sim_runner=sim_runner, load_z_frac=z_frac,
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

        # For each vehicles on the bridge at this time step.
        for mv_vehicle in traffic[t]:

            # assert mv_vehicle.on_bridge(time=time, bridge=c.bridge)
            # We get the x and z positions of this vehicles. There is one x
            # position for each axle, and two z positions per vehicles.
            mv_vehicle_x_fracs = [
                x_frac
                for x_frac in mv_vehicle.x_fracs_at(time=time, bridge=c.bridge)
                if 0 <= x_frac <= 1
            ]
            mv_vehicle_z_fracs = mv_vehicle.wheel_tracks(bridge=c.bridge, meters=False)

            # Update the response at each point due to this vehicles..
            for p, point in enumerate(points):

                # Calculate a response to each wheel on this vehicles. We start
                # by iterating through each wheel track, and then each wheel on
                # that track.
                mv_vehicle_responses = []
                for mv_vehicle_z_frac in mv_vehicle_z_fracs:
                    il_matrix = il_matrices[mv_vehicle_z_frac]
                    for axle, mv_vehicle_x_frac in enumerate(mv_vehicle_x_fracs):
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


#################################
##### Via direct simulation #####
#################################


def responses_to_loads_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
    sim_runner: FEMRunner,
    damage_scenario: DamageScenario = HealthyDamage(),
):
    """Responses to loads via direct simulation.

    NOTE: this function will place a point load directly. This function doesn't
    take into account wheel track bins.

    """
    if not isinstance(damage_scenario, HealthyDamage):
        raise ValueError("Only HealthyDamage supported in direct simulation")
    expt_responses = load_expt_responses(
        c=c,
        expt_params=ExptParams(
            [
                SimParams(response_types=ResponseType.all(), ploads=loads_)
                for loads_ in loads
            ]
        ),
        response_type=response_type,
        sim_runner=sim_runner,
    )
    result = []
    for sim_responses in expt_responses:
        result.append([sim_responses.at_deck(point, interp=True) for point in points])
        print_i("Interpolating responses in responses_from_load_d")
    return np.array(result)


def responses_to_vehicles_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    mv_vehicles: List[MvVehicle],
    times: List[float],
    sim_runner: FEMRunner,
    binned: bool = True,
    damage_scenario: DamageScenario = HealthyDamage(),
):
    """Response at points to vehicles via direct simulation.

    NOTE: this function will place a point load directly at the center of each
    wheel. This function doesn't take into account wheel track buckets.

    """
    if not isinstance(damage_scenario, HealthyDamage):
        raise ValueError("Only HealthyDamage supported in direct simulation")
    if binned:
        print("binned")
        loads = [
            [v.to_wheel_track_loads(c=c, time=time) for v in mv_vehicles]
            for time in times
        ]
        print(loads[4])
    else:
        print_w(f"Not using fractions of wheel track bins in simulation")
        loads = [
            [v.to_point_load_pw(time=time, bridge=c.bridge) for v in mv_vehicles]
            for time in times
        ]
    loads = [flatten(vehicle_loads, PointLoad) for vehicle_loads in loads]
    print([len(load_) for load_ in loads])
    print(loads[0])
    print(loads[-1])
    assert isinstance(loads, list)
    assert isinstance(loads[0], list)
    assert isinstance(loads[0][0], PointLoad)
    return responses_to_loads_d(
        c=c,
        response_type=response_type,
        points=points,
        loads=loads,
        sim_runner=sim_runner,
        damage_scenario=damage_scenario,
    )
