"""Generate an influence line."""
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

from config import bridge_705_config, Config
from fem.params import ExptParams, FEMParams
from fem.responses import ExptResponses, load_expt_responses
from fem.run import FEMRunner
from fem.run.opensees import os_runner
from model import *
from plot import *
from util import *

def il_matrix_id(c: Config, response_type: ResponseType, fem_runner: FEMRunner,
                 num_loads: int) -> str:
    return f"{c.il_unit_load_kn}-{response_type}-{fem_runner.name}-{num_loads}"


class ILMatrix:
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
             num_loads: int = 12, save_all=True):
        """Load ILMatrix from disk, running simulations if necessary.

        Args:
            response_type: ResponseType, the type of response to load.
            fem_runner: FEMRunner, the program to run simulations with.
            save_all: bool, save all response types when running a simulation.

        """
        # Return ILMatrix if already calculated.
        id_ = il_matrix_id(c, response_type, fem_runner, num_loads)
        if id_ in c.il_matrices:
            return c.il_matrices[id_]

        # Else calculate, keep a reference and return.
        expt_params = ExptParams([
            FEMParams(
                loads=[Load(x_frac, c.il_unit_load_kn)],
                # If save_all is true pass all response types.
                response_types=[rt for rt in ResponseType] if save_all
                               else [response_type])
            for x_frac in np.linspace(0, 1, num_loads)])
        c.il_matrices[id_] = ILMatrix(c, response_type, load_expt_responses(
            c, expt_params, response_type, fem_runner), fem_runner.name)
        return c.il_matrices[id_]

    def response(self, resp_x_frac, load_x_frac, load, y=0, z=0, t=0):
        """The response at a position to a load at a position.

        Point load response.

        Args:
            resp_x_frac: float, fraction of x-axis response position in [0 1].
            load_x_frac: float, fraction of x-axis load position in [0 1].
            load: float, value of the load.

        """
        print(resp_x_frac)
        print(load_x_frac)
        print(load)
        assert 0 <= resp_x_frac and resp_x_frac <= 1
        # Determine load index.
        load_ind = int(np.interp(
            load_x_frac, [0, 1], [0, len(self.expt_responses) - 1]))
        # The simulation response * the load factor.
        response = self.expt_responses[load_ind].at(
            x=resp_x_frac, y=y, z=z, t=t)
        return (response.value * (load / self.c.il_unit_load_kn))

    def plot_ils(self, time:int=0, cols:int=3, save=False, show=False):
        """Plot the influence line for each load position.

        Args:
            time: int, time index of the simulation.
            cols: int, amount of plots in a row.

        """

        class ScalarFormatterForceFormat(ScalarFormatter):
            def _set_format(self):
                self.format = "%1.1f"

        rows = self.num_loads / cols
        if rows % 1 != 0:
            rows += 1
        rows = int(rows)
        for load_ind in range(self.num_loads):
            plt.subplot(rows, cols, load_ind + 1)
            self.expt_responses[load_ind].plot_x(show=False)
            plot_bridge_deck_side(self.c.bridge, show=False)
            name = response_type_name(self.response_type)
            units = response_type_units(self.response_type)
            pos = np.interp(
                load_ind, [0, self.num_loads - 1], [0, self.c.bridge.length])
            plt.ylabel(f"{name} ({units})")
            plt.gca().yaxis.set_major_formatter(ScalarFormatterForceFormat())
            plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
            plt.xlabel("x-axis (m)")
            plt.title(f"{self.c.il_unit_load_kn}kN load at {pos:.2f}m")
        plt.gcf().set_size_inches(16, 10)
        plt.tight_layout()
        if save:
            name = response_type_name(self.response_type)
            plt.savefig(os.path.join(
                self.c.images_dir,
                f"il-subplots-{self.fem_runner_name}-{name}" +
                f"-{len(self.expt_responses)}"))
        if show: plt.show()
        if save or show: plt.close()

    def imshow(self, y_frac=0, z_frac=0, t=0, save=False, show=False):
        """Plot a matrix of influence line for each load position."""
        matrix = [
            [fem_responses.at(x_ord=x_ord, y=y_frac, z=z_frac, t=t).value
             for x_ord in fem_responses.xs]
            for fem_responses in self.expt_responses]
        plt.imshow(matrix, aspect="auto")
        plt.colorbar()
        plt.ylabel("load index")
        plt.xlabel("sensor index")
        name = response_type_name(self.response_type)
        plt.title(f"{self.fem_runner_name} IL for {len(self.expt_responses)}"
                  + " load positions")
        if save:
            plt.savefig(os.path.join(
                self.c.images_dir,
                f"il-imshow-{self.fem_runner_name}-{name}" +
                f"-{len(self.expt_responses)}"))
        if show: plt.show()
        if save or show: plt.close()
