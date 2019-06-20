"""
Generate an influence line.
"""
import pickle

import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from config import Config
from model import *
from models import bridge_705_config
from plot import plot_bridge
from run_opensees_model import run_opensees_model
from util import *


def il_matrix_path(c: Config, num_loads, response_type):
    """Path of the influence line matrix on disk."""
    return (f"{c.il_mat_path_prefix}-nl-{num_loads}"
            + f"-l-{c.il_unit_load}-r-{response_type.name}.npy")


def gen_il_matrix(c: Config, num_loads):
    """Generate a response matrix for each sensor/load position."""
    responses = [0 for _ in range(num_loads)]
    for i, load_position in enumerate(np.linspace(0, 1, num_loads)):
        build_opensees_model(c, loads=[Load(load_position, c.il_unit_load)])
        simulation_responses = run_opensees_model(c)
        responses[i] = simulation_responses
    for response_type in Response:
        print_i(response_type)
        ILMatrix(c, response_type,
                 [np.array(responses[i][response_type])
                  for i in range(num_loads)]
        ).save(c)


class ILMatrix():
    """Indexed as [load position, fiber, time, sensor position].

    NOTE: Time may vary per fiber. Translation is for only one fiber.

    Attrs:
        b: Bridge, bridge for plotting.
        response_type: Response, type of the response.
        max_time: int, maximum time index of each load position's simulation.
        responses: the matrix as indexed in the class header.
    """
    def __init__(self, c: Config, response_type: Response, responses):
        self.b = c.bridge
        self.unit_load = c.il_unit_load
        self.response_type = response_type
        self.max_time = min([r.shape[1] for r in responses])
        self.responses = responses
        self.num_loads = len(responses)
        self.num_sensors = len(responses[0][0][0])

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
        load_ind = int(np.interp(load_pos, [0, 1], [0, self.num_loads - 1]))
        sensor_ind = int(np.interp(
            sensor_pos, [0, 1], [0, self.num_sensors - 1]))
        # The influence line value * the load factor.
        return (self.responses[load_ind][fiber, time, sensor_ind]
                * (load / self.unit_load))

    def save(self, c: Config):
        path = il_matrix_path(c, len(self.responses), self.response_type)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        print_i(f"Saved IL matrix to {path}")

    @staticmethod
    def load(c: Config, num_loads, response_type: Response):
        path = il_matrix_path(c, num_loads, response_type)
        if (not os.path.exists(path)):
            gen_il_matrix(c, num_loads)
        with open(path, "rb") as f:
            return pickle.load(f)

    def plot(self, fibre=0, time=0):
        """Plot this influence line matrix.

        Args:
            fibre: int, index of the fibre.
            time: int, time index of the simulation.
        """
        matrix = [
            [self.responses[l][fibre, time, s]
             for s in range(self.num_sensors)]
            for l in range(self.num_loads)
        ]
        plt.imshow(matrix, aspect="auto")
        plt.ylabel("load")
        plt.xlabel("sensor")
        plt.show()

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
    response_type = Response.YTranslation

    clean_generated(c)
    il_matrix = ILMatrix.load(c, num_loads, response_type)
    il_matrix.plot()
    # il_matrix.plot_ils(at=4)
