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
                       response_type: ResponseType, runner_name: str):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{fem_params}"
            + f"-ul-{c.il_unit_load}-rt-{response_type.name}"
            + f"-ru-{runner_name}.npy")


class FEMResponses:
    """Responses of one sensor type for one simulation.

    Indexed as [time][x][y][z], where x, y, z are axis ordinates.

    NOTE: Use the .at method to access responses.

    """
    def __init__(self, fem_params: FEMParams, runner_name: str,
                 response_type: ResponseType, responses: [Response]):
        assert isinstance(responses, list)
        assert isinstance(responses[0], Response)

        # Used for de/serialization.
        self._responses = responses

        self.fem_params = fem_params
        self.runner_name = runner_name
        self.response_type = response_type
        self.num_sensors = len(responses)

        # Nested dictionaries for indexing responses by ordinates.
        self.responses = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict)))
        for r in responses:
            self.responses[r.time][r.point.x][r.point.y][r.point.z] = r

        # Convert nested dictionaries to sorted lists at leaves.
        self.times = sorted(self.responses.keys())
        points = self.responses[self.times[0]]
        self.xs = sorted(points.keys())
        self.ys = {x: sorted(points[x].keys()) for x in self.xs}
        self.zs = {x: {y: sorted(points[x][y].keys())
                       for y in self.ys[x]} for x in self.xs}

    def at(self, x=0, x_ord=None, y=0, y_ord=None, z=0, z_ord=None, t=-1,
           time=None):
        """Access simulation responses using indices or directly."""
        if x_ord is None:
            x_ind = int(np.interp(x, [0, 1], [0, len(self.xs) - 1]))
            x_ord = self.xs[x_ind]
        if y_ord is None:
            y_ind = int(np.interp(y, [0, 1], [0, len(self.ys[x_ord]) - 1]))
            y_ord = self.ys[x_ord][y_ind]
        if z_ord is None:
            z_ind = int(
                np.interp(z, [0, 1], [0, len(self.zs[x_ord][y_ord]) - 1]))
            z_ord = self.zs[x_ord][y_ord][z_ind]
        if time is None:
            time = self.times[t]
        # print(f"({x}, {y}, {z}) ({x_ord}, {y_ord}, {z_ord}) t={time}")
        return self.responses[time][x_ord][y_ord][z_ord]

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.fem_params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self._responses, f)
        print_i(f"Saved FEM responses to {path}")

    def plot(self, y=0, z=0, t=-1):
        """Plot responses along the x-axis for each simulation."""
        matrix = [
            [self.at(x, y=y, z=z, t=t).value for x in self.xs]
            for simulation in range(self.num_simulations)]
        plt.imshow(matrix, aspect="auto")
        plt.ylabel("load")
        plt.xlabel("sensor")
        plt.show()


def plot_x(fem_responses, y=0, y_ord=None, z=0, z_ord=None, t=-1, time=None):
    """Plot responses along the x axis at some (y, z, t)."""
    data = [fem_responses.at(
                x_ord=x_ord, y=y, y_ord=y_ord, z=z, z_ord=z_ord, t=t).value
            for x_ord in fem_responses.xs]
    plt.plot(data)
    plt.show()


def load_fem_responses(c: Config, fem_params: FEMParams,
                       response_type: ResponseType, runner: FEMRunner):
    print_i("Loading FEMResponses")
    path = fem_responses_path(c, fem_params, response_type, runner.name)
    if (not os.path.exists(path)):
        runner.run(c, fem_params)
    with open(path, "rb") as f:
        return FEMResponses(
            fem_params, runner.name, response_type, pickle.load(f))
