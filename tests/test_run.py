from bridge_sim.configs import test_config
from bridge_sim.model import Point, ResponseType
from bridge_sim.sim import run


def test_point_load():
    """Test passing an index to 'point_load' runs the correct simulation."""
    config, exe_found = test_config()
    if not exe_found:
        return
    for index in [100, 2000]:
        sim_responses = list(run.point_load(config=config, indices=[index], response_type=ResponseType.YTrans))[0]
        xs = config.bridge.wheel_track_xs(config)
        zs = config.bridge.wheel_track_zs(config)
        x = xs[index % len(xs)]
        max_r, max_point = 1, None
        for response, point in sim_responses.values(point=True):
            if response < max_r:
                max_r = response
                max_point = point
        assert max_point[0] == x
        assert max_point[2] == zs[index // len(xs)]

