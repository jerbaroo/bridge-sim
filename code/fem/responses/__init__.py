"""Responses to a load/vehicle across a bridge."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from timeit import default_timer as timer
from typing import List, NewType, Optional, Tuple

from config import Config
from fem.params import ExptParams, SimParams
from model import Response
from model.bridge import Dimensions, Point
from model.response import ResponseType
from util import nearest_index, print_d, print_i

# Print debug information for this file.
D: str = "fem.responses"
# D: bool = False


def _responses_path(
    sim_runner: "FEMRunner", sim_params: SimParams, response_type: ResponseType
) -> str:
    """Path to responses that were generated with given parameters."""
    return sim_runner.sim_out_path(
        sim_params=sim_params, ext="npy", response_types=[response_type]
    )


def load_fem_responses(
    c: Config,
    sim_params: SimParams,
    response_type: ResponseType,
    sim_runner: "FEMRunner",
    run: bool = False,
    index: Optional[Tuple[int, int]] = None,
) -> FEMResponses:
    """Load responses of one sensor type from a FE simulation.

    Responses are loaded from disk, the simulation is only run if necessary

    Args:
        c: Config, global configuration object.
        sim_params: FEMParams, simulation parameters. Note that these decide
            which responses are generated and saved to disk.
        response_type: ResponseType, responses to load from disk and return.
        sim_runner: FEMRunner, FE program to run the simulation with.
        run:
        index: Optional[int], simulation progress (n/m) printed if given.

    """
    if response_type not in sim_params.response_types:
        raise ValueError(f"Can't load {response_type} if not in FEMParams")
    for rt in sim_params.response_types:
        if rt not in sim_runner.supported_response_types(c.bridge):
            raise ValueError(f"{rt} not supported by {sim_runner}")

    prog_str = "1/1: "
    if index is not None:
        prog_str = f"{index[0]}/{index[1]}: "
    print_prog = lambda s: print_i(prog_str + s, end="\r")

    # May need to free a node in y direction.
    if c.bridge.dimensions == Dimensions.D2:
        set_y_false = False
        if sim_params.displacement_ctrl is not None:
            pier = sim_params.displacement_ctrl.pier
            fix = c.bridge.supports[pier]
            if fix.y:
                fix.y = False
                set_y_false = True

    path = _responses_path(
        sim_runner=sim_runner,
        sim_params=sim_params,
        response_type=response_type,
    )

    # Run an experiment with a single FEM simulation.
    if run or not os.path.exists(path):
        print_prog(f"Running simulation")
        sim_runner.run(ExptParams([sim_params]))
    else:
        print_prog(f"Not running simulation")

    # And set the node as fixed again after running.
    if c.bridge.dimensions == Dimensions.D2:
        if set_y_false:
            fix.y = True

    start = timer()
    with open(path, "rb") as f:
        responses = pickle.load(f)
    print_prog(f"Loaded Responses in {timer() - start:.2f}s, ({response_type})")

    start = timer()
    fem_responses = FEMResponses(
        c=c,
        fem_params=sim_params,
        sim_runner=sim_runner,
        response_type=response_type,
        responses=responses,
    )
    print_prog(
        f"Built FEMResponses in {timer() - start:.2f}s, ({response_type})"
    )

    return fem_responses


# A Response is a value at a Point. The response type should be maintained
# separately, for space efficiency reasons as it will be the same for many
# Response.
Respoon = NewType("Respoon", Tuple[float, Point])


class Responses:
    """Responses of one sensor type at many points."""

    def __init__(self, response_type: ResponseType):
        self.response_type = response_type
        # Nested dictionaries for indexing responses by position.
        self.responses = defaultdict(
            lambda: defaultdict(lambda: defaultdict(dict))
        )

    def index(self):
        """Create attributes for fast indexing of times and positions."""
        self.times = sorted(self.responses.keys())
        points = self.responses[self.times[0]]
        self.xs = sorted(points.keys())
        self.ys = {x: sorted(points[x].keys()) for x in self.xs}
        self.zs = {
            x: {y: sorted(points[x][y].keys()) for y in self.ys[x]}
            for x in self.xs
        }

    def values(self):
        """Yield each response value."""
        for y_dict in self.responses[self.times[0]].values():
            for z_dict in y_dict.values():
                for response in z_dict.values():
                    if hasattr(response, "value"):
                        yield response.value
                    return response

    @staticmethod
    def from_responses(response_type: ResponseType, responses: List[Respoon]):
        _responses = Responses(response_type)
        for value, point in responses:
            _responses.responses[0][point.x][point.y][point.z] = value
        _responses.index()
        return _responses


class FEMResponses(Responses):
    """Responses of one sensor type for one FEM simulation.

    FEMResponses.responses can be indexed as [time][x][y][z], where x, y, z are
    axis positions in meters, while the .at method allows accessing responses
    by fractional positions.

    Args:
        fem_params: FEMParams, the parameters of the simulation.
        runner_name: str, the FEMRunner used to run the simulation.
        response_type: ResponseType, the type of sensor responses to collect.
        responses: List[Response], the raw responses from simulation.
        skip_index: bool, reduces time if responses will only be saved.

    TODO: Warn about assumption of equidistant points?

    """

    def __init__(
        self,
        c: Config,
        fem_params: SimParams,
        sim_runner: "FEMRunner",
        response_type: ResponseType,
        responses: List[Response],
        skip_index: bool = False,
    ):
        super().__init__(response_type=response_type)
        assert isinstance(responses, list)
        if len(responses) == 0:
            raise ValueError("No responses found")
        assert isinstance(responses[0], Response)

        # Used for de/serialization.
        self._responses = responses

        self.c = c
        self.fem_params = fem_params
        self.sim_runner = sim_runner
        self.num_sensors = len(responses)

        if not skip_index:
            for r in responses:
                self.responses[r.time][r.point.x][r.point.y][r.point.z] = r
            self.index()

    def save(self):
        """Save theses simulation responses to disk."""
        path = _responses_path(
            sim_runner=self.sim_runner,
            sim_params=self.fem_params,
            response_type=self.response_type,
        )
        with open(path, "wb") as f:
            pickle.dump(self._responses, f)

    def _at(self, x: float, y: float, z: float, time_index: int = 0):
        x_ind = nearest_index(self.xs, x)
        x_near = self.xs[x_ind]
        y_ind = nearest_index(self.ys[x_near], y)
        y_near = self.ys[x_near][y_ind]
        z_ind = nearest_index(self.zs[x_near][y_near], z)
        z_near = self.zs[x_near][y_near][z_ind]
        return self.responses[time_index][x_near][y_near][z_near].value

    def at(
        self,
        x_frac: float = 0,
        y_frac: float = 1,
        z_frac: float = 0.5,
        time_index: int = 0,
        interpolate: bool = False,
    ):
        """Return a response from a sensor at a given position."""
        assert 0 <= x_frac <= 1
        assert 0 <= y_frac <= 1
        assert 0 <= z_frac <= 1

        x = self.c.bridge.x(x_frac=x_frac)
        y = self.c.bridge.y(y_frac=y_frac)
        z = self.c.bridge.z(z_frac=z_frac)

        if interpolate:
            return self.at_interpolate(x=x, y=y, z=z, time_index=time_index)

        return self._at(x=x, y=y, z=z)

    def at_interpolate(
        self, x: float = 0, y: float = 1, z: float = 0.5, time_index: int = 0
    ):
        """Compute an interpolated response via axis fractions in [0 1].

        Interpolate the response between the 8 closest points of a cuboid.

        """
        print_d(D, f"Interpolating")

        x_lo_ind, x_hi_ind = self._x_indices(x=x)
        x_lo, x_hi = self.xs[x_lo_ind], self.xs[x_hi_ind]

        y_lo_x_lo_ind, y_hi_x_lo_ind = self._y_indices(x=x_lo, y=y)
        y_lo_x_hi_ind, y_hi_x_hi_ind = self._y_indices(x=x_hi, y=y)
        y_lo_x_lo, y_hi_x_lo = (
            self.ys[x_lo][y_lo_x_lo_ind],
            self.ys[x_lo][y_hi_x_lo_ind],
        )
        y_lo_x_hi, y_hi_x_hi = (
            self.ys[x_hi][y_lo_x_hi_ind],
            self.ys[x_hi][y_hi_x_hi_ind],
        )

        z_lo_y_lo_x_lo_ind, z_hi_y_lo_x_lo_ind = self._z_indices(
            x=x_lo, y=y_lo_x_lo, z=z
        )
        z_lo_y_lo_x_hi_ind, z_hi_y_lo_x_hi_ind = self._z_indices(
            x=x_hi, y=y_lo_x_hi, z=z
        )
        z_lo_y_hi_x_lo_ind, z_hi_y_hi_x_lo_ind = self._z_indices(
            x=x_lo, y=y_hi_x_lo, z=z
        )
        z_lo_y_hi_x_hi_ind, z_hi_y_hi_x_hi_ind = self._z_indices(
            x=x_hi, y=y_hi_x_hi, z=z
        )
        z_lo_y_lo_x_lo, z_hi_y_lo_x_lo = (
            self.zs[x_lo][y_lo_x_lo][z_lo_y_lo_x_lo_ind],
            self.zs[x_lo][y_lo_x_lo][z_hi_y_lo_x_lo_ind],
        )
        z_lo_y_lo_x_hi, z_hi_y_lo_x_hi = (
            self.zs[x_hi][y_lo_x_hi][z_lo_y_lo_x_hi_ind],
            self.zs[x_hi][y_lo_x_hi][z_hi_y_lo_x_hi_ind],
        )
        z_lo_y_hi_x_lo, z_hi_y_hi_x_lo = (
            self.zs[x_lo][y_hi_x_lo][z_lo_y_hi_x_lo_ind],
            self.zs[x_lo][y_hi_x_lo][z_hi_y_hi_x_lo_ind],
        )
        z_lo_y_hi_x_hi, z_hi_y_hi_x_hi = (
            self.zs[x_hi][y_hi_x_hi][z_lo_y_hi_x_hi_ind],
            self.zs[x_hi][y_hi_x_hi][z_hi_y_hi_x_hi_ind],
        )

        points = [  # z y x
            Point(x=x_lo, y=y_lo_x_lo, z=z_lo_y_lo_x_lo),  # 0 0 0
            Point(x=x_hi, y=y_lo_x_hi, z=z_lo_y_lo_x_hi),  # 0 0 1
            Point(x=x_lo, y=y_hi_x_lo, z=z_lo_y_hi_x_lo),  # 0 1 0
            Point(x=x_hi, y=y_hi_x_hi, z=z_lo_y_hi_x_hi),  # 0 1 1
            Point(x=x_lo, y=y_lo_x_lo, z=z_hi_y_lo_x_lo),  # 1 0 0
            Point(x=x_hi, y=y_lo_x_hi, z=z_hi_y_lo_x_hi),  # 1 0 1
            Point(x=x_lo, y=y_hi_x_lo, z=z_hi_y_hi_x_lo),  # 1 1 0
            Point(x=x_hi, y=y_hi_x_hi, z=z_hi_y_hi_x_hi),
        ]  # 1 1 1
        [print(D, f"point = {point}") for point in points]
        request = Point(x=x, y=y, z=z)
        print(D, f"request = {request}")
        distances = [point.distance(request) for point in points]
        print(D, f"distances = {distances}")
        sum_distances = sum(distances)
        if sum_distances == 0:
            p = points[0]
            return self.responses[time_index][p.x][p.y][p.z].value
        print(D, f"sum distances = {sum_distances}")
        responses = [
            self.responses[time_index][point.x][point.y][point.z].value
            for point in points
        ]
        print(D, f"responses = {responses}")
        response = sum(
            [
                response * (distance / sum_distances)
                for response, distance in zip(responses, distances)
            ]
        )
        print(D, f"response = {response}")
        return response

    def _x_indices(self, x: float) -> Tuple[int, int]:
        """Indices of the x positions of sensors either side of x."""
        # If only one point, return that.
        if len(self.xs) == 1:
            return 0, 0
        # Points are sorted, so find the first equal or greater.
        for i in range(len(self.xs)):
            if self.xs[i] == x:
                return i, i
            if self.xs[i] > x and i > 0:
                return i - 1, i
        # Else the last point.
        return i, i

    def _y_indices(self, x: float, y: float) -> Tuple[int, int]:
        """Indices of the y positions of sensors either side of y."""
        print(D, self.ys[x])
        print(D, f"x = {x}, y = {y}")
        # If only one point, return that.
        if len(self.ys[x]) == 1:
            return 0, 0
        # Points are sorted, so find the first equal or greater.
        for i in range(len(self.ys[x])):
            if self.ys[x][i] == y:
                return i, i
            if self.ys[x][i] > y and i > 0:
                return i - 1, i
        # Else the last point.
        return i, i

    def _z_indices(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """Indices of the z positions of sensors either side of z.

        TODO: Test this.
        TODO: Switch to numpy.searchsorted for performance.
        TODO: Factor out into a method re-usable for x, y, z.

        """
        # If only one point, return that.
        if len(self.zs[x][y]) == 1:
            return 0, 0
        # Points are sorted, so find the first equal or greater.
        for i in range(len(self.zs[x][y])):
            if self.zs[x][y][i] == z:
                return i, i
            if self.zs[x][y][i] > z and i > 0:
                return i - 1, i
        # Else the last point.
        return i, i
