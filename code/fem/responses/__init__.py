"""Sensor responses from a FEM simulation."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from config import bridge_705_config
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


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


class NewFEMResponses:
    """Responses of one sensor type for one simulation.

    Indexed as [time][x][y][z], where x, y, z are axis ordinates.

    To index using floats in [0 1] use the .at method.
    """
    def __init__(self, fem_params: FEMParams, runner_name: str,
                 max_time: int, response_type: Response,
                 responses: [_Response]):
        assert isinstance(responses, list)
        assert isinstance(responses[0], _Response)

        # Used for de/serialization.
        self._responses = responses

        self.fem_params = fem_params
        self.runner_name = runner_name
        self.max_time = max_time
        print(f"max_time = {self.max_time}")
        self.response_type = response_type
        self.num_sensors = len(responses)

        # Nested dictionaries for indexing responses by ordinates.
        self.responses = [
            defaultdict(lambda: defaultdict(dict))
            for _ in range(self.max_time + 1)]
        for r in responses:
            self.responses[r.time][r.point.x][r.point.y][r.point.z] = r

        # Convert nested dictionaries to sorted lists at leaves.
        points = self.responses[0]
        self.xs = sorted(list(points.keys()))
        self.ys = {x: sorted(list(points[x].keys())) for x in self.xs}
        self.zs = {x: {y: sorted(list(points[x][y].keys()))
                       for y in self.ys[x]} for x in self.xs}

    def at(self, x=0, x_ord=None, y=0, y_ord=None, z=0, z_ord=None,
           simulation=0, time=0):
        """A FEMResponse indexed using floats in [0 1]."""
        if x_ord is None:
            x_ind = int(np.interp(x, [0, 1], [0, len(self.xs) - 1]))
            x_ord = self.xs[x_ind]
        if y_ord is None:
            y_ind = int(np.interp(y, [0, 1], [0, len(self.ys[x_ord]) - 1]))
            y_ord = self.ys[x_ord][y_ind]
        if z_ord is None:
            z_ind = int(np.interp(z, [0, 1], [0, len(self.zs[x_ord][y_ord]) - 1]))
            z_ord = self.zs[x_ord][y_ord][z_ind]
        # print(f"({x}, {y}, {z}) ({x_ord}, {y_ord}, {z_ord})")
        return self.responses[simulation][time][x_ord][y_ord][z_ord]

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.fem_params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self._responses, f)
        print_i(f"Saved FEM responses to {path}")

    def plot(self, y=0, z=0, time=0):
        """Plot responses along the x-axis for each simulation."""
        print(self.num_simulations)
        matrix = [
            [self.at(x, y=y, z=z, simulation=simulation, time=time).value
             for x in self.xs]
            for simulation in range(self.num_simulations)]
        plt.imshow(matrix, aspect="auto")
        plt.ylabel("load")
        plt.xlabel("sensor")
        plt.show()

    def plot_1(self, y=0, z=0, time=0):
        print(self.xs)
        data = [self.at(x_ord=x, y=y, z=z, time=time).value for x in self.xs]
        plt.plot(data)
        plt.show()


def load_fem_responses(c: Config, fem_params: FEMParams,
                       response_type: Response, runner: FEMRunner):
    print("Running NEWFEMResponses.load")
    path = fem_responses_path(c, fem_params, response_type, runner.name)
    if (not os.path.exists(path)):
        runner.run(c, fem_params)
    with open(path, "rb") as f:
        return NewFEMResponses(
            fem_params, runner.name, response_type, pickle.load(f))
