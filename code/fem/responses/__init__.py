"""
Sensor responses from a FEM simulation.
"""
import os
import pickle
from typing import Callable

import matplotlib.pyplot as plt

from fem.params import FEMParams
from fem.run import FEMRunner
from models import *
from util import *


def fem_responses_path(c: Config, fem_params: FEMParams,
                       response_type: Response, runner_name: str):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{fem_params.id_str()}"
            + f"-ul-{c.il_unit_load}-rt-{response_type.name}"
            + f"-ru-{runner_name}.npy")


class FEMResponses():
    """Indexed as [simulation][fiber, time, sensor].

    THe responses of one sensor type for a number of simulations.

    NOTE:
      - Time may vary per simulation.
      - Translation is for only one fiber.

    Attrs:
        params: FEMParams, used to generate these responses.
        response_type: Response, type of the response.
        responses: the matrix as indexed in the class header.
        max_time: int, maximum time index of each load position's simulation.
        num_simulations: int, number of simulations with responses.
        num_sensors: int, number of sensors.

    """
    def __init__(self, params: FEMParams, runner_name: str,
                 response_type: Response, responses):
        self.params = params
        self.runner_name = runner_name
        self.response_type = response_type
        self.responses = list(map(np.array, responses))
        self.max_time = min([r.shape[1] for r in self.responses])
        self.num_simulations = len(self.responses)
        self.num_sensors = len(self.responses[0][0][0])

    @staticmethod
    def load(c: Config, fem_params: FEMParams, response_type: Response,
             runner: FEMRunner):
        path = fem_responses_path(c, fem_params, response_type, runner.name)
        if (not os.path.exists(path)):
            runner.run(c, fem_params)
        with open(path, "rb") as f:
            return pickle.load(f)

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        print_i(f"Saved FEM responses to {path}")

    def plot(self, fibre=0, time=0):
        """Plot the responses for each sensor for each experiment.

        Args:
            fibre: int, index of the fibre.
            time: int, time index of the simulation.
        """
        matrix = [
            [self.responses[l][fibre, time, s]
             for s in range(self.num_sensors)]
            for l in range(self.num_simulations)
        ]
        plt.imshow(matrix, aspect="auto")
        plt.ylabel("load")
        plt.xlabel("sensor")
        plt.show()
