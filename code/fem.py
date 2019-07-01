"""
Parameters and responses of a FEM simulation.
"""
import os
import pickle
from typing import Callable

import matplotlib.pyplot as plt

from build_opensees_model import build_opensees_model
from models import *
from run_opensees_model import run_opensees_model
from util import *


class FEMParams():
    """Parameters for FEM simulations.

    NOTE:
      - Currently only static loads.

    Attributes:
        simulations: [[Load]], a list of Load per simulation.
    """
    def __init__(self, simulations: [[Load]]=[]):
        self.simulations=simulations

    def id_str(self):
        return "-".join(
            f"[{lstr}]" for lstr in (
                ",".join(str(l) for l in loads)
                for loads in self.simulations))


class FEMRunner():
    """Run FEM simulations and generate responses."""
    def __init__(self, run: Callable[[Config, FEMParams], None], name: str):
        self.run = run
        self.name = name


def fem_responses_path(c: Config, num_simulations, response_type: Response,
                       runner: FEMRunner):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{num_simulations}"
            + f"-ul-{c.il_unit_load}-rt-{response_type.name}"
            + f"-ru-{runner.name}.npy")


def _os_runner(c: Config, f: FEMParams):
    """Generate a FEMResponses for each FEMParams for each ResponseType."""
    responses = [0 for _ in range(len(f.simulations))]
    for i, loads in enumerate(f.simulations):
        build_opensees_model(c, loads=loads)
        responses[i] = run_opensees_model(c)
    for response_type in Response:
        FEMResponses(
            response_type,
            list(map(lambda r: np.array(r[response_type]), responses))
        ).save(c)


os_runner = FEMRunner(_os_runner, "OpenSees")


class FEMResponses():
    """Indexed as [simulation][fiber, time, sensor].

    THe responses of some sensor type for a number of simulations.

    NOTE:
      - Time may vary per simulation.
      - Translation is for only one fiber.

    Attrs:
        params: FEMParams, used to generate these responses.
        response_type: Response, type of the response.
        max_time: int, maximum time index of each load position's simulation.
        responses: the matrix as indexed in the class header.
        num_simulations: int, number of simulations with responses.
        num_sensors: int, number of sensors.

    """
    def __init__(self, params: FEMParams, response_type: Response, responses):
        self.response_type = response_type
        self.max_time = min([r.shape[1] for r in responses])
        self.responses = responses
        self.num_simulations = len(responses)
        self.num_sensors = len(responses[0][0][0])

    @staticmethod
    def load(c: Config, f: FEMParams, response_type: Response,
             runner: FEMRunner=os_runner):
        path = fem_responses_path(c, f, response_type, runner)
        if (not os.path.exists(path)):
            runner.run(c, f)
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


if __name__ == "__main__":
    fem_params = FEMParams(
        simulations=[[Load(0.5, 5e3), Load(0.2, 5e1)], [Load(0.6, 5e2)]])
    print(fem_params.id_str())
