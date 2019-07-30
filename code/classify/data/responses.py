"""Time series of responses to moving loads."""
from itertools import takewhile
from typing import List

import numpy as np

from config import Config
from fem.responses.matrix import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import MovingLoad, Point, Response, ResponseType
from model.bridge_705 import bridge_705_config
from util import *

print_w("TODO: classify.data.responses.response_at_time: implement for vehicle load")


def response_at_time(
        c: Config, mv_load: MovingLoad, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner
    ) -> Response:
    """The response to a moving load at a given time."""
    if not mv_load.load.is_point_load():
        raise ValueError("Can only calculate response to point load")
    load_x_frac = mv_load.x_frac_at(time, c.bridge)
    il_matrix = ILMatrix.load(c, response_type, fem_runner)
    result = il_matrix.response_to(
        c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn)
    # print_d(f"load_x_frac = {load_x_frac}, at = {at}, kn = {mv_load.load.kn}, result = {result}")
    return result


def responses_to_mv_load(
        c: Config, mv_load: MovingLoad, response_type: ResponseType,
        fem_runner: FEMRunner, times: List[float], at: List[Point]):
    """The responses to a load over a number of time steps.

    Returns a numpy array of shape (time_end / time_step + 1, len(at)).

    """
    result = np.array([
        [response_at_time(c, mv_load, time, at_, response_type, fem_runner)
         for at_ in at]
        for time in times])
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    return result


def times_on_bridge(c: Config, mv_load: MovingLoad, times: List[float]):
    """Return only the times the moving load is on the bridge."""

    def on_bridge_at(time):
        x_frac = mv_load.x_frac_at(time, c.bridge)
        return 0 <= x_frac and x_frac <= 1

    return list(takewhile(on_bridge_at, times))
