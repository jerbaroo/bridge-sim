"""Regression tests for unit load simulations."""

import matplotlib.pyplot as plt

from bridge_sim import plot, sim
from bridge_sim.configs import test_config
from bridge_sim.model import ResponseType, Point, PointLoad, PierSettlement

config, exe_found = test_config()


def test_point_load():
    if not exe_found:
        return
    responses = sim.responses.load(
        config=config,
        response_type=ResponseType.YTrans,
        point_loads=[PointLoad(x=51, z=0, load=100 * 1E3)],
    )
    # plot.contour_responses(config, responses)
    # plt.show()
    response = responses.at_decks([Point(x=50)])[0]
    assert response == -5.593642227074236e-05


def test_pier_settlement():
    if not exe_found:
        return
    responses = sim.responses.load(
        config=config,
        response_type=ResponseType.YTrans,
        pier_settlement=[PierSettlement(0, 1.2)]
    )
    # plot.contour_responses(config, responses)
    # plt.show()
    response = responses.at_decks([Point(x=10, z=-10)])[0]
    assert response == -0.7866629942331611


def test_uniform_thermal():
    if not exe_found:
        return
    responses = sim.responses.load(
        config=config,
        response_type=ResponseType.YTrans,
        temp_deltas=(1, None)
    # To microstrain.
    ).map(lambda r: r * 1E6)
    # plot.contour_responses(config, responses)
    # plt.show()
    response = responses.at_decks([Point(x=10, z=-10)])[0]
    assert response == 6.621297286756995


def test_linear_thermal():
    if not exe_found:
        return
    responses = sim.responses.load(
        config=config,
        response_type=ResponseType.YTrans,
        temp_deltas=(None, 1)
        # To microstrain.
    ).map(lambda r: r * 1E6)
    # plot.contour_responses(config, responses)
    # plt.show()
    response = responses.at_decks([Point(x=10, z=-10)])[0]
    assert response == 59.410866339544526
