"""
Generate an influence line.
"""
import matplotlib.pyplot as plt
import numpy as np

from config import bridge_705_config, Config
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *
from plot import plot_bridge
from util import *


class ILMatrix():
    """FEM responses used for influence line calculation."""
    def __init__(self, c: Config, response_type: Response, fem_responses:
                 FEMResponses):
        self.b = c.bridge
        self.unit_load = c.il_unit_load
        self.fem_responses = fem_responses

    @staticmethod
    def load(c: Config, response_type: Response, runner: FEMRunner):
        params = FEMParams([[Load(load_pos, c.il_unit_load)]
                           for load_pos in np.linspace(0, 1, c.il_num_loads)])
        return ILMatrix(c, response_type, FEMResponses.load(
            c, params, response_type, runner))

    def response(self, sensor_pos, load_pos, load, fiber=0, time=0):
        """The response at a position, to a load at a position.

        Args:
            sensor_pos: float, position of the response, in [0 1].
            load_pos: float, position of the load, in [0 1].
            load: float, value of the load.
            fiber: int, index of the fiber.
            time: int, time index of the simulation.
        """
        # Determine load and sensor indices.
        load_ind = int(np.interp(
            load_pos, [0, 1], [0, self.fem_responses.num_simulations - 1]))
        sensor_ind = int(np.interp(
            sensor_pos, [0, 1], [0, self.fem_responses.num_sensors - 1]))
        # The influence line value * the load factor.
        return (self.fem_responses.responses[load_ind][fiber, time, sensor_ind]
                * (load / self.unit_load))

    def plot_ils(self, at=None, fiber=0, time=0):
        """Plot each influence line from the matrix.

        Args:
            at: int, position index to plot influence line at.
            fibre: int, index of the fibre.
            time: int, time index of the simulation.
        """
        load_indices = range(self.num_loads) if at is None else [at]
        for l in load_indices:
            plt.plot(
                self.b.x_axis(self.fem_responses.num_sensors),
                [self.fem_responses.responses[l][fiber, time, s]
                 for s in range(self.fem_responses.num_sensors)]
            )
            plot_bridge(c.bridge)
            plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    response_type = Response.Strain

    # clean_generated(c)
    il_matrix = ILMatrix.load(c, response_type, os_runner)
    il_matrix.fem_responses.plot()
    # il_matrix.plot_ils(at=4)
