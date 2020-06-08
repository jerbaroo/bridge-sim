from copy import deepcopy
import numpy as np

from bridge_sim.bridges.bridge_705 import bridge_705
from bridge_sim.configs import opensees_default
from bridge_sim.vehicles import truck1
from bridge_sim.model import PointLoad
from bridge_sim.util import flatten

c = opensees_default(bridge_705(0.5))
entering_time = truck1.time_entering_bridge(bridge=c.bridge)
entered_time = truck1.time_entered_bridge(bridge=c.bridge)
leaving_time = truck1.time_leaving_bridge(bridge=c.bridge)
left_time = truck1.time_left_bridge(bridge=c.bridge)
wagen1_top_lane = deepcopy(truck1)
wagen1_top_lane.lane = 1
assert truck1.lane != wagen1_top_lane.lane
assert truck1.init_x_frac == 0


def test_mv_vehicle_time_leaving_bridge():
    # Bottom lane.
    assert c.bridge.length / truck1.mps == truck1.time_leaving_bridge(c.bridge)
    # Top lane.
    assert c.bridge.length / wagen1_top_lane.mps == wagen1_top_lane.time_leaving_bridge(
        c.bridge
    )


def test_mv_vehicle_time_left_bridge():
    # Bottom lane.
    time_to_leave = truck1.time_left_bridge(c.bridge) - truck1.time_leaving_bridge(
        c.bridge
    )
    assert np.isclose(truck1.length / truck1.mps, time_to_leave)
    # Top lane.
    time_to_leave = wagen1_top_lane.time_left_bridge(
        c.bridge
    ) - wagen1_top_lane.time_leaving_bridge(c.bridge)
    assert np.isclose(wagen1_top_lane.length / wagen1_top_lane.mps, time_to_leave)


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


def test_to_wheel_track_loads():
    # As Truck 1 enters the bridge, total load is less than Truck 1.
    enter_times = np.linspace(entering_time, entered_time - 0.001, 100)
    for time in enter_times:
        loads = truck1.to_wheel_track_loads(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_kn()
    # As Truck 1 is fully on the bridge, total load equals that of Truck 1.
    on_times = np.linspace(entered_time, leaving_time, 100)
    truck_front_x = np.arange(8, 102)
    more_times = np.array([truck1.time_at(x=x, bridge=c.bridge) for x in truck_front_x])
    on_times = np.concatenate((on_times, more_times))
    for time in on_times:
        loads = truck1.to_wheel_track_loads(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert np.isclose(total_kn, truck1.total_kn())
    # As Truck 1 is leaving the bridge, total load is less than Truck 1.
    leave_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in leave_times:
        loads = truck1.to_wheel_track_loads(c=c, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_kn()


def test_wheel_track_loads_on_track():
    wheel_track_xs = c.bridge.wheel_track_xs(c)
    enter_times = np.linspace(entering_time, entered_time - 0.001, 100)
    on_times = np.linspace(entered_time, leaving_time, 100)
    leave_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in np.concatenate((enter_times, on_times, leave_times)):
        loads = truck1.to_wheel_track_loads(c=c, time=time, flat=True)
        for load in loads:
            assert any(np.isclose(load.x, x) for x in wheel_track_xs)


def test_compare_to_wheel_track_and_to_point_load():
    truck_front_x = np.arange(1, 116.1, 1)
    times = [truck1.time_at(x=x, bridge=c.bridge) for x in truck_front_x]
    loads_wt = [
        [v.to_wheel_track_loads(c=c, time=time) for v in [truck1]] for time in times
    ]
    # print_w(f"Not using fractions of wheel track bins in simulation")
    loads_pw = [
        [v.to_point_load_pw(time=time, bridge=c.bridge) for v in [truck1]]
        for time in times
    ]

    def sum_loads(loads):
        """Sum of the load intensity (kn) of all given loads."""
        return sum(map(lambda l: l.load, flatten(loads, PointLoad)))

    for i in range(len(times)):
        # Assert that the total load intensity is equal for both functions.
        wt, pw = np.array(loads_wt[i]), np.array(loads_pw[i])
        sum_wt = np.around(sum_loads(wt), 5)
        sum_pw = np.around(sum_loads(pw), 5)
        assert sum_wt == sum_pw
        # Assert the shape of fem is as expected.
        assert wt.shape[0] == 1  # One vehicles.
        assert pw.shape[0] == 1  # One vehicles.
        # Assert that both loads have equal amount of axles.
        assert wt.shape[1] == pw.shape[1]
        # Assert that at each time, the shape of loads is as expected.
        if wt.shape[1] >= 1:
            assert len(wt.shape) >= 3
            assert len(pw.shape) == 3
            assert wt.shape[2] == 2
            assert pw.shape[2] == 2
            if len(wt.shape) == 4:
                assert wt.shape[3] == 2
            # Assert that x positions of loads match up.
            for axle_i in range(wt.shape[1]):
                for wt_load, pw_load in zip(wt[0][axle_i], pw[0][axle_i]):
                    # Total kn should be equal between both functions..
                    wt_kn = sum_loads(wt_load)
                    assert np.isclose(wt_kn, pw_load.load)
                    # ..x positions should match up too.
                    if len(wt_load) == 1:
                        assert np.isclose(wt_load[0].x, pw_load.x)
                    elif len(wt_load) == 2:
                        assert wt_load[0].x < pw_load.x < wt_load[1].x
                    else:
                        assert False
