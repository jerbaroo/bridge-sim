"""Time series of responses to moving loads."""
from typing import List, Optional

import numpy as np

from config import Config
from fem.responses.matrix.il import load_il_matrix
from fem.run import FEMRunner
from model import Response
from model.bridge import Bridge, Point
from model.load import MovingLoad
from model.response import ResponseType


def response_to_mv_load(
        c: Config, mv_load: MovingLoad, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner,
        per_axle: bool=False) -> Response:
    """The response to one or more moving loads at a single time.

    Args:
        per_axle: bool, if true then return a list of response per axle,
            otherwise return a single response for the vehicle.

    """
    assert on_bridge(bridge=c.bridge, mv_load=mv_load, time=time)

    load_x_frac = mv_load.x_frac_at(time=time, bridge=c.bridge)
    il_matrix = load_il_matrix(c, response_type, fem_runner)

    # Point load.
    if mv_load.load.is_point_load():
        return il_matrix.response_to(
            c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn)

    # Vehicle load.
    else:
        axle_responses = []
        for i in range(mv_load.load.num_axles):
            # Update load position for each axle.
            if i != 0:
                axle_distance = mv_load.load.axle_distances[i - 1] / 100
                load_x_frac += c.bridge.x_frac(axle_distance)
            axle_responses.append(il_matrix.response_to(
                c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn))

    return axle_responses if per_axle else sum(axle_responses)


def response_to_mv_loads(
        c: Config, mv_loads: List[MovingLoad], time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner,
        per_axle: bool=False) -> Response:
    """The response to one or more moving loads at one simulation time.

    Args:
        per_axle: bool, if true then return a list of response per axle,
            otherwise return a single response for the vehicle.

    """
    responses = [
        response_to_mv_load(
            c=c, mv_load=mv_load, time=time, at=at,
            response_type=response_type, fem_runner=fem_runner,
            per_axle=per_axle)
        for mv_load in mv_loads
        if on_bridge(bridge=c.bridge, mv_load=mv_load, time=time)]
    return responses if per_axle else np.sum(responses)


def responses_to_mv_loads(
        c: Config, mv_loads: List[MovingLoad],
        response_types: List[ResponseType],
        fem_runner: FEMRunner, at: List[Point], per_axle: bool = False,
        times: Optional[List[float]] = None):
    """The responses to a load for a number of time steps.

    Returns either a 4 or 5 dimensional numpy array, of shape (len(times),
    len(at), len(response_types), len(mv_loads)) if per_axle is False, else of
    shape (len(times), len(at), len(response_types), len(mv_loads), #axles).

    Args:
        per_axle: bool, if true then return a response per axle, otherwise
            return a single response for the vehicle.
        times: Optional[List[float]], times to record responses at. If None
            (default) then select all times when a MovingLoad is on the bridge.

    """
    assert isinstance(c, Config)
    assert isinstance(mv_loads[0], MovingLoad)
    assert isinstance(response_types[0], ResponseType)
    assert isinstance(fem_runner, FEMRunner)
    assert isinstance(at, list)
    assert isinstance(at[0], Point)

    if times is None:
        times = list(times_on_bridge(c=c, mv_loads=mv_loads))

    result = np.array([
        [[response_to_mv_loads(
            c=c, mv_loads=mv_loads, time=time, at=at_,
            response_type=response_type, fem_runner=fem_runner,
            per_axle=per_axle)
          for response_type in response_types]
         for at_ in at]
        for time in times])

    assert len(result.shape) == 5 if per_axle else 4
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    assert result.shape[2] == len(response_types)
    return result


def on_bridge(bridge: Bridge, mv_load: MovingLoad, time: float):
    """Whether a moving load is on a bridge at a given time."""
    # Find leftmost and rightmost points of the load.
    left_x_frac = mv_load.x_frac_at(time, bridge)
    right_x_frac = left_x_frac
    if not mv_load.load.is_point_load():
        vehicle_length = sum(mv_load.load.axle_distances)
        right_x_frac += bridge.x_frac(vehicle_length)
    return 0 <= left_x_frac <= 1 and 0 <= right_x_frac <= 1


def times_on_bridge(c: Config, mv_loads: List[MovingLoad]) -> List[float]:
    """Yield the times when a moving load is on a bridge."""
    time = 0
    while any(
            on_bridge(bridge=c.bridge, mv_load=mv_load, time=time)
            for mv_load in mv_loads):
        yield time
        time += c.time_step
