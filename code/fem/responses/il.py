"""Generate an influence line."""
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from config import bridge_705_config, Config
from fem.params import ExptParams, FEMParams
from fem.responses import ExptResponses, FEMResponses, load_fem_responses
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *
from plot import plot_bridge
from util import *


def load_expt_responses(c: Config, expt_params: ExptParams,
                        response_type: ResponseType, runner: FEMRunner):
    """Load responses for an experiment."""
    return [
        load_fem_responses(c, fem_params, response_type, runner)
        for fem_params in expt_params]


class ILMatrix():
    """Experiment responses used for influence line calculation."""
    def __init__(self, c: Config, expt_responses: ExptResponses):
        self.b = c.bridge
        self.unit_load = c.il_unit_load
        self.expt_responses = expt_responses

    @staticmethod
    def load(c: Config, response_type: ResponseType, runner: FEMRunner):
        expt_params = [
            FEMParams([Load(load_pos, c.il_unit_load)])
            for load_pos in np.linspace(0, 1, c.il_num_loads)]
        return ILMatrix(c, load_expt_responses(
            c, expt_params, response_type, runner))

    def response(self, x, load_pos, load, y=0, z=0, t=-1):
        """The response at a position to a load at a position.

        Args:
            x: float, response position on the x-axis, in [0 1].
            load_pos: float, position of the load, in [0 1].
            load: float, value of the load.
        
        """
        # Determine load index.
        load_ind = int(np.interp(
            load_pos, [0, 1], [0, len(self.expt_responses) - 1]))
        # The influence line value * the load factor.
        return (self.expt_responses[load_ind].at(x=x, y=y, z=z, t=t)
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
                 for s in range(self.fem_responses.num_sensors)])
            plot_bridge(c.bridge)
            plt.show()

    def imshow(self, y=0, z=0, t=-1):
        """Imshow the responses along the x-axis for each simulation."""
        matrix = [
            [fem_responses.at(x, y=y, z=z, t=t).value
             for x in fem_responses.xs]
            for fem_responses in self.expt_responses]
        plt.imshow(matrix, aspect="auto")
        plt.ylabel("load")
        plt.xlabel("sensor")
        plt.show()


if __name__ == "__main__":
    c = bridge_705_config
    c.il_num_loads = 10
    response_type = ResponseType.Stress

    # clean_generated(c)
    il_matrix = ILMatrix.load(c, response_type, os_runner)
    il_matrix.expt_responses[0].plot_x()
    # il_matrix.imshow()
    # il_matrix.plot_ils(at=4)
