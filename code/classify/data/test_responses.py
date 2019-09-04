"""Test classify.data.responses."""
import pytest

from classify.data.responses import response_to_mv_loads
from classify.data.scenarios import normal_traffic
from fem.run.opensees import os_runner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import Load, MovingLoad
from model.response import ResponseType


def test_response_to_mv_loads():
    c = bridge_705_config()

    # All lanes are the same, so no error should be raised.
    mv_loads = [
        MovingLoad.from_vehicle(
            x_frac=0, vehicle=normal_traffic.vehicle(c), lane=0)
        for _ in range(2)]
    response_to_mv_loads(
        c=c, mv_loads=mv_loads, time=1, at=Point(x=1),
        response_type=ResponseType.XTranslation, fem_runner=os_runner(c))

    # Different lanes, so an error should be raised.
    mv_loads = [
        MovingLoad.from_vehicle(
            x_frac=0, vehicle=normal_traffic.vehicle(c), lane=i)
        for i in range(2)]
    with pytest.raises(Exception):
        response_to_mv_loads(
            c=c, mv_loads=mv_loads, time=1, at=Point(x=1),
            response_type=ResponseType.XTranslation, fem_runner=os_runner(c))
