"""Generate an influence line."""
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from config import bridge_705_config, Config
from fem.params import ExptParams, FEMParams
from fem.responses import ExptResponses, load_expt_responses
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *
from plot import *
from util import *


class ILMatrix():
    """Experiment responses used for influence line calculation."""
    def __init__(self, c: Config, response_type: ResponseType,
                 expt_responses: ExptResponses, fem_runner_name: str):
        self.c = c
        self.response_type = response_type
        self.expt_responses = expt_responses
        self.num_loads = len(expt_responses)
        self.fem_runner_name = fem_runner_name

    @staticmethod
    def load(c: Config, response_type: ResponseType, fem_runner: FEMRunner,
             num_loads: int = 12):
        expt_params = ExptParams([
            FEMParams(
                [Load(x_frac, c.il_unit_load_kgs)],
                response_types=[response_type])
            for x_frac in np.linspace(0, 1, num_loads)])
        return ILMatrix(c, response_type, load_expt_responses(
            c, expt_params, response_type, fem_runner), fem_runner.name)

    def response(self, x_frac, load_pos, load, y=0, z=0, t=-1):
        """The response at a position to a load at a position.

        Args:
            x_frac: float, fraction of x-axis response position in [0 1].
            load_pos: float, position of x-axis load position in [0 1].
            load: float, value of the load.

        """
        assert 0 <= x_frac and x_frac <= 1
        # Determine load index.
        load_ind = int(np.interp(
            load_pos, [0, 1], [0, len(self.expt_responses) - 1]))
        # The influence line value * the load factor.
        return (self.expt_responses[load_ind].at(x=x_frac, y=y, z=z, t=t)
                * (load / self.c.unit_load_kgs))

    def plot_ils(self, time:int=0, cols:int=3, save=True, show=True):
        """Plot the influence line for each load position.

        Args:
            time: int, time index of the simulation.
            cols: int, amount of plots in a row.

        """
        rows = self.num_loads / cols
        if rows % 1 != 0:
            rows += 1
        rows = int(rows)
        for load_ind in range(self.num_loads):
            plt.subplot(rows, cols, load_ind + 1)
            self.expt_responses[load_ind].plot_x(show=False)
            plot_bridge_deck_side(c.bridge, show=False)
            name = response_type_name(self.response_type)
            units = response_type_units(self.response_type)
            pos = np.interp(
                load_ind, [0, self.num_loads - 1], [0, self.c.bridge.length])
            plt.ylabel(f"{name} ({units})")
            plt.xlabel("x-axis (m)")
            plt.title(f"Load at {pos:.2f}m")
        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(
                self.c.images_dir,
                f"il-subplots-{self.fem_runner_name}" +
                f"-{len(self.expt_responses)}"))
        if show:
            plt.show()

    def imshow(self, y_frac=0, z_frac=0, t=0, save=True, show=True):
        """Plot a matrix of influence line for each load position."""
        matrix = [
            [fem_responses.at(x_ord=x_ord, y=y_frac, z=z_frac, t=t).value
             for x_ord in fem_responses.xs]
            for fem_responses in self.expt_responses]
        plt.imshow(matrix, aspect="equal")
        plt.colorbar()
        plt.ylabel("load index")
        plt.xlabel("sensor index")
        plt.title(f"{self.fem_runner_name} IL for {len(self.expt_responses)}"
                  + " load positions")
        if save:
            plt.savefig(os.path.join(
                self.c.images_dir,
                f"il-imshow-{self.fem_runner_name}" +
                f"-{len(self.expt_responses)}"))
        if show:
            plt.show()


if __name__ == "__main__":
    c = bridge_705_config()

    # clean_generated(c)
    il_matrix = ILMatrix.load(c, ResponseType.XTranslation, os_runner(c))
    # il_matrix.expt_responses[1].plot_x()
    # il_matrix.imshow()
    il_matrix.plot_ils()
