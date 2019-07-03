"""Sensor responses from a FEM simulation."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from typing import Callable

import matplotlib.pyplot as plt

from fem.params import FEMParams
from model import *
from util import *


def fem_responses_path(c: Config, fem_params: FEMParams,
                       response_type: Response, runner_name: str):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{fem_params}"
            + f"-ul-{c.il_unit_load}-rt-{response_type.name}"
            + f"-ru-{runner_name}.npy")


class FEMResponses():
    """Indexed as [simulation][fiber, time, sensor].

    The responses of one sensor type for a number of simulations.

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
        self.num_simulations = len(self.responses)
        try:
            self.max_time = min([r.shape[1] for r in self.responses])
            self.num_sensors = len(self.responses[0][0][0])
        except:
            self.max_time = 0
            self.num_sensors = 0

    @staticmethod
    def load(c: Config, fem_params: FEMParams, response_type: Response,
             runner: FEMRunner):
        path = fem_responses_path(c, fem_params, response_type, runner.name)
        if (not os.path.exists(path)):
            print("Generating new FEMResponses")
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


class _Response:
    """A sensor response collected from a simulation."""
    # TODO: Rename srfnr to srf_id etc.
    def __init__(self, value, x=None, y=None, z=None, time=0, elem_id=None,
                 srfnr=None, node_id=None, section_id=None, fiber_cmd_id=None):
        self.value = value
        self.point = Point(x=x, y=y, z=z)
        self.time = time
        self.elem_id = elem_id
        self.node_id = node_id
        self.srfnr = srfnr
        self.section_id = section_id
        self.fiber_cmd_id = fiber_cmd_id

    def __str__(self):
        # TODO: Append elmnr etc. if not None.
        return (f"{self.value}"
               + f" at ({self.point.x}, {self.point.y}, {self.point.z})"
               + f" t={self.time}"
               + ("" if self.node_id is None else f" node_id={self.node_id}")
               + ("" if self.elem_id is None else f" elem_id={self.elem_id}"))


# class FEMResponse:
#     """A sensor response kept in FEMResponses, saves space."""
#     def __init__(self, response: _Response):
#         self.value = response.value
#         self.elmnr = response.elmnr
#         self.srfnr = response.srfnr
#         self.nodnr = response.nodnr
#         self.fibnr = response.fibnr


class NewFEMResponses:
    """Responses of one sensor type for a number of simulations.

    Indexed as [simulation][time][x][y][z], where x, y, z are ordinates.

    To index using floats in [0 1] use the .at method.

    NOTE:
      - Assumed that all simulations have the same points recorded.

    """
    def __init__(self, fem_params: FEMParams, runner_name: str,
                 response_type: Response, responses: [[_Response]]):
        self.fem_params = fem_params
        self.runner_name = runner_name
        self.response_type = response_type
        # Nested dictionaries for indexing responses by ordinates.
        self.responses = [
            defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for _ in responses]
        # Add responses to nested dictionaries of ordinates.
        for i, sim_responses in enumerate(responses):
            done = False
            for r in sim_responses:
                if not done:
                    print(r.time)
                    print(r.point.x)
                    print(r.point.y)
                    print(r.point.z)
                    done = True
                self.responses[i][r.time][r.point.x][r.point.y][r.point.z] = r
        # Make responses a normal dict so it's serializable.
        def default_to_regular(d):
            if isinstance(d, defaultdict):
                d = {k: default_to_regular(v) for k, v in d.items()}
            return d
        self.responses = [default_to_regular(d) for d in self.responses]
        # Convert nested dictionaries to sorted lists at leaves.
        points = self.responses[0][0]
        self.xs = sorted(list(points.keys()))
        self.ys = {x: sorted(list(points[x].keys())) for x in self.xs}
        self.zs = {x: {y: sorted(list(points[x][y].keys()))
                       for y in self.ys[x]} for x in self.xs}

    def at(self, x, y=0, z=0, simulation=0, time=0):
        """A FEMResponse indexed using floats in [0 1]."""
        x_ind = int(np.interp(x, [0, 1], [0, len(self.xs) - 1]))
        x_ord = self.xs[x_ind]
        y_ind = int(np.interp(y, [0, 1], [0, len(self.ys[x_ord]) - 1]))
        y_ord = self.ys[x_ord][y_ind]
        z_ind = int(np.interp(z, [0, 1], [0, len(self.zs[x_ord][y_ord]) - 1]))
        z_ord = self.zs[x_ord][y_ord][z_ind]
        # print(f"({x}, {y}, {z}) ({x_ord}, {y_ord}, {z_ord})")
        return self.responses[simulation][time][x_ord][y_ord][z_ord]

    @staticmethod
    def load(c: Config, fem_params: FEMParams, response_type: Response,
             runner: FEMRunner):
        print("Running NEWFEMResponses.load")
        path = fem_responses_path(c, fem_params, response_type, runner.name)
        if (not os.path.exists(path)):
            runner.run(c, fem_params)
        with open(path, "rb") as f:
            return pickle.load(f)

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.fem_params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        print_i(f"Saved FEM responses to {path}")
