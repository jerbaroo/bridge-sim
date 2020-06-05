"""High-level API for saving/loading responses from FE simulation."""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
from bridge_sim.model import (
    Config,
    ResponseType,
    Point,
    PointLoad,
    Vehicle,
    PierSettlement,
)
from bridge_sim.sim.model import SimParams, Responses
from bridge_sim.sim.run import load_expt_responses, load_fem_responses, load_ulm
from bridge_sim.util import flatten, print_i, print_w

D: str = "sim.responses"
# D: bool = False


def load(
    config: Config,
    response_type: ResponseType,
    point_loads: List[PointLoad] = [],
    pier_settlement: List[PierSettlement] = [],
    temp_deltas: Tuple[Optional[float], Optional[float]] = (None, None),
) -> Responses:
    """Responses from a single linear simulation.

    The simulation is only run if results are not found on disk. Note that for
    temperature loading no post-processing is done.

    Args:
        config: simulation configuration object.
        response_type: sensor response type to return.
        point_loads: a list of point-loads to apply.
        pier_settlement: a pier settlement to apply.
        temp_deltas: uniform and linear temperature components.

    """
    return load_fem_responses(
        c=config,
        sim_params=SimParams(
            ploads=point_loads,
            pier_settlement=pier_settlement,
            axial_delta_temp=temp_deltas[0],
            moment_delta_temp=temp_deltas[1],
        ),
        response_type=response_type,
    )


def responses_to_traffic_array(
    c: Config,
    traffic_array: "TrafficArray",
    response_type: ResponseType,
    points: List[Point],
):
    """Responses to a traffic array at some points.

    Args:
        c: Config, simulations configuration object.
        traffic_array: traffic array to calculate responses to.
        response_type: the type of sensor response.
        points: points at which to calculate responses.

    Returns: NumPY array indexed first by point the time.

    """
    ulm = load_ulm(c, response_type, points)
    assert ulm.shape[0] == len(points)
    print(traffic_array.shape, ulm.shape)
    return np.matmul(traffic_array, ulm)


def responses_to_loads_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
):
    """Responses to point-loads via direct simulation."""
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
):
    """Response vehicles via direct simulation."""
    if binned:
        loads = [
            [v.to_wheel_track_loads(c=c, time=time) for v in mv_vehicles]
            for time in times
        ]
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
    )

