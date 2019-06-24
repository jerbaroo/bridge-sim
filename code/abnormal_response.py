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


def load_for_response(c: Config, il_num_loads, response_type: Reponse,
                      response_pos, response, load_pos=None, fiber=0, time=0):
    """The load at a point for a response at a point."""
    if load_pos is None:
        load_pos = response_pos
    il_matrix = ILMatrix.load(c, il_num_loads, response_type)
    response_for_unit_load = il_matrix.response(
        response_pos, load_pos, c.il_unit_load, fiber, time)
    return c.il_unit_load * response / response_for_unit_load


def settlement_response(c: Config, il_num_loads, response_type: Response,
                        response_pos, settlement, fiber=0, time=0, print_=True):
    """Yield responses due to settlement and a sampled static load."""
    sampler = kde_sampler(a16_data(c)["total_weight"], print_=print_)
    il_matrix = ILMatrix.load(c, il_num_loads, response_type)
    while True:
        load_for_settlement = load_for_response(
            c, il_num_loads, response_type, response_pos, Response.YTranslation)
        settlement_response = il_matrix(
            response_pos, response_pos, load_for_settlement, fiber, time)
        sample_response = il_matrix(
            response_pos, np.random.uniform(), -next(sampler), fiber, time)
        yield settlement_response + sample_response


def plot_settlement_response(c: Config, il_num_loads, response_type: Response,
                             response_pos, loads=[], fiber=0, time=0,
                             print_=True, samples=10000):
    """Plot responses from a displacement and a static load."""
    gen = settlement_response(c, il_num_loads, response_type, response_pos,
                              loads=loads, fiber=fiber, time=time,
                              print_=print_)
    responses = [next(gen) for _ in range(samples)]
    plt.hist(responses)
    plt.savefig(os.path.join(c.fig_dir, "settlement_response"))
    plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    il_num_loads = 10
    response_type = Response.YTranslation

    plot_settlement_response(
        c, il_num_loads, response_type, 0.3, loads=[Load(0.5, -5e4)])
