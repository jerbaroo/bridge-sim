"""
Generate data we want to classify as abnormal.
"""
import os
import matplotlib.pyplot as plt

from config import Config
from influence_line import ILMatrix
from model import *
from models import bridge_705_config
from normal_load import a16_data, kde_sampler


def settlement_response(c: Config, num_loads, response_type: Response,
                        response_pos, loads=[], fiber=0, time=0, print_=True):
    """Yield responses from a displacement and a static load.

    Args:
        response_pos: float, position of the response, in [0 1].
    """
    sampler = kde_sampler(a16_data(c)["total_weight"], print_=print_)
    il_matrix = ILMatrix.load(c, num_loads, response_type)
    while True:
        sensor_response = 0
        for load in loads:
            sensor_response += il_matrix.response(
                response_pos, load.x_pos, load.weight, fiber, time)
        yield sensor_response + il_matrix.response(
            response_pos, np.random.uniform(), -next(sampler), fiber, time)


def plot_settlement_response(c: Config, num_loads, response_type: Response,
                             response_pos, loads=[], fiber=0, time=0,
                             print_=True, samples=10000):
    """Plot responses from a displacement and a static load."""
    gen = settlement_response(c, num_loads, response_type, response_pos,
                              loads=loads, fiber=fiber, time=time,
                              print_=print_)
    responses = [next(gen) for _ in range(samples)]
    plt.hist(responses)
    plt.savefig(os.path.join(c.fig_dir, "settlement_response"))
    plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    num_loads = 10
    response_type = Response.YTranslation

    plot_settlement_response(
        c, num_loads, response_type, 0.3, loads=[Load(0.5, -5e4)])
