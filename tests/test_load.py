from copy import deepcopy

import numpy as np

from bridge_sim.configs import test_config
from bridge_sim.model import PointLoad
from bridge_sim.vehicles import truck1
from bridge_sim.util import flatten

c = test_config(msl=10)

entering_time = truck1.time_entering_bridge(bridge=c.bridge)
entered_time = truck1.time_entered_bridge(bridge=c.bridge)
leaving_time = truck1.time_leaving_bridge(bridge=c.bridge)
left_time = truck1.time_left_bridge(bridge=c.bridge)
wagen1_top_lane = deepcopy(truck1)
wagen1_top_lane.lane = 1
assert truck1.lane != wagen1_top_lane.lane
assert truck1.init_x == 0


def test_to_point_load_pw():
    # As Truck 1 enters the bridge.
    wagen1_times = np.linspace(entering_time, entered_time - 0.001, 100)
    for time in wagen1_times:
        loads = truck1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_kn()
    # As Truck 1 is fully on the bridge.
    wagen1_times = np.linspace(entered_time, leaving_time, 100)
    for time in wagen1_times:
        loads = truck1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn == truck1.total_kn()
    # As Truck 1 is leaving the bridge.
    wagen1_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in wagen1_times:
        loads = truck1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_kn()


def test_wheel_to_wheel_track_xs():
    og_il_num_loads = c.il_num_loads
    c.il_num_loads = 10
    # Very beginning.
    (x0, f0), (x1, f1) = truck1.to_wheel_track_xs(c=c, wheel_x=0)
    assert x0 == c.bridge.x_min
    assert f0 == 1
    assert f1 == 0
    # Very end.
    (x0, f0), (x1, f1) = truck1.to_wheel_track_xs(c=c, wheel_x=c.bridge.x_max)
    assert x0 == c.bridge.x_max
    assert f0 == 1
    assert f1 == 0
    # In the middle.
    (x0, f0), (x1, f1) = truck1.to_wheel_track_xs(c=c, wheel_x=c.bridge.length / 2)
    assert f0 == 0.5
    assert f1 == 0.5
    bucket_width = c.bridge.length / (c.il_num_loads - 1)
    assert x0 == np.around(bucket_width * 4, 6)
    assert x1 == np.around(bucket_width * 5, 6)
    # Near the beginning (exact match).
    (x0, f0), (x1, f1) = truck1.to_wheel_track_xs(
        c=c, wheel_x=c.bridge.length / (c.il_num_loads - 1),
    )
    # The fraction might not be exactly 1, because of rounding of the wheel
    # track positions.
    assert np.around(f0, 4) == 1
    assert np.around(f1, 4) == 0
    assert x0 == np.around(bucket_width, 6)
    # Near the beginning (a little more).
    (x0, f0), (x1, f1) = truck1.to_wheel_track_xs(
        c=c, wheel_x=c.bridge.length / (c.il_num_loads - 1) + 0.001,
    )
    assert f0 != 0
    assert f0 != 1
    assert f0 + f1 == 1
    assert f0 > f1
    assert x0 == np.around(bucket_width, 6)
    assert x1 == np.around(bucket_width * 2, 6)
    c.il_num_loads = og_il_num_loads
