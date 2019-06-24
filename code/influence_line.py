"""
Generate an influence line.
"""
import pickle

import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from config import Config
from fem import FEMResponses, fem_responses_path
from model import *
from models import bridge_705_config
from plot import plot_bridge
from run_opensees_model import run_opensees_model
from util import *


class ILMatrix(FEMResponses):
    """Indexed as [load position][fiber, time, sensor position]."""
    def __init__(self, c: Config, response_type: Response, responses):
        self.b = c.bridge
        self.unit_load = c.il_unit_load
        super().__init__(self, response_type, responses)

    @staticmethod
    def load(c: Config, num_loads, response_type: Response):
        params = [FEMParams(Load(c.unit_load, load_pos))
                  for load_pos in np.linspace(0, 1, num_loads)]
        super(FEMResponses, FEMResponses).load(c, params, response_type)

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
            load_pos, [0, 1], [0, self.num_simulations - 1]))
        sensor_ind = int(np.interp(
            sensor_pos, [0, 1], [0, self.num_sensors - 1]))
        # The influence line value * the load factor.
        return (self.responses[load_ind][fiber, time, sensor_ind]
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
                self.b.x_axis(self.num_sensors),
                [self.responses[l][fiber, time, s]
                 for s in range(self.num_sensors)]
            )
            plot_bridge(c.bridge)
            plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    num_loads = 10
    response_type = Response.Strain

    # clean_generated(c)
    il_matrix = ILMatrix.load(c, num_loads, response_type)
    il_matrix.plot()
    # il_matrix.plot_ils(at=4)
