"""
Generate data we want to classify as abnormal.
"""
import os
import matplotlib.pyplot as plt

from config import Config
from influence_line import il_response
from model import *
from models import bridge_705_config
from normal_load import kde_sampler


def settlement_response(c: Config, response_pos, loads=[], print_=True):
    """Yield responses at a position from a displacement and a static load.

    Args:
        response_pos: float, position on the beam in [0 1].
    """
    sampler = kde_sampler(c.a16_data()["total_weight"], print_=print_)
    while True:
        sensor_response = 0
        for load in loads:
            sensor_response += il_response(
                c, response_pos, load.x_pos, load.weight)
        yield sensor_response + il_response(
            c, response_pos, np.random.uniform(), -next(sampler))


def plot_settlement_response(c: Config, response_pos, loads=[], print_=True,
                             samples=10000):
    """Plot responses at a position from a displacement and a static load."""
    gen = settlement_response(c, response_pos, loads=loads, print_=print_)
    responses = [next(gen) for _ in range(samples)]
    plt.hist(responses)
    plt.savefig(os.path.join(c.images_dir, "settlement_response"))
    plt.show()


if __name__ == "__main__":
    plot_settlement_response(bridge_705_config, 0.3, loads=[Load(0.5, -5e4)])
