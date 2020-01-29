"""Test classify.data.responses."""
import numpy as np
import pytest

from classify.data.responses import x_to_wheel_track_index
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import MvVehicle
from model.response import ResponseType

c = bridge_705_config(bridge_705_3d)
c.il_num_loads = 10


def test_x_to_wheel_track_index():
    wheel_track_index = x_to_wheel_track_index(c)
    assert wheel_track_index(c.bridge.x_min) == 0
    assert wheel_track_index(c.bridge.x_max) == c.il_num_loads - 1
    sml_bin_width = (c.bridge.length / (c.il_num_loads - 1)) / 2
    for x in np.linspace(c.bridge.x_min, c.bridge.x_max, 1000):
        wti = wheel_track_index(x)
        if x < c.bridge.x_min + sml_bin_width:
            assert wti == 0
        elif x > c.bridge.x_max - sml_bin_width:
            assert wti == c.il_num_loads - 1
        else:
            assert wti not in [0, c.il_num_loads - 1]
    assert wheel_track_index(c.bridge.x_min + sml_bin_width + 0.001) == 1
    assert (
        wheel_track_index(c.bridge.x_max - sml_bin_width - 0.001) == c.il_num_loads - 2
    )


# def test_response_to_mv_vehicles():

#     # All lanes are the same, so no error should be raised.
#     mv_vehicles_gen = normal_traffic(c).mv_vehicles(lane=0)
#     mv_vehicles = [next(mv_vehicles_gen) for _ in range(2)]
#     response_to_mv_vehicles(
#         c=c,
#         mv_vehicles=mv_vehicles,
#         bridge_scenario=None,
#         time=1,
#         at=Point(x=1),
#         response_type=ResponseType.XTranslation,
#         fem_runner=OSRunner(c),
#     )

#     # Different lanes, so an error should be raised.
#     for i, mv_vehicle in enumerate(mv_vehicles):
#         mv_vehicle.lane = i
#     with pytest.raises(ValueError) as e:
#         response_to_mv_vehicles(
#             c=c,
#             mv_vehicles=mv_vehicles,
#             bridge_scenario=BridgeScenarioNormal(),
#             time=1,
#             at=Point(x=1),
#             response_type=ResponseType.XTranslation,
#             fem_runner=OSRunner(c),
#         )
#     assert "single lane" in str(e.value)
