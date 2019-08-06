"""Time series of responses to normal moving loads."""
from typing import Iterable, List, NewType, Optional

import numpy as np

from classify.data.responses import responses_to_mv_load, times_on_bridge
from config import Config
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import MovingLoad, Point, ResponseType
from model.bridge_705 import bridge_705_config
from vehicles.sample import sample_vehicle

Array2D = NewType("Array2D", np.ndarray)


def responses_to_normal_mv_load(
        c: Config, response_type: ResponseType, fem_runner: FEMRunner,
        lane: int, at: List[Point], group_index: Optional[int]=None,
        l_to_r: bool=True
    ) -> Array2D:
    """The responses to a sampled normal load over a number of time steps.

    Indexed first by time and then by sensor position. The responses are
    collected until time_end or until the vehicle is no longer on the bridge,
    whichever comes first.

    Args:
        c: Config, simulation configuration.
        response_type: ResponseType, type of the response to collect.
        fem_runner: FEMRunner, program the run the FEM simulation.
        lane: int, index of the lane on the bridge.
        at: List[Point], points at which to collect responses.
        group_index: Optional[int], if given sample from that group index.
        l_to_r: bool, direction of the vehicle, left to right or opposite.
     

    """
    vehicle = sample_vehicle(c, group_index)
    mv_load = MovingLoad.from_vehicle(
        x_frac=0, vehicle=vehicle, lane=lane, l_to_r=l_to_r)
    times = times_on_bridge_(
        c, mv_load, time_step=time_step, time_end=time_end)
    return responses_to_mv_load(
        c, mv_load, response_type, fem_runner, times, at)


if __name__ == "__main__":
    c = bridge_705_config()
    at = [Point(x=c.bridge.x(x_frac)) for x_frac in np.linspace(0, 1, 100)]
    resp = responses_to_normal_mv_load(
        c, ResponseType.Strain, os_runner(c), 0, at, 0.1, 10)
