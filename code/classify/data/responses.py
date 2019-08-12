"""Time series of responses to moving loads."""
from itertools import takewhile
from typing import List, NewType, Optional

import numpy as np

from config import Config
from fem.responses.matrix import load_il_matrix
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import Bridge, MovingLoad, Point, Response, ResponseType
from model.bridge_705 import bridge_705_config
from util import *


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

    load_x_frac = mv_load.x_frac_at(time, c.bridge)
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
    """The response to one or more moving loads at a single time.

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
    if per_axle:
        return responses
    else:
        return np.sum(responses)



def responses_to_mv_loads(
        c: Config, mv_loads: List[MovingLoad], response_type: ResponseType,
        fem_runner: FEMRunner, at: List[Point], per_axle: bool=False,
        times: Optional[List[float]]=None):
    """The responses to a load for a number of time steps.

    Returns a numpy array of shape (len(times), len(at)) or if per_axle is
    True then a numpy array of shape(len(times), len(at), number of axles).

    Args:
        times: Optional[List[float]], times to record responses at. If None
            then select all times when the MovingLoad is on the bridge.
        per_axle: bool, if true then return a response per axle, otherwise
            return a single response for the vehicle.

    """
    assert isinstance(c, Config)
    assert isinstance(mv_loads[0], MovingLoad)
    assert isinstance(response_type, ResponseType)
    assert isinstance(fem_runner, FEMRunner)
    assert isinstance(at, list)
    assert isinstance(at[0], Point)
    if times is None:
        print_w(f"times is None")
        times = list(times_on_bridge(c=c, mv_loads=mv_loads))
        print_w(f"max_time = {times[-1]}")
    # TODO: Make this a generator.
    result = np.array([
        [response_to_mv_loads(
            c=c, mv_loads=mv_loads, time=time, at=at_,
            response_type=response_type, fem_runner=fem_runner,
            per_axle=per_axle)
         for at_ in at]
        for time in times])
    assert len(result.shape) == 3 if per_axle else 2
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    return result


def on_bridge(bridge: Bridge, mv_load: MovingLoad, time: float):
    """Whether a moving load is on a bridge at a given time."""
    # Find leftmost and rightmost points of the load.
    left_x_frac = mv_load.x_frac_at(time, bridge)
    print_w(f"x_frac = {mv_load.x_frac_at(0, bridge)} @ {time}")
    print_w(f"left_x_frac = {left_x_frac}")
    right_x_frac = left_x_frac
    if not mv_load.load.is_point_load():
        vehicle_length = sum(mv_load.load.axle_distances)
        right_x_frac += bridge.x_frac(vehicle_length)
    print_w(f"right_x_frac = {right_x_frac}")
    return (
        0 <= left_x_frac and left_x_frac <= 1 and
        0 <= right_x_frac and right_x_frac <= 1)


def times_on_bridge(c: Config, mv_loads: List[MovingLoad]) -> List[float]:
    """Yield the times when a moving load is on a bridge."""
    time = 0
    while any(
            on_bridge(bridge=c.bridge, mv_load=mv_load, time=time)
            for mv_load in mv_loads):
        yield time
        time += c.time_step
