from copy import deepcopy
import numpy as np

from classify.vehicle import wagen1
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import MvVehicle, PointLoad, Vehicle
from util import flatten

c = bridge_705_config(bridge_705_3d)
entering_time = wagen1.time_entering_bridge(bridge=c.bridge)
entered_time = wagen1.time_entered_bridge(bridge=c.bridge)
leaving_time = wagen1.time_leaving_bridge(bridge=c.bridge)
left_time = wagen1.time_left_bridge(bridge=c.bridge)
wagen1_top_lane = deepcopy(wagen1)
wagen1_top_lane.lane = 1
assert wagen1.lane != wagen1_top_lane.lane
assert wagen1.init_x_frac == 0


def test_mv_vehicle_time_leaving_bridge():
    # Bottom lane.
    assert c.bridge.length / wagen1.mps == wagen1.time_leaving_bridge(c.bridge)
    # Top lane.
    assert c.bridge.length / wagen1_top_lane.mps == wagen1_top_lane.time_leaving_bridge(
        c.bridge
    )


def test_mv_vehicle_time_left_bridge():
    # Bottom lane.
    time_to_leave = wagen1.time_left_bridge(c.bridge) - wagen1.time_leaving_bridge(
        c.bridge
    )
    assert np.isclose(wagen1.length / wagen1.mps, time_to_leave)
    # Top lane.
    time_to_leave = wagen1_top_lane.time_left_bridge(
        c.bridge
    ) - wagen1_top_lane.time_leaving_bridge(c.bridge)
    assert np.isclose(wagen1_top_lane.length / wagen1_top_lane.mps, time_to_leave)


def test_to_point_load_pw():
    # As Truck 1 enters the bridge.
    wagen1_times = np.linspace(entering_time, entered_time - 0.001, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        assert total_kn < wagen1.total_kn()
    # As Truck 1 is fully on the bridge.
    wagen1_times = np.linspace(entered_time, leaving_time, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        assert total_kn == wagen1.total_kn()
    # As Truck 1 is leaving the bridge.
    wagen1_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_load_pw(time=time, bridge=c.bridge)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        assert total_kn < wagen1.total_kn()


def test_to_point_loads_buckets():
    # As Truck 1 enters the bridge.
    return
    wagen1_times = np.linspace(entering_time, entered_time - 0.001, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_loads_buckets(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        assert total_kn < wagen1.total_kn()
    # As Truck 1 is fully on the bridge.
    wagen1_times = np.linspace(entered_time, leaving_time, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_loads_buckets(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        print(time)
        print(total_kn)
        print(wagen1.total_kn())
        assert np.isclose(total_kn, wagen1.total_kn())
    # As Truck 1 is leaving the bridge.
    wagen1_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in wagen1_times:
        loads = wagen1.to_point_loads_buckets(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.kn, flat_loads))
        assert total_kn < wagen1.total_kn()


# def test_mv_vehicle_to_point_loads():
#     wagen1 = get_wagen1()
#     loads = wagen1.to_point_loads(time=2, bridge=c.bridge)
#     assert len(loads) == 4
#     assert loads[0][0].kn == 5050
#     assert loads[0][1].kn == 5300
#     assert loads[0][0].z_frac > loads[0][1].z_frac


# def test_mv_vehicle_time_at():
#     wagen1 = get_wagen1()
#     mps = wagen1.kmph / 3.6
#     assert wagen1.time_at(x=20, bridge=c.bridge) == 20 / mps
#     assert wagen1.time_at(x=102.75, bridge=c.bridge) == 102.75 / mps
