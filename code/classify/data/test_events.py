"""Test events.py."""
import numpy as np

from classify.data.events import events_from_mv_loads
from fem.run.opensees import os_runner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import MovingLoad
from model.response import Event, ResponseType


def test_events_from_mv_loads():
    c = bridge_705_config()

    mv_loads = [MovingLoad.sample(c=c, x_frac=0, lane=0) for _ in range(2)]
    response_types = [ResponseType.Strain, ResponseType.Stress]
    at = [Point(x=c.bridge.x(x_frac)) for x_frac in np.linspace(0, 1, num=10)]
    events = list(events_from_mv_loads(
        c=c, mv_loads=mv_loads, response_types=response_types,
        fem_runner=os_runner(c), at=at))
    shape = np.array(events).shape
    assert len(shape) == 3
    assert shape[0] == len(at)
    assert shape[1] == len(response_types)
    assert isinstance(events[0][0], list)
    assert isinstance(events[0][0][0], Event)
