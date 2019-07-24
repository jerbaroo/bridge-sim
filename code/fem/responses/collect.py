"""Collect responses based on the IL matrices."""
import numpy as np
from typing import List

from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *
from util import *


def response_at_time(
        c: Config, mv_load: MovingLoad, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner):
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
    responses = []
    for time in times:
        responses.append([
            response_at_time(c, mv_load, time, at_, response_type, fem_runner)
            for at_ in at])
    result = np.array(responses)
    assert result.shape[0] == len(times)
    assert result.shape[1] == len(at)
    return result


if __name__ == "__main__":
    c = bridge_705_config()
    mv_load = MovingLoad(Load(x_frac=0, kn=5000), kmph=20)
    at = [Point(x_frac) for x_frac in np.linspace(0, 1, 10)]
    response_type = ResponseType.XTranslation
    fem_runner = os_runner(c)

    responses = responses_to_mv_load(
        c, mv_load, time_step=0.1, time_end=10, at=at,
        response_type=response_type, fem_runner=fem_runner)
    print(responses)
