"""Test "Vehicle" methods."""

from copy import deepcopy

import pytest

import numpy as np

from bridge_sim.configs import test_config
from bridge_sim.model import Vehicle, PointLoad
from bridge_sim.util import flatten
from bridge_sim.vehicles import truck1

config = test_config(msl=10)[0]


def test_constructor():
    with pytest.raises(ValueError):
        Vehicle(kn=[100], axle_distances=[1], axle_width=2.5, kmph=20)


def test_is_load_per_axle():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20)
    assert not v._is_load_per_axle()
    v = Vehicle(kn=[25, 25], axle_distances=[1], axle_width=2.5, kmph=20)
    assert v._is_load_per_axle()


def test_total_load():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20)
    assert v.total_load() == 100
    v = Vehicle(kn=[25, 25], axle_distances=[1], axle_width=2.5, kmph=20)
    assert v.total_load() == 50


def test_load_per_axle():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20)
    assert len(v.load_per_axle()) == 2
    assert sum(v.load_per_axle()) == 100
    v = Vehicle(kn=[25, 25], axle_distances=[1], axle_width=2.5, kmph=20)
    assert len(v.load_per_axle()) == 2
    assert sum(v.load_per_axle()) == 50


def test_wheel_track_zs():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20)
    assert v.wheel_tracks_zs(config) == [-9.65, -7.15]
    assert v.wheel_tracks_zs(config) != [-9.60, -7.15]
    # Second lane.
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1)
    assert v.wheel_tracks_zs(config) == [+7.15, +9.65]


def test_xs_at():
    # Lane 0, time 0.
    v0 = Vehicle(kn=100, axle_distances=[1, 1.5], axle_width=2.5, kmph=20)
    xs = v0.xs_at(times=[0], bridge=config.bridge)[0]
    assert xs[0] == 0
    assert xs[1] == -1
    assert xs[2] == -2.5
    # Lane 1, time 0.
    v1 = Vehicle(kn=100, axle_distances=[1, 1.5], axle_width=2.5, kmph=20, lane=1)
    xs = v1.xs_at(times=[0], bridge=config.bridge)[0]
    assert xs[0] == config.bridge.x_max
    assert xs[1] == config.bridge.x_max + 1
    assert xs[2] == config.bridge.x_max + 2.5
    # Lane 0, times 1 and 8.
    xs = v0.xs_at(times=[1, 8], bridge=config.bridge)
    front = 5.5555555556
    assert np.isclose(xs[0][0], front)
    assert np.isclose(xs[0][1], front - 1)
    assert np.isclose(xs[0][2], front - 2.5)
    front = 44.4444444444
    assert np.isclose(xs[1][0], front)
    assert np.isclose(xs[1][1], front - 1)
    assert np.isclose(xs[1][2], front - 2.5)
    # Lane 1, times 1 and 8.
    xs = v1.xs_at(times=[1, 8], bridge=config.bridge)
    front = config.bridge.x_max - 5.5555555556
    assert np.isclose(xs[0][0], front)
    assert np.isclose(xs[0][1], front + 1)
    assert np.isclose(xs[0][2], front + 2.5)
    front = config.bridge.x_max - 44.4444444444
    assert np.isclose(xs[1][0], front)
    assert np.isclose(xs[1][1], front + 1)
    assert np.isclose(xs[1][2], front + 2.5)
    # Lane 0, times 0 and 3, starts behind.
    v = Vehicle(kn=100, axle_distances=[1, 1.5], axle_width=2.5, kmph=20, init_x=-20)
    xs = v.xs_at(times=[0, 3], bridge=config.bridge)
    front = -20
    assert xs[0][0] == front
    assert xs[0][1] == front - 1
    assert xs[0][2] == front - 2.5
    front = -3.3333333333
    assert np.isclose(xs[1][0], front)
    assert np.isclose(xs[1][1], front - 1)
    assert np.isclose(xs[1][2], front - 2.5)
    # Lane 1, times 0 and 3, starts behind.
    v = Vehicle(kn=100, axle_distances=[1, 1.5], axle_width=2.5, kmph=20, lane=1, init_x=-20)
    xs = v.xs_at(times=[0, 3], bridge=config.bridge)
    front = config.bridge.x_max + 20
    assert xs[0][0] == front
    assert xs[0][1] == front + 1
    assert xs[0][2] == front + 2.5
    front = config.bridge.x_max + 3.3333333333
    assert np.isclose(xs[1][0], front)
    assert np.isclose(xs[1][1], front + 1)
    assert np.isclose(xs[1][2], front + 2.5)


def test_x_at():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20)
    assert np.isclose(v.x_at(time=1, bridge=config.bridge), 5.5555555556)


