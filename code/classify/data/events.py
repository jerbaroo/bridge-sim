"""Generate, save and load events."""
from typing import List

import numpy as np

from classify.data.recorder import Recorder
from classify.data.responses import responses_to_mv_loads
from classify.data.trigger import Trigger, always_trigger
from config import Config
from fem.run import FEMRunner
from model.bridge import Point
from model.load import MovingLoad
from model.response import Event, ResponseType


def events_from_mv_loads(
        c: Config, mv_loads: List[MovingLoad],
        response_types: List[ResponseType], fem_runner: FEMRunner,
        at: List[Point], per_axle: bool = False,
        trigger: Trigger = always_trigger()) -> List[List[List[Event]]]:
    """Return events generated from moving loads.

    Each yielded result is of shape (len(at), len(response_type), #events), a
    list of Event for each sensor position and response type.

    """
    # Collect responses for each sensor position and response type.
    responses = responses_to_mv_loads(
        c=c, mv_loads=mv_loads, response_types=response_types,
        fem_runner=fem_runner, at=at, per_axle=per_axle)

    shape = np.array(responses).shape
    assert len(shape) == 3
    assert shape[1] == len(at)
    assert shape[2] == len(response_types)

    # Construct a Recorder for each sensor position and response type.
    recorders = [
        [Recorder(c=c, trigger=trigger, response_type=response_type)
         for response_type in response_types]
        for _ in range(len(at))]

    shape = np.array(recorders).shape
    assert len(shape) == 2
    assert shape[0] == len(at)
    assert shape[1] == len(response_types)

    # Events are collected for each sensor position and response type.
    events = [
        [[] for _r in range(len(response_types))]
        for _a in range(len(at))]

    # For the responses at each time.
    for response in responses:
        for a in range(len(at)):
            for r in range(len(response_types)):
                recorders[a][r].receive(response[a][r])
                maybe_event = recorders[a][r].maybe_event()
                if maybe_event is not None:
                    events[a][r].append(maybe_event)
    return events
