"""High-level API for saving/loading responses from FE simulation."""

from __future__ import annotations

# Print debug information for this file.
from typing import List, Optional, Tuple

import numpy as np
from bridge_sim.model import (
    Config,
    ResponseType,
    Point,
    PointLoad,
    Vehicle,
    Config as LibConfig,
    PierSettlement,
)
from bridge_sim.sim.model import SimParams, Responses
from bridge_sim.sim.run import load_expt_responses, load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from bridge_sim.util import (
    print_i,
    print_w,
    flatten,
)

D: str = "fem.fem"
# D: bool = False


def responses_to_traffic_array(
    c: Config,
    traffic_array: "TrafficArray",
    response_type: ResponseType,
    points: List[Point],
):
    """The magic function.

    Args:
        c: Config, global configuration object.
        traffic_array: TrafficArray, ....
        response_type: ResponseType, the type of sensor response to calculate.
        points: List[Point], points on the bridge to calculate fem at.

    """
    unit_load_matrix = ULResponses.load_ulm(
        c=c, response_type=response_type, points=points,
    )
    print(traffic_array.shape)
    print(unit_load_matrix.shape)
    return np.matmul(traffic_array, unit_load_matrix)


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


def load(
    config: LibConfig,
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


def run_ulm(c: Config, healthy: bool, cracked: bool, x_i: float, z_i: float):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    wheel_xs = c.bridge.wheel_track_xs(c)
    wheel_x = wheel_xs[x_i]
    wheel_zs = c.bridge.wheel_track_zs(c)
    wheel_z = wheel_zs[z_i]
    print_i(f"Wheel (x, z) = ({wheel_x}, {wheel_z})")
    point = Point(x=wheel_x, y=0, z=wheel_z)
    if healthy:
        ULResponses.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
    if cracked:
        c = transverse_crack().use(c)[0]
        ULResponses.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