def test_on_bridge():
    for lane in [0, 1]:
        # Negative time.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).on_bridge(
            time=-0.0000001, bridge=config.bridge,
        )
        # Negative init_x.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, init_x=-0.0000001, lane=lane).on_bridge(
            time=0, bridge=config.bridge,
        )
        # Time 0.
        assert Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).on_bridge(
            time=0, bridge=config.bridge,
        )
        # Time 1, init_x ~= - kmph / 3.6.
        assert Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, init_x=-5.5555555555, lane=lane).on_bridge(
            time=1, bridge=config.bridge,
        )
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, init_x=-5.5555555556, lane=lane).on_bridge(
            time=1, bridge=config.bridge,
        )
        # Time ~= (bridge length + 1) / kmph / 3.6.
        assert Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).on_bridge(
            time=18.675, bridge=config.bridge,
        )
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).on_bridge(
            time=18.675001, bridge=config.bridge,
        )


def test_passed_bridge():
    for lane in [0, 1]:
        # Time 0.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).passed_bridge(
            time=0, bridge=config.bridge,
        )
        # Negative time.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).passed_bridge(
            time=-1, bridge=config.bridge,
        )
        # Negative init x.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane, init_x=-1).passed_bridge(
            time=0, bridge=config.bridge,
        )
        # Front axle at x_max.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).passed_bridge(
            time=18.495, bridge=config.bridge,
        )
        # Rear axle at x_max.
        assert not Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).passed_bridge(
            time=18.675, bridge=config.bridge,
        )
        # Rear axle passed x_max.
        assert Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane).passed_bridge(
            time=18.675001, bridge=config.bridge,
        )


def test_time_at():
    # Lane 0 half way.
    halfway_time = 9.2475
    assert halfway_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_at(
        x=102.75 / 2, bridge=config.bridge,
    )
    # Lane 1 half way.
    assert halfway_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_at(
        x=102.75 / 2, bridge=config.bridge,
    )
    # Lane 0 full way.
    fullway_time = 18.495
    assert fullway_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_at(
        x=102.75, bridge=config.bridge,
    )
    # Lane 1 full way.
    assert fullway_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_at(
        x=0, bridge=config.bridge,
    )
    # Lane 0 passed bridge.
    passed_time = 19.035
    assert passed_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0, init_x=-2).time_at(
        x=103.75, bridge=config.bridge,
    )
    # Lane 1 passed bridge.
    assert passed_time == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1, init_x=-2).time_at(
        x=-1, bridge=config.bridge,
    )


def test_time_entering_bridge():
    # Lane 0, init x 0.
    assert 0 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_entering_bridge(config.bridge)
    # Lane 1, init x 0.
    assert 0 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_entering_bridge(config.bridge)
    # Lane 0, init x negative.
    assert np.isclose(
        0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0, init_x=-1).time_entering_bridge(config.bridge)
    )
    # Lane 1, init x negative.
    assert np.isclose(
        0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1, init_x=-1).time_entering_bridge(config.bridge)
    )


def test_time_entered_bridge():
    # Lane 0, init x 0.
    assert 0.18 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_entered_bridge(config.bridge)
    # Lane 1, init x 0.
    assert 0.18 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_entered_bridge(config.bridge)
    # Lane 0, init x negative.
    assert np.isclose(
        0.18 * 2,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0, init_x=-1).time_entered_bridge(config.bridge)
    )
    # Lane 1, init x negative.
    assert np.isclose(
        0.18 * 2,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1, init_x=-1).time_entered_bridge(config.bridge)
    )


def test_time_leaving_bridge():
    # Lane 0, init x 0.
    assert 18.495 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_leaving_bridge(config.bridge)
    # Lane 1, init x 0.
    assert 18.495 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_leaving_bridge(config.bridge)
    # Lane 0, init x negative.
    assert np.isclose(
        18.495 + 0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0, init_x=-1).time_leaving_bridge(config.bridge)
    )
    # Lane 1, init x negative.
    assert np.isclose(
        18.495 + 0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1, init_x=-1).time_leaving_bridge(config.bridge)
    )


def test_time_left_bridge():
    # Lane 0, init x 0.
    assert 18.495 + 0.18 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0).time_left_bridge(
        config.bridge)
    # Lane 1, init x 0.
    assert 18.495 + 0.18 == Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1).time_left_bridge(
        config.bridge)
    # Lane 0, init x negative.
    assert np.isclose(
        18.495 + 2 * 0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0, init_x=-1).time_left_bridge(
            config.bridge)
    )
    # Lane 1, init x negative.
    assert np.isclose(
        18.495 + 2 * 0.18,
        Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=1, init_x=-1).time_left_bridge(
            config.bridge)
    )


