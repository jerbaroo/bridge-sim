"""
Parameters and responses of a FEM simulation.
"""
import os
import pickle

import matplotlib.pyplot as plt

from build_opensees_model import build_opensees_model
from models import *
from run_opensees_model import run_opensees_model
from util import *


class FEMParams():
    """Parameters for running FEM simulations.

    NOTE:
      - Currently only static loads.
      - A list of Load per simulation.
    """
    def __init__(self, loads=[[Load]]):
        self.loads=loads


def fem_responses_path(c: Config, num_simulations, response_type: Response):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-ns-{num_simulations}"
            + f"-l-{c.il_unit_load}-r-{response_type.name}.npy")


def gen_fem_responses(c: Config, f: FEMParams):
    """Generate a response matrix for each set of parameters."""
    responses = [0 for _ in range(len(f.loads))]
    for i, loads in enumerate(f.loads):
        build_opensees_model(c, loads=loads)
        responses[i] = run_opensees_model(c)
    for response_type in Response:
        FEMResponses(
            response_type,
            list(map(lambda r: np.array(r[response_type]), responses))
        ).save(c)


class FEMResponses():
    """Indexed as [simulation no.][fiber, time, sensor position].

    For a simulation, the responses of type R in a fiber F at time T.

    NOTE:
      - Time may vary per experiment.
      - Translation is for only one fiber.

    Attrs:
        response_type: Response, type of the response.
        max_time: int, maximum time index of each load position's simulation.
        responses: the matrix as indexed in the class header.
        num_simulations: int, number of simulations with responses.
        num_sensors: int, number of sensors.

    """
    def __init__(self, response_type: Response, responses):
        self.response_type = response_type
        self.max_time = min([r.shape[1] for r in responses])
        self.responses = responses
        self.num_simulations = len(responses)
        self.num_sensors = len(responses[0][0][0])

    @staticmethod
    def load(c: Config, f: FEMParams, response_type: Response):
        path = fem_responses_path(c, len(f.loads), response_type)
        if (not os.path.exists(path)):
            gen_fem_responses(c, f)
        with open(path, "rb") as f:
            return pickle.load(f)

    def save(self, c: Config):
        path = fem_responses_path(c, self.num_simulations, self.response_type)
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
