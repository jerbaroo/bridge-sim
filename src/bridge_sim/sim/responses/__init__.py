"""High-level API for saving/loading responses from FE simulation."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from bridge_sim import temperature, util

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
from bridge_sim.traffic import TrafficArray
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


def to_traffic_array(
    c: Config,
    traffic_array: TrafficArray,
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
    assert ulm.shape[1] == len(points)
    assert traffic_array.shape[1] == ulm.shape[0]
    print(traffic_array.shape, ulm.shape)
    return np.matmul(traffic_array, ulm).T


def to_loads_direct(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
):
    """Responses to point-loads over time (via direct simulation)."""
    expt_responses = load_expt_responses(
        c=c,
        expt_params=[SimParams(ploads=loads_) for loads_ in loads],
        response_type=response_type,
    )
    return np.array(
        [sim_responses.at_decks(points) for sim_responses in expt_responses]
    )


def to_vehicles_direct(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    vehicles: List[Vehicle],
    times: List[float],
):
    """Responses to vehicles over time (via direct simulation)."""
    loads = [v.wheel_track_loads(config=c, times=times) for v in vehicles]
    loads_per_time = [[] for _ in times]
    for v_loads in loads:
        for t, t_loads in enumerate(v_loads):
            loads_per_time[t] += t_loads
    loads_per_time = [flatten(v_loads, PointLoad) for v_loads in loads_per_time]
    print([len(load_) for load_ in loads_per_time])
    print(loads_per_time[0])
    print(loads_per_time[-1])
    assert isinstance(loads_per_time, list)
    assert isinstance(loads_per_time[0], list)
    assert isinstance(loads_per_time[0][0], PointLoad)
    return to_loads_direct(
        c=c, response_type=response_type, points=points, loads=loads_per_time,
    )


def to_pier_settlement(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    pier_settlement: List[Tuple[PierSettlement, PierSettlement]],
) -> List[List[float]]:
    """Time series of responses to pier settlement.

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        responses_array: NumPY array indexed first by point the time.
        response_type: the sensor response type to add.
        pier_settlement: start and end settlements of piers.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from pier settlement.

    """
    assert len(responses_array) == len(points)
    start_responses = load(
        config=config,
        response_type=response_type,
        pier_settlement=list(map(lambda ps: ps[0], pier_settlement)),
    ).at_decks(points)
    assert len(start_responses.shape) == 1
    assert len(start_responses) == len(points)
    end_responses = load(
        config=config,
        response_type=response_type,
        pier_settlement=list(map(lambda ps: ps[1], pier_settlement)),
    ).at_decks(points)
    ps_responses = np.zeros(responses_array.shape)
    for p, _ in enumerate(points):
        ps_responses[p] = np.interp(
            np.arange(ps_responses.shape[1]),
            [0, ps_responses.shape[1] - 1],
            [start_responses[p], end_responses[p]]
        )
    return ps_responses


def to_temperature(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    weather: Optional[pd.DataFrame] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[List[float]]:
    """Time series of responses to temperature.

    Date formats must be given as "%d/%m/%y %H:%M" e.g. "01/05/19 00:00".

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        responses_array: NumPY array indexed first by point the time.
        response_type: the sensor response type to add.
        weather: the FULL weather data to calculate responses.
        start_date: start-date of weather data.
        end_date: end-date of weather data.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from temperature.

    """
    temp_responses = np.zeros(responses_array.shape)
    if weather is None:
        return temp_responses
    weather = temperature.from_to_mins(
        weather,
        from_=datetime.strptime(start_date, "%d/%m/%y %H:%M"),
        to=datetime.strptime(end_date, "%d/%m/%y %H:%M"),
    )
    effect = temperature.effect(
        config=config,
        response_type=response_type,
        points=points,
        weather=weather,
    )
    assert len(responses_array) == len(points)
    assert len(effect) == len(points)
    for p, _ in enumerate(points):
        temp_responses[p] = util.apply(effect[p], temp_responses[p])
    return temp_responses
