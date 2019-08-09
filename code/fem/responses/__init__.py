"""Responses of one sensor type for one FEM simulation."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from model.bridge_705 import bridge_705_config
from timeit import default_timer as timer
from typing import Callable, List

import matplotlib.pyplot as plt

from fem.params import ExptParams, FEMParams
from model import *
from util import *


# TODO: Rename to sim_responses_path.
def fem_responses_path(
        c: Config, fem_params: FEMParams, response_type: ResponseType,
        runner_name: str):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{fem_params.load_str()}"
            + f"-rt-{response_type.name()}-ru-{runner_name}.npy")


# TODO: Rename to SimResponses, move to fem.responses.sim.
class FEMResponses:
    """Responses of one sensor type for one FEM simulation.

    FEMResponses.responses can be indexed as [time][x][y][z], where x, y, z are
    axis ordinates, but it is better to use the .at method to access responses.

    Args:
        fem_params: FEMParams, the parameters of the simulation.
        runner_name: str, the FEMRunner used to run the simulation.
        response_type: ResponseType, the type of sensor responses collected.
        skip_build: bool, reduces time if responses will only be saved.

    """
    def __init__(self, fem_params: FEMParams, runner_name: str,
                 response_type: ResponseType, responses: [Response],
                 skip_build=False):
        assert isinstance(responses, list)
        assert isinstance(responses[0], Response)

        # Used for de/serialization.
        self._responses = responses

        self.fem_params = fem_params
        self.runner_name = runner_name
        self.response_type = response_type
        self.num_sensors = len(responses)

        if skip_build: return

        # Nested dictionaries for indexing responses by ordinates.
        self.responses = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict)))
        for r in responses:
            self.responses[r.time][r.point.x][r.point.y][r.point.z] = r

        # Convert nested dictionaries to sorted lists at leaves.
        # This allows for conversion from an index to an ordinate.
        self.times = sorted(self.responses.keys())
        points = self.responses[self.times[0]]
        self.xs = sorted(points.keys())
        self.ys = {x: sorted(points[x].keys()) for x in self.xs}
        self.zs = {x: {y: sorted(points[x][y].keys())
                       for y in self.ys[x]} for x in self.xs}

    def at(self, x=0, x_ord=None, y=0, y_ord=None, z=0, z_ord=None, t=0,
           time=None):
        """Access responses with axis fractions in [0 1] or with ordinates."""
        assert 0 <= x and x <= 1
        assert 0 <= y and y <= 1
        assert 0 <= z and z <= 1
        # print(f"({x}, {y}, {z}) ({x_ord}, {y_ord}, {z_ord}) t={time}")

        # Convert to x ordinate if necessary.
        if x_ord is None:
            x_ind = int(np.interp(x, [0, 1], [0, len(self.xs) - 1]))
            x_ord = self.xs[x_ind]

        # Convert to y ordinate if necessary.
        if y_ord is None:
            y_ind = int(np.interp(y, [0, 1], [0, len(self.ys[x_ord]) - 1]))
            y_ord = self.ys[x_ord][y_ind]

        # Convert to z ordinate if necessary.
        if z_ord is None:
            z_ind = int(
                np.interp(z, [0, 1], [0, len(self.zs[x_ord][y_ord]) - 1]))
            z_ord = self.zs[x_ord][y_ord][z_ind]

        if time is None:
            time = self.times[t]

        return self.responses[time][x_ord][y_ord][z_ord]

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.fem_params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self._responses, f)

    # TODO: Remove.
    def plot_x(self, y=0, y_ord=None, z=0, z_ord=None, t=0, time=None,
               show=True):
        """Plot responses along the x axis at some (y, z, t)."""
        data = [self.at(
                    x_ord=x_ord, y=y, y_ord=y_ord, z=z, z_ord=z_ord, t=t).value
                for x_ord in self.xs]
        plt.plot(self.xs, data)
        if show: plt.show()


# TODO: Make a method of SimResponses.
def load_fem_responses(c: Config, fem_params: FEMParams,
                       response_type: ResponseType, fem_runner: FEMRunner
                      ) -> FEMResponses:
    """Load responses of one type for a simulation.

    The FEMParams determine which responses are saved.

    """
    assert response_type in fem_params.response_types

    # May need to free a node in y direction.
    set_y_false = False
    if fem_params.displacement_ctrl is not None:
        pier = fem_params.displacement_ctrl.pier
        fix = c.bridge.fixed_nodes[pier]
        if fix.y:
            fix.y = False
            set_y_false = True

    path = fem_responses_path(c, fem_params, response_type, fem_runner.name)
    if (not os.path.exists(path)):
        fem_runner.run(ExptParams([fem_params]))

    # And set the node as fixed again after running.
    if set_y_false:
        fix.y = True

    start = timer()
    with open(path, "rb") as f:
        responses = pickle.load(f)
    print_i(f"Loaded Responses in {timer() - start:.2f}s, ({response_type})")

    start = timer()
    fem_responses = FEMResponses(
        fem_params, fem_runner.name, response_type, responses)
    print_i(f"Built FEMResponses in {timer() - start:.2f}s, ({response_type})")

    return fem_responses


# TODO: Replace by ResponsesMatrix.
ExptResponses = List[FEMResponses]


# TODO: Move to fem.responses.expt.
def load_expt_responses(c: Config, expt_params: ExptParams,
                        response_type: ResponseType, fem_runner: FEMRunner
                       ) -> ExptResponses:
    """Load responses of one type for an experiment."""
    results = []
    for i, fem_params in enumerate(expt_params.fem_params):
        results.append(load_fem_responses(
            c, fem_params, response_type, fem_runner))
        print_i(f"Loading FEMResponses {i + 1}/{len(expt_params.fem_params)}")
    return results
