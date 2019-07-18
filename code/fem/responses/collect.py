"""Collect responses based on the IL matrices."""
import numpy as np

from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *


def response_at_time(
        c: Config, mv_load: MovingLoad, time: float, at: Point,
        response_type: ResponseType, fem_runner: FEMRunner):
    """The response to a load at a given time."""
    load_x_frac = mv_load.x_frac_at(time, c.bridge)
    il_matrix = ILMatrix.load(c, response_type, fem_runner)
    if not mv_load.load.is_point_load():
        raise ValueError("Can only calculate response to point load")
    return il_matrix.response(
        c.bridge.x_frac(at.x), load_x_frac, mv_load.load.kn)


def responses_to_mv_load(
        c: Config, mv_load: MovingLoad, time_step: float, time_end: float,
        at: List[Point], response_type: ResponseType, fem_runner: FEMRunner):
    """The responses to a load over a number of time steps.

    Returns a numpy array of shape (time_end / time_step + 1, len(at)).

    """
    num_times = (time_end / time_step) + 1
    responses = []
    for time in np.linspace(0, time_end, num_times):
        time_responses = [
            response_at_time(c, mv_load, time, at_, response_type, fem_runner)
            for at_ in at]
        responses.append(time_responses)
        assert len(time_responses) == len(at)
    return np.array(responses)


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
