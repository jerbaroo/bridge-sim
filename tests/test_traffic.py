"""Test traffic generation."""

import numpy as np

from bridge_sim.configs import test_config
from bridge_sim.model import Vehicle
from bridge_sim.sim.run import ulm_xzs
from bridge_sim.traffic import normal_traffic, load_traffic
from bridge_sim.util import flatten

config = test_config(msl=10)[0]


def test_load_traffic():
    time = 10
    traffic_scenario = normal_traffic(config=config)
    ts1, t1, ta1 = load_traffic(
        config=config,
        traffic_scenario=traffic_scenario,
        time=time,
    )
    ts2, t2, ta2 = load_traffic(
        config=config,
        traffic_scenario=traffic_scenario,
        time=time,
    )
    assert (ta1 == ta2).all()


def test_traffic_scenario():
    time = 10
    traffic_scenario = normal_traffic(config=config)
    traffic_sequence = traffic_scenario.traffic_sequence(config, time)
    warmed_up = max(
        vs[0].time_left_bridge(config.bridge)
        for vs in traffic_sequence.vehicles_per_lane
    )
    assert traffic_sequence.start_time == warmed_up
    assert traffic_sequence.final_time == warmed_up + time


def test_traffic_and_traffic_array():
    time = 10
    traffic_scenario = normal_traffic(config=config)
    traffic_sequence = traffic_scenario.traffic_sequence(config, time)
    traffic = traffic_sequence.traffic()
    traffic_array = traffic_sequence.traffic_array()
    assert len(traffic_sequence.times) == 1 + time / config.sensor_hz
    assert len(traffic) == len(traffic_sequence.times)
    assert len(traffic_array) == len(traffic_sequence.times)

    xzs = ulm_xzs(config)
    wheel_track_xs = config.bridge.wheel_track_xs(config)

    for t, time in enumerate(traffic_sequence.times):
        traffic_vehicles = flatten(traffic[t], Vehicle)
        # Assert the amount of load is equal in both cases.
        traffic_load = 0
        for v in traffic_vehicles:
            for point_load in v.point_load_pw(config, time, list=True):
                traffic_load += point_load.load
        assert np.isclose(traffic_load, sum(traffic_array[t]))
        # Assert the position of loads is equal in both cases.
        for v in traffic_vehicles:
            for point_load in v.point_load_pw(config, time, list=True):
                (lo, weight_lo), (hi, weight_hi) = v._axle_track_weights(
                    point_load.x, wheel_track_xs
                )
                lo = lo + v.lane * config.il_num_loads
                if hi is None:
                    x = xzs[lo][0]
                    assert np.isclose(x, point_load.x)
                else:
                    hi = hi + v.lane * config.il_num_loads
                    x0, z0 = xzs[lo]
                    x1, z1 = xzs[hi]
                    assert x0 < point_load.x
                    assert x1 > point_load.x
                    if point_load.z < 0:
                        assert z0 < 0
                        assert z1 < 0
                    else:
                        assert z0 > 0
                        assert z1 > 0

