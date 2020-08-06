"""Test "Bridge" methods."""

import numpy as np

from bridge_sim import configs

c, exe_found = configs.test_config(msl=10)
c.il_num_loads = 10


def test_wheel_track_xs():
    if not exe_found:
        return
    wheel_track_xs = c.bridge.wheel_track_xs(c)
    delta_x = c.bridge.length / (c.il_num_loads - 1)
    assert wheel_track_xs[0] == c.bridge.x_min
    assert wheel_track_xs[1] == np.around(c.bridge.x_min + delta_x, 6)
    assert wheel_track_xs[-1] == c.bridge.x_max
    assert wheel_track_xs[-2] == np.around(c.bridge.x_max - delta_x, 6)
