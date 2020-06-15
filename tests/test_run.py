"""Test running of "ULS" simulations."""

from bridge_sim import sim
from bridge_sim.configs import test_config
from bridge_sim.model import ResponseType


def test_point_load():
    """Test passing an index to 'point_load' runs the correct simulation."""
    config, exe_found = test_config()
    if not exe_found:
        return
    for index in [300, 1100]:
        sim_responses = list(sim.run.point_load(
            config=config,
            indices=[index],
            response_type=ResponseType.YTrans,
        ))[0]
        # plot.contour_responses(config, sim_responses)
        # plot.top_view_bridge(config.bridge, piers=True)
        # plot.plt.show()
        xs = config.bridge.wheel_track_xs(config)
        zs = config.bridge.axle_track_zs()
        x = xs[index % len(xs)]
        max_r, max_point = 1, None
        for response, point in sim_responses.values(point=True):
            if response < max_r:
                max_r = response
                max_point = point
        assert max_point[0] == x

