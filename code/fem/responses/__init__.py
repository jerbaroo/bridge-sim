"""Responses of one sensor type for one FEM simulation."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from timeit import default_timer as timer
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from config import Config
from fem.params import ExptParams, FEMParams
from model import Response
from model.bridge import Point
from model.response import ResponseType
from util import print_i, print_w


def fem_responses_path(
        c: Config, fem_params: FEMParams, response_type: ResponseType,
        runner_name: str):
    """Path of the influence line matrix on disk."""
    return (f"{c.fem_responses_path_prefix}-pa-{fem_params.load_str()}"
            + f"-rt-{response_type.name()}-ru-{runner_name}.npy")


class FEMResponses:
    """Responses of one sensor type for one FEM simulation.

    FEMResponses.responses can be indexed as [time][x][y][z], where x, y, z are
    axis ordinates, but it is better to use the .at method to access responses.

    Args:
        fem_params: FEMParams, the parameters of the simulation.
        runner_name: str, the FEMRunner used to run the simulation.
        response_type: ResponseType, the type of sensor responses collected.
        skip_build: bool, reduces time if responses will only be saved.

    TODO: Warn about assumption.
    """
    def __init__(
            self, c: Config, fem_params: FEMParams, runner_name: str,
            response_type: ResponseType, responses: [Response],
            skip_build: bool = False):
        assert isinstance(responses, list)
        assert isinstance(responses[0], Response)

        # Used for de/serialization.
        self._responses = responses

        self.c = c
        self.fem_params = fem_params
        self.runner_name = runner_name
        self.response_type = response_type
        self.num_sensors = len(responses)

        if skip_build:
            return

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

    # def indices(self, x_frac: float = 0, y_frac: float = 0, z_frac: float = 0):
    #     """Return the indices and values of the closest available values.

    #     Return a 6-tuple of (x_ind, x_true, y_ind, y_true, z_ind, z_true) where
    #     the _true values are the closest available values, and the _ind values
    #     are the indices for accessing the resective _true values.

    #     """
    #     x_ind = int(np.interp(x_frac, [0, 1], [0, len(self.xs) - 1]))
    #     x_true = self.xs[x_ind]
    #     y_ind = int(np.interp(y_frac, [0, 1], [0, len(self.ys[x_true]) - 1]))
    #     y_true = self.ys[x_true][y_ind]
    #     z_ind = int(
    #         np.interp(z_frac, [0, 1], [0, len(self.zs[x_true][y_true]) - 1]))
    #     z_true = self.zs[x_true][y_true][y_ind]
    #     return (x_ind, x_true, y_ind, y_true, z_ind, z_true)

    def _x_indices(self, x: float) -> Tuple[int, int]:
        """Indices of the x positions of sensors either side of x.

        TODO: Test this, and switch to numpy.searchsorted.

        """
        for i in range(len(self.xs)):
            if self.xs[i] == x:
                return i, i
            if self.xs[i] > x and i > 0:
                return i - 1, i
        # x_ind_f = np.interp(x_frac, [0, 1], [0, len(self.xs) - 1])
        # x_ind = int(x_ind_f)
        # return (x_ind, x_ind) if x_ind_f == x_ind else (x_ind, x_ind + 1)

    def _y_indices(self, x: float, y: float) -> Tuple[int, int]:
        """Indices of the y positions of sensors either side of y.

        TODO: Test this, and switch to numpy.searchsorted.

        """
        # print(f"x = {x}")
        # print(self.ys[x])
        if len(self.ys[x]) == 1:
            return 0, 0
        for i in range(len(self.ys[x])):
            if self.ys[x][i] == y:
                return i, i
            if self.ys[x][i] > y and i > 0:
                return i - 1, i
        # y_ind_f = np.interp(y_frac, [0, 1], [0, len(self.ys[x]) - 1])
        # y_ind = int(y_ind_f)
        # return (y_ind, y_ind) if y_ind_f == y_ind else (y_ind, y_ind + 1)

    def _z_indices(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """Indices of the z positions of sensors either side of z.

        TODO: Test this, and switch to numpy.searchsorted.

        """
        if len(self.zs[x][y]) == 1:
            return 0, 0
        for i in range(len(self.zs[x][y])):
            if self.zs[x][y][i] == z:
                return i, i
            if self.zs[x][y][i] > z and i > 0:
                return i - 1, i
        # z_ind_f = np.interp(z_frac, [0, 1], [0, len(self.zs[x][y]) - 1])
        # z_ind = int(z_lo_ind_f)
        # return (z_ind, z_ind) if z_ind_f == z_ind else (z_ind, z_ind + 1)

    def at(
            self, x_frac: float = 0, y_frac: float = 1, z_frac: float = 0.5,
            time_index: int = 0):
        """Compute an interpolated response via axis fractions in [0 1]."""
        assert 0 <= x_frac <= 1
        assert 0 <= y_frac <= 1
        assert self.c.bridge.z_min <= z_frac <= self.c.bridge.z_max

        x = self.c.bridge.x(x_frac=x_frac)
        y = self.c.bridge.y(y_frac=y_frac)
        z = self.c.bridge.z(z_frac=z_frac)
        # print_i(f"x_frac, y_frac, z_frac = ({x_frac}, {y_frac}, {z_frac})")
        print_i(f"x, y, z = ({x}, {y}, {z})")

        x_lo_ind, x_hi_ind = self._x_indices(x=x)
        x_lo, x_hi = self.xs[x_lo_ind], self.xs[x_hi_ind]

        y_lo_x_lo_ind, y_hi_x_lo_ind = self._y_indices(x=x_lo, y=y)
        y_lo_x_hi_ind, y_hi_x_hi_ind = self._y_indices(x=x_hi, y=y)
        y_lo_x_lo, y_hi_x_lo = self.ys[x_lo][y_lo_x_lo_ind], self.ys[x_lo][y_hi_x_lo_ind]
        y_lo_x_hi, y_hi_x_hi = self.ys[x_hi][y_lo_x_hi_ind], self.ys[x_hi][y_hi_x_hi_ind]

        z_lo_y_lo_x_lo_ind, z_hi_y_lo_x_lo_ind = self._z_indices(x=x_lo, y=y_lo_x_lo, z=z)
        z_lo_y_lo_x_hi_ind, z_hi_y_lo_x_hi_ind = self._z_indices(x=x_hi, y=y_lo_x_hi, z=z)
        z_lo_y_hi_x_lo_ind, z_hi_y_hi_x_lo_ind = self._z_indices(x=x_lo, y=y_hi_x_lo, z=z)
        z_lo_y_hi_x_hi_ind, z_hi_y_hi_x_hi_ind = self._z_indices(x=x_hi, y=y_hi_x_hi, z=z)
        z_lo_y_lo_x_lo, z_hi_y_lo_x_lo = self.zs[x_lo][y_lo_x_lo][z_lo_y_lo_x_lo_ind], self.zs[x_lo][y_lo_x_lo][z_hi_y_lo_x_lo_ind]
        z_lo_y_lo_x_hi, z_hi_y_lo_x_hi = self.zs[x_hi][y_lo_x_hi][z_lo_y_lo_x_hi_ind], self.zs[x_hi][y_lo_x_hi][z_hi_y_lo_x_hi_ind]
        z_lo_y_hi_x_lo, z_hi_y_hi_x_lo = self.zs[x_lo][y_hi_x_lo][z_lo_y_hi_x_lo_ind], self.zs[x_lo][y_hi_x_lo][z_hi_y_hi_x_lo_ind]
        z_lo_y_hi_x_hi, z_hi_y_hi_x_hi = self.zs[x_hi][y_hi_x_hi][z_lo_y_hi_x_hi_ind], self.zs[x_hi][y_hi_x_hi][z_hi_y_hi_x_hi_ind]

        points = [                                         # z y x
            Point(x=x_lo, y=y_lo_x_lo, z=z_lo_y_lo_x_lo),  # 0 0 0
            Point(x=x_hi, y=y_lo_x_hi, z=z_lo_y_lo_x_hi),  # 0 0 1
            Point(x=x_lo, y=y_hi_x_lo, z=z_lo_y_hi_x_lo),  # 0 1 0
            Point(x=x_hi, y=y_hi_x_hi, z=z_lo_y_hi_x_hi),  # 0 1 1
            Point(x=x_lo, y=y_lo_x_lo, z=z_hi_y_lo_x_lo),  # 1 0 0
            Point(x=x_hi, y=y_lo_x_hi, z=z_hi_y_lo_x_hi),  # 1 0 1
            Point(x=x_lo, y=y_hi_x_lo, z=z_hi_y_hi_x_lo),  # 1 1 0
            Point(x=x_hi, y=y_hi_x_hi, z=z_hi_y_hi_x_hi)   # 1 1 1
        ]
        request = Point(x=x, y=y, z=z)
        distances = [p.distance(request) for p in points]
        [print(p) for p in points]
        print(distances)

    def at_(
            self, x_frac: float = 0, y_frac: float = 0, z_frac: float = 0,
            time_index: int = 0):
        """Compute an interpolated response via axis fractions in [0 1]."""
        assert 0 <= x_frac <= 1
        assert 0 <= y_frac <= 1
        assert 0 <= z_frac <= 1

        # Set the low and high values if an exact index is available.
        x_ind_f = np.interp(x_frac, [0, 1], [0, len(self.xs) - 1])
        x_ind = int(x_ind_f)
        if x_ind_f == x_ind:
            x_lo_ind, x_hi_ind = x_ind, x_ind
            x = self.xs[x_ind]
            x_lo, x_hi = x, x
        # Else set the low and high values separately.
        else:
            x_lo_ind, x_hi_ind = x_ind, x_ind + 1
            x_lo, x_hi = self.xs[x_lo_ind], self.xs[x_hi_ind]
        print_w(
            f"x_frac = {x_frac}\n"
            + f"x_ind_f = {x_ind_f}\n"
            + f"x_ind = {x_ind}\n"
            + f"x_lo, x_hi = {x_lo}, {x_hi}\n")

        # Y index for the low x value.
        y_lo_ind_f = np.interp(y_frac, [0, 1], [0, len(self.ys[x_lo]) - 1])
        y_lo_ind = int(y_lo_ind_f)
        if abs(y_lo_ind_f - y_lo_ind) > abs(y_lo_ind_f - y_lo_ind + 1):
            y_lo_ind += 1

        # Y index for the high x value.
        y_hi_ind_f = np.interp(y_frac, [0, 1], [0, len(self.ys[x_hi]) - 1])
        y_hi_ind = int(y_hi_ind_f)
        if abs(y_hi_ind_f - y_hi_ind) > abs(y_hi_ind_f - y_hi_ind + 1):
            y_hi_ind += 1

        # Low and high y values.
        y_lo, y_hi = self.ys[x_lo][y_lo_ind], self.ys[x_hi][y_lo_ind]
        print_w(
            f"y_frac = {y_frac}\n"
            + f"y_lo_ind_f = {y_lo_ind_f}\n"
            + f"y_lo_ind = {y_lo_ind}\n"
            + f"y_hi_ind_f = {y_hi_ind_f}\n"
            + f"y_hi_ind = {y_hi_ind}\n"
            + f"y_lo, y_hi = {y_lo}, {y_hi}\n")

        # Z index for the low x value.
        z_lo_ind_f = np.interp(
            z_frac, [0, 1], [0, len(self.zs[x_lo][y_lo]) - 1])
        z_lo_ind = int(z_lo_ind_f)
        if abs(z_lo_ind_f - z_lo_ind) > abs(z_lo_ind_f - z_lo_ind + 1):
            z_lo_ind += 1

        # Z index for the high x value.
        z_hi_ind_f = np.interp(
            z_frac, [0, 1], [0, len(self.zs[x_hi][y_hi]) - 1])
        z_hi_ind = int(z_hi_ind_f)
        if abs(z_hi_ind_f - z_hi_ind) > abs(z_hi_ind_f - z_hi_ind + 1):
            z_hi_ind += 1

        # Low and high z values.
        z_lo, z_hi = (
            self.zs[x_lo][y_lo][z_lo_ind], self.zs[x_hi][y_hi][z_lo_ind])
        print_w(
            f"z_frac = {z_frac}\n"
            + f"z_lo_ind_f = {z_lo_ind_f}\n"
            + f"z_lo_ind = {z_lo_ind}\n"
            + f"z_hi_ind_f = {z_hi_ind_f}\n"
            + f"z_hi_ind = {z_hi_ind}\n"
            + f"z_lo, z_hi = {z_lo}, {z_hi}\n")

        x_frac_lo = np.interp(x_lo_ind, [0, len(self.xs) - 1], [0, 1])
        x_frac_hi = np.interp(x_hi_ind, [0, len(self.xs) - 1], [0, 1])
        y_frac_lo = np.interp(y_lo_ind, [0, len(self.ys[x_lo]) - 1], [0, 1])
        y_frac_hi = np.interp(y_hi_ind, [0, len(self.ys[x_hi]) - 1], [0, 1])
        z_frac_lo = np.interp(z_lo_ind, [0, len(self.zs[x_lo][y_lo]) - 1], [0, 1])
        z_frac_hi = np.interp(y_hi_ind, [0, len(self.zs[x_hi][y_hi]) - 1], [0, 1])
        p_lo = Point(x=x_frac_lo, y=y_frac_lo, z=z_frac_lo)
        p_hi = Point(x=x_frac_hi, y=y_frac_hi, z=z_frac_hi)
        p = Point(x=x_frac, y=y_frac, z=z_frac)
        print_w(
            f"p_lo = {p_lo}\n"
            + f"p_hi = {p_hi}\n"
            + f"p = {p}\n")
        response_lo = self.responses[self.times[time_index]][x_lo][y_lo][z_lo]
        response_hi = self.responses[self.times[time_index]][x_hi][y_hi][z_hi]
        print_w(
            f"response_lo = {response_lo}\n"
            + f"response_hi = {response_hi}\n")
        return (
            (response_lo.value * (p.distance(p_lo) / p_lo.distance(p_hi)))
            + (response_hi.value * (p.distance(p_hi) / p_lo.distance(p_hi))))

    def save(self, c: Config):
        path = fem_responses_path(
            c, self.fem_params, self.response_type, self.runner_name)
        with open(path, "wb") as f:
            pickle.dump(self._responses, f)

    # TODO: Remove.
    def plot_x(
            self, y=0, y_ord=None, z=0, z_ord=None, t=0, time=None, show=True):
        """Plot responses along the x axis at some (y, z, t)."""
        data = [self.at(
                    x_ord=x_ord, y=y, y_ord=y_ord, z=z, z_ord=z_ord, t=t).value
                for x_ord in self.xs]
        plt.plot(self.xs, data)
        if show: plt.show()


def load_fem_responses(
        c: Config, fem_params: FEMParams, response_type: ResponseType,
        fem_runner: FEMRunner) -> FEMResponses:
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
    # Run an experiment with a single simulation.
    if not os.path.exists(path):
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
        c=c, fem_params=fem_params, runner_name=fem_runner.name,
        response_type=response_type, responses=responses)
    print_i(f"Built FEMResponses in {timer() - start:.2f}s, ({response_type})")

    return fem_responses


# TODO: Replace by ExptMatrix/Responses.
ExptResponses = List[FEMResponses]


# TODO: Move to fem.responses.expt.
def load_expt_responses(
        c: Config, expt_params: ExptParams, response_type: ResponseType,
        fem_runner: FEMRunner) -> ExptResponses:
    """Load responses of one type for an experiment."""
    results = []
    for i, fem_params in enumerate(expt_params.fem_params):
        results.append(load_fem_responses(
            c, fem_params, response_type, fem_runner))
        print_i(f"Loading FEMResponses {i + 1}/{len(expt_params.fem_params)}")
    return results
