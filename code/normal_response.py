"""
Generate a range of normal sensor responses.
"""
import matplotlib.pyplot as plt
import numpy as np

from config import Config
from influence_line import ILMatrix
from normal_load import a16_data, kde_sampler
from model import *
from models import bridge_705_config
from util import *


def to_normal_static_loads_1s_1t(c: Config, num_loads, response_pos,
                                 response_type, fiber=0, time=0, print_=True):
    """Yield responses to normal static loads for one sensor at one time.

    Args:
        num_loads: int, number of simulations to generate the IL.
        response_pos: float, position on the beam in [0 1].
    """
    sampler = kde_sampler(a16_data(c)["total_weight"], print_=print_)
    il_matrix = ILMatrix.load(c, num_loads, response_type)
    while True:
        yield il_matrix.response(
            response_pos, np.random.uniform(), -next(sampler), fiber, time)


def plot_normal_static_loads_1s_1t(c: Config, num_loads, response_pos,
                                   response_type, fiber=0, time=0,
                                   samples=10000, print_=True):
    """Plot responses to normal static loads for one sensor at one time.

    Args:
        num_loads: int, number of simulations to generate the IL.
        response_pos: float, position on the beam in [0 1].
    """
    response_gen = to_normal_static_loads_1s_1t(
        bridge_705_config, num_loads=num_loads, response_pos=response_pos,
        response_type=response_type, fiber=fiber, time=time, print_=print_)
    responses = [next(response_gen) for _ in range(10000)]
    plt.hist(responses)
    plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    num_loads = 4
    response_pos = 0.3
    response_type = Response.YTranslation

    # clean_generated(c)
    plot_normal_static_loads_1s_1t(c, num_loads, response_pos, response_type)
    # il_matrix.plot_ils(at=4)
