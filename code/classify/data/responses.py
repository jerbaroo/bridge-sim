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
    print_d(f"{mv_load.load!r}")
    load_x_frac = mv_load.x_frac_at(time, c.bridge)
    il_matrix = ILMatrix.load(c, response_type, fem_runner)
    if mv_load.load.is_point_load():
        return il_matrix.response_to(
            c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn)
    # Vehicle load.
    else:
        response = 0
        for i in range(mv_load.load.num_axles):
            # Update load position for each axle.
            if i != 0:
                axle_distance = mv_load.load.axle_distances[i - 1] / 100
                print(f"axle_distance = {axle_distance}")
                load_x_frac += c.bridge.x_frac(axle_distance)
                print(f"load_x_frac = {load_x_frac}")
            response += il_matrix.response_to(
                c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn)
    # print_d(f"load_x_frac = {load_x_frac}, at = {at}, kn = {mv_load.load.kn}, result = {result}")
    return response


def responses_to_mv_load(
        c: Config, mv_load: MovingLoad, response_type: ResponseType,
        fem_runner: FEMRunner, times: List[float], at: List[Point]):
    """The responses to a load over a number of time steps.

    Returns a numpy array of shape (len(times), len(at)).

    """
    print(times)
    result = np.array([
        [response_at_time(c, mv_load, time, at_, response_type, fem_runner)
         for at_ in at]
        for time in times])
    print(result.shape)
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    return result


def times_on_bridge(c: Config, mv_load: MovingLoad, times: List[float]):
    """Return only the times the moving load is on the bridge."""

    def on_bridge_at(time):
        min_x_frac = mv_load.x_frac_at(time, c.bridge)
        max_x_frac = min_x_frac
        if not mv_load.load.is_point_load():
            vehicle_length = sum(mv_load.load.axle_distances) / 100  # From cm.
            print(f"vehicle length = {vehicle_length}")
            max_x_frac += c.bridge.x_frac(vehicle_length)
        return (
            0 <= min_x_frac and min_x_frac <= 1 and
            0 <= max_x_frac and max_x_frac <= 1)

    return list(takewhile(on_bridge_at, times))
