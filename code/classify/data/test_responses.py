"""Test classify.data.responses."""
import pytest

from classify.data.responses import response_to_mv_loads
from classify.data.scenarios import normal_traffic
from fem.run.opensees import os_runner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import MovingLoad
from model.response import ResponseType

c = bridge_705_config()
c.il_num_loads = 10


def test_response_to_mv_loads():

    # All lanes are the same, so no error should be raised.
    mv_loads = normal_traffic(c).mv_loads(num_vehicles=2, lane=0)
    response_to_mv_loads(
        c=c, mv_loads=mv_loads, bridge_scenario=None, time=1, at=Point(x=1), 
        response_type=ResponseType.XTranslation, fem_runner=os_runner(c))

    # Different lanes, so an error should be raised.
    for i, mv_load in enumerate(mv_loads):
        mv_load.load.lane = i
    with pytest.raises(Exception):
        response_to_mv_loads(
            c=c, mv_loads=mv_loads, time=1, at=Point(x=1),
            response_type=ResponseType.XTranslation, fem_runner=os_runner(c))
