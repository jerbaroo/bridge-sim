"""Load and save influence line matrices."""
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

        # Determine simulation parameters.
        # If save_all is true pass all response types.
        response_types=(
            [rt for rt in ResponseType] if save_all else [response_type])
        expt_params = ExptParams([
            FEMParams(
                loads=[Load(x_frac, c.il_unit_load_kn)],
                response_types=response_types)
            for x_frac in np.linspace(0, 1, num_loads)])

        # Calculate ILMatrix, keep a reference and return.
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
        assert 0 <= resp_x_frac and resp_x_frac <= 1
        assert 0 <= load_x_frac and load_x_frac <= 1
        # Determine load index.
        load_ind = int(np.interp(
            load_x_frac, [0, 1], [0, len(self.expt_responses) - 1]))
        # The simulation response * the load factor.
        response = self.expt_responses[load_ind].at(
            x=resp_x_frac, y=y, z=z, t=t)
        return (response.value * (load / self.c.il_unit_load_kn))
