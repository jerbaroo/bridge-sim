"""
Generate an influence line from a configuration.
"""
import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from config import Config
from model import Load
from models import bridge_705_config
from plot import plot_bridge
from run_opensees_model import run_opensees_model


def gen_il_matrix(c: Config):
    """Generate a stress response matrix for each sensor/load position."""
    matrix = np.empty(shape=(c.il_num_loads, c.num_elems()))
    for i, load_position in enumerate(np.linspace(0, 1, c.il_num_loads)):
        build_opensees_model(c, loads=[Load(load_position, c.il_unit_load)])
        _x, _y, stress, _strain = run_opensees_model(c)
        matrix[i] = stress[0][c.il_save_time]
    np.save(c.il_mat_path(), matrix)
    plt.imshow(matrix)
    plt.ylabel("load position")
    plt.xlabel("sensor position")
    plt.show()


def plot_ils(c: Config, at=None):
    """Plot each influence line from the matrix.

    Args:
        at: int, position index to plot influence line at.
    """
    il_indices = range(len(c.il_matrix())) if at is None else [at]
    for i in il_indices:
        plt.plot(c.bridge.x_axis(len(c.il_matrix()[i])), c.il_matrix()[i])
        plot_bridge(c.bridge)
        plt.show()


def il_response(c: Config, response_pos, load_pos, load):
    """The response of a load at a position from an influence line matrix.

    Args:
        response_pos: position of the returned response, in [0 1].
        load_pos: position of the load, in [0 1].
        load: the value of the load.
    """
    # Convert load_pos to a matrix index.
    load_ind = int(np.interp(load_pos, [0, 1], [0, len(c.il_matrix()) - 1]))
    # Convert response_pos to a matrix index.
    response_ind = int(np.interp(
        response_pos, [0, 1], [0, len(c.il_matrix()[0]) - 1]))
    # Return the matrix value times the load factor.
    return c.il_matrix()[load_ind, response_ind] * (load / c.il_unit_load)


if __name__ == "__main__":
    gen_il_matrix(bridge_705_config)
    il_response(bridge_705_config, 0.5, 0.6, -5e6)
    plot_ils(bridge_705_config, at=4)
