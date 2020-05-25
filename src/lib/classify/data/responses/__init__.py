"""Time series of fem to moving loads."""

from __future__ import annotations

from typing import Callable, List

import numpy as np

from bridge_sim.model import Point, Config, PointLoad, Vehicle, ResponseType
from bridge_sim.scenarios import DamageScenario
from lib.classify.scenario.bridge import HealthyDamage, PierDispDamage
from lib.fem.params import SimParams
from lib.fem.responses.many import load_expt_responses
from lib.fem.responses.many.ps import PSResponses
from lib.fem.responses.many.ul import ULResponses
from lib.fem.run import FEMRunner
from lib.fem.run.opensees import OSRunner
from bridge_sim.util import flatten, print_i, print_w

# Comment/uncomment to print debug statements for this file.
# D: str = "classify.data.fem"
D: bool = False


####################
# Via wheel tracks #
####################


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
        response_type: ResponseType, the type of sensor response to calculate.
        points: List[Point], points on the bridge to calculate fem at.
        sim_runner: Callable[[Config], FEMRunner], the FEM program to run
            simulations with.

    """
    use_c = damage_scenario.use(c)[0]
    unit_load_matrix = ULResponses.load_ulm(
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
            PSResponses.load(c=c, response_type=response_type, fem_runner=sim_runner(c))
        )
        for point_i, point in enumerate(points):
            for pier_displacement in damage_scenario.pier_disps:
                pd_sim_responses = pd_expt[pier_displacement.pier]
                pd_responses[point_i] += pd_sim_responses.at_deck(
                    point, interp=False
                ) * (pier_displacement.displacement / c.pd_unit_disp)

    return responses + pd_responses.T


#########################
# Via direct simulation #
#########################


def responses_to_loads_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
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
        expt_params=[SimParams(ploads=loads_) for loads_ in loads],
        response_type=response_type,
    )
    result = []
    for sim_responses in expt_responses:
        result.append([sim_responses.at_deck(point, interp=True) for point in points])
        print_i("Interpolating fem in responses_from_load_d")
    return np.array(result)


def responses_to_vehicles_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    mv_vehicles: List[Vehicle],
    times: List[float],
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
        damage_scenario=damage_scenario,
    )