def test__axle_track_weights():
    for lane in [0, 1]:
        v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=lane)
        xs = config.bridge.wheel_track_xs(config)
        # Wheel x = 0.
        (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(0, xs)
        assert lo == 0
        assert weight_lo == 1
        assert hi is None
        assert weight_hi == 0
        # Wheel x = 0.000001.
        (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(0.000001, xs)
        assert lo == 0
        assert weight_lo == 1 - (0.000001 / xs[1])
        assert hi == 1
        assert weight_hi == 0.000001 / xs[1]
        # Wheel x = halfway first bucket.
        halfway_x = xs[1] / 2
        (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(halfway_x, xs)
        assert lo == 0
        assert weight_lo == 0.5
        assert hi == 1
        assert weight_hi == 0.5
        # Wheel x = first bucket.
        (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(xs[1], xs)
        assert lo == 1
        assert weight_lo == 1
        assert hi is None
        assert weight_hi == 0
        # Wheel x = last bucket.
        assert xs[-1] == 102.75
        (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(xs[-1], xs)
        assert lo == 599
        assert weight_lo == 1
        assert hi is None
        assert weight_hi == 0


def test_axle_track_indices():
    # Mostly tested by function above. So just one small test per lane.
    # Lane 0, first bucket.
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0)
    indices = list(v._axle_track_indices(config, times=[0]))
    assert len(indices) == 1
    assert len(indices[0]) == 1
    (lo, load_lo), (hi, load_hi) = indices[0][0]
    assert lo == 0
    assert load_lo == 50  # Two axles (50 on one of them).
    assert hi is None
    assert load_hi == 0
    # Lane 0, halfway through first bucket.
    (lo, load_lo), (hi, load_hi) = list(v._axle_track_indices(config, times=[0.0001]))[0][0]
    assert lo == 0
    assert hi == 1
    assert load_lo + load_hi == 50
    assert load_lo < 50
    # Lane 1.
    v = Vehicle(kn=[25, 40], axle_distances=[1], axle_width=2.5, kmph=20, lane=1)
    indices = list(v._axle_track_indices(config, times=[0]))
    assert len(indices) == 1
    assert len(indices[0]) == 1
    (lo, load_lo), (hi, load_hi) = indices[0][0]
    assert lo == 1199
    assert load_lo == 25  # 25 on the front axle.
    assert hi is None
    assert load_hi == 0


def test__times_on_bridge():
    v = Vehicle(kn=100, axle_distances=[1], axle_width=2.5, kmph=20, lane=0)
    sorted_times = np.arange(-1, 100, config.sensor_hz)
    v_times_indices, v_times = v._times_on_bridge(config, sorted_times)
    assert len(v_times_indices) == len(v_times)
    for v_times_index, v_time in zip(v_times_indices, v_times):
        assert v_time == sorted_times[v_times_index]
    assert v.on_bridge(time=sorted_times[v_times_indices[0]], bridge=config.bridge)
    assert v.on_bridge(time=sorted_times[v_times_indices[-1]], bridge=config.bridge)
    if v_times_indices[0] > 0:
        assert not v.on_bridge(time=sorted_times[v_times_indices[0] - 1], bridge=config.bridge)
    if v_times_indices[-1] < len(sorted_times) - 1:
        assert not v.on_bridge(time=sorted_times[v_times_indices[-1] + 1], bridge=config.bridge)


def test_to_point_load_pw():
    entering_time = truck1.time_entering_bridge(bridge=config.bridge)
    entered_time = truck1.time_entered_bridge(bridge=config.bridge)
    leaving_time = truck1.time_leaving_bridge(bridge=config.bridge)
    left_time = truck1.time_left_bridge(bridge=config.bridge)
    wagen1_top_lane = deepcopy(truck1)
    wagen1_top_lane.lane = 1
    assert truck1.lane != wagen1_top_lane.lane
    assert truck1.init_x == 0
    # As Truck 1 enters the bridge.
    wagen1_times = np.linspace(entering_time, entered_time - 0.001, 100)
    for time in wagen1_times:
        loads = truck1.point_load_pw(config=config, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_load()
    # As Truck 1 is fully on the bridge.
    wagen1_times = np.linspace(entered_time, leaving_time, 100)
    for time in wagen1_times:
        loads = truck1.point_load_pw(config=config, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn == truck1.total_load()
    # As Truck 1 is leaving the bridge.
    wagen1_times = np.linspace(leaving_time + 0.001, left_time, 100)
    for time in wagen1_times:
        loads = truck1.point_load_pw(config=config, time=time)
        flat_loads = flatten(loads, PointLoad)
        total_kn = sum(map(lambda l: l.load, flat_loads))
        assert total_kn < truck1.total_load()

