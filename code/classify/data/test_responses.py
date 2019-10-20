"""Test classify.data.responses."""
import pytest

from classify.data.responses import response_to_mv_vehicles
from classify.data.scenarios import BridgeScenarioNormal, normal_traffic
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import MvVehicle
from model.response import ResponseType

c = bridge_705_test_config(bridge_705_3d)
c.il_num_loads = 10


def test_response_to_mv_vehicles():

    # All lanes are the same, so no error should be raised.
    mv_vehicles_gen = normal_traffic(c).mv_vehicles(lane=0)
    mv_vehicles = [next(mv_vehicles_gen) for _ in range(2)]
    response_to_mv_vehicles(
        c=c, mv_vehicles=mv_vehicles, bridge_scenario=None, time=1, at=Point(x=1),
        response_type=ResponseType.XTranslation, fem_runner=OSRunner(c))

    # Different lanes, so an error should be raised.
    for i, mv_vehicle in enumerate(mv_vehicles):
        mv_vehicle.lane = i
    with pytest.raises(ValueError) as e:
        response_to_mv_vehicles(
            c=c, mv_vehicles=mv_vehicles, bridge_scenario=BridgeScenarioNormal(),
            time=1, at=Point(x=1), response_type=ResponseType.XTranslation,
            fem_runner=OSRunner(c))
    assert "single lane" in str(e.value)
