"""
Generate a range of normal sensor responses.
"""
import matplotlib.pyplot as plt
import numpy as np

from config import Config
from influence_line import il_response
from normal_load import kde_sampler
from models import bridge_705_config


def from_static_load(c: Config, response_pos, print_=True):
    """Yield responses from static load at random positions for one sensor.

    Args:
        response_pos: float, position on the beam in [0 1].
    """
    sampler = kde_sampler(c.a16_data()["total_weight"], print_=print_)
    while True:
        yield il_response(
            c, response_pos, np.random.uniform(), next(sampler))


if __name__ == "__main__":
    gen = from_static_load(bridge_705_config, 0.3)
    responses = [next(gen) for _ in range(10000)]
    plt.hist(responses)
    plt.show()
