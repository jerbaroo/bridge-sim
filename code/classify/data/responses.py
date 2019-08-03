"""Time series of responses to moving loads."""
from itertools import takewhile
from typing import List, NewType

import numpy as np

from config import Config
from fem.responses.matrix import load_il_matrix
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import MovingLoad, Point, Response, ResponseType
from model.bridge_705 import bridge_705_config
from util import *


def response_at_time(
        c: Config, mv_load: MovingLoad, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner,
        per_axle: bool=False) -> Response:
    """The response to a moving load at a given time.

    Args:
        per_axle: bool, if true then return a list of response per axle,
            otherwise return a single response for the vehicle.
    """
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


def responses_to_mv_load(
        c: Config, mv_load: MovingLoad, response_type: ResponseType,
        fem_runner: FEMRunner, times: List[float], at: List[Point],
        per_axle: bool=False):
    """The responses to a load for a number of time steps.

    Returns a numpy array of shape (len(times), len(at)) or if per_axle if
    True then a numpy array of shape(len(times), len(at), number of axles).

    Args:
        per_axle: bool, if true then return a response per axle, otherwise
            return a single response for the vehicle.

    """
    result = np.array([
        [response_at_time(
            c, mv_load, time, at_, response_type, fem_runner,
            per_axle=per_axle)
         for at_ in at]
        for time in times])
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    return result


def times_on_bridge(
        c: Config, mv_load: MovingLoad, times: List[float]) -> List[float]:
    """Return only the times the moving load is on the bridge."""

    def on_bridge_at(time):
        min_x_frac = mv_load.x_frac_at(time, c.bridge)
        max_x_frac = min_x_frac
        if not mv_load.load.is_point_load():
            vehicle_length = sum(mv_load.load.axle_distances)
            max_x_frac += c.bridge.x_frac(vehicle_length)
        return (
            0 <= min_x_frac and min_x_frac <= 1 and
            0 <= max_x_frac and max_x_frac <= 1)

    return list(takewhile(on_bridge_at, times))


def times_on_bridge_(
        c: Config, mv_load: MovingLoad, time_step: float=0.05,
        time_end: float=20) -> List[float]:
    """Return only the times the moving load is on the bridge."""
    num_times = int((time_end / time_step) + 1)
    return times_on_bridge(c, mv_load, np.linspace(0, time_end, num_times))
