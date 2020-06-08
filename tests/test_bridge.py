import numpy as np

from bridge_sim.bridges.bridge_705 import bridge_705
from bridge_sim.configs import opensees_default

c = opensees_default(bridge_705(0.5))
c.il_num_loads = 10


def test_wheel_track_xs():
    wheel_track_xs = c.bridge.wheel_track_xs(c)
    delta_x = c.bridge.length / (c.il_num_loads - 1)
    assert wheel_track_xs[0] == c.bridge.x_min
    assert wheel_track_xs[1] == np.around(c.bridge.x_min + delta_x, 6)
    assert wheel_track_xs[-1] == c.bridge.x_max
    assert wheel_track_xs[-2] == np.around(c.bridge.x_max - delta_x, 6)
