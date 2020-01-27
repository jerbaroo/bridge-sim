"""Responses to a load/vehicle across a bridge."""
from __future__ import annotations

import os
import pickle
from collections import defaultdict
from timeit import default_timer as timer
from typing import List, NewType, Optional, Tuple

import numpy as np
from scipy.interpolate import interp1d, interp2d

from config import Config
from fem.params import ExptParams, SimParams
from model.bridge import Bridge, Dimensions, Point
from model.response import Response, ResponseType
from util import nearest_index, print_i, print_w

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
        run: bool, run the simulation even if results are already saved.
        index: Optional[int], simulation progress (n/m) printed if given.

    NOTE: Note-to-self. This function is NOT to take a DamageScenario. The whole
    'fem' module of this package should be separate from that abstraction.

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
        sim_runner=sim_runner, sim_params=sim_params, response_type=response_type,
    )

    # Run an experiment with a single FEM simulation.
    print(path)
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
    sim_responses = SimResponses(
        c=c,
        sim_params=sim_params,
        sim_runner=sim_runner,
        response_type=response_type,
        responses=responses,
    )
    print_prog(f"Built FEMResponses in {timer() - start:.2f}s, ({response_type})")

    return sim_responses


class Responses:
    """Responses of one sensor type for one FE simulation."""

    def __init__(
        self,
        response_type: ResponseType,
        responses: List[Response],
        build: bool = True,
    ):
        assert isinstance(responses, list)
        if len(responses) == 0:
            raise ValueError("No responses found")
        assert isinstance(responses[0][1], Point)
        self.response_type = response_type
        self.raw_responses = responses
        self.num_sensors = len(responses)
        # Nested dictionaries for indexing responses by position.
        self.responses = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        if build:
            for response, p in responses:
                self.responses[0][p.x][p.y][p.z] = response
            self.index()

    def index(self):
        """Create attributes for fast indexing of times and positions."""
        self.times = sorted(self.responses.keys())
        points = self.responses[self.times[0]]
        self.xs = sorted(points.keys())
        self.ys = {x: sorted(points[x].keys()) for x in self.xs}
        self.deck_xs = [x for x in self.xs if 0 in points[x].keys()]
        self.zs = {
            x: {y: sorted(points[x][y].keys()) for y in self.ys[x]} for x in self.xs
        }

    def map(self, f):
        """Map a function over the values of responses."""
        for x, y_dict in self.responses[self.times[0]].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    self.responses[self.times[0]][x][y][z] = f(response)

    def without(self, remove: Callable[[Point], bool]) -> "Responses":
        responses = []
        for x, y_dict in self.responses[self.times[0]].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    p = Point(x=x, y=y, z=z)
                    if not remove(p):
                        responses.append((response, p))
                    # if abs(p.distance(of)) > radius:
        return Responses(response_type=self.response_type, responses=responses)

    def strain_to_real_strain(self, strain_1: float):
        self.map(lambda r: r - strain_1)
        return self

    def deck_strain_to_stress(self, bridge: Bridge, times: float = 1):
        """Convert strains on the deck to stresses."""
        if self.response_type != ResponseType.Strain:
            raise ValueError(f"Responses are not {response_type.Strain}")
        if len(bridge.sections) > 1:
            raise ValueError("Currently only single deck section supported")
        youngs = bridge.sections[0].youngs
        self.map(lambda r: r * youngs * times)
        return self

    def values(self):
        """Yield each response value."""
        for y_dict in self.responses[self.times[0]].values():
            for z_dict in y_dict.values():
                for response in z_dict.values():
                    yield response

    def at_deck(self, point: Point, interp: bool):
        """Response at the deck (y = 0) with optional interpolation."""
        assert point.y == 0
        if not interp:
            print_w("Not interpolating response!")
            return self._at_deck_snap(x=point.x, z=point.z)
        return self._at_deck_interp(x=point.x, z=point.z)

    def _at_deck_interp(self, x: float, z: float):
        x_lo, x_hi = self._lo_hi(a=self.deck_xs, b=x)
        z_lo_x_lo, z_hi_x_lo = self._lo_hi(a=self.zs[x_lo][0], b=z)
        z_lo_x_hi, z_hi_x_hi = self._lo_hi(a=self.zs[x_hi][0], b=z)
        xs = [x_lo, x_lo, x_hi, x_hi]
        zs = [z_lo_x_lo, z_hi_x_lo, z_lo_x_hi, z_hi_x_hi]
        vs = [self.responses[0][xs[i]][0][zs[i]] for i in range(len(xs))]
        # In the case of strain collection in the 3D OpenSees simulation the
        # values collected are not at the nodes but at the integration points.
        # Thus at the perimeter of the bridge no values will be collected and
        # extrapolation is necessary.
        if x_lo == x_hi:
            if z_lo_x_lo == z_hi_x_lo:
                # print("interp1d, x == x, z == z")
                return vs[0]
            # print("interp1d, x == x")
            return interp1d(
                [z_lo_x_lo, z_hi_x_lo], [vs[0], vs[1]], fill_value="extrapolate"
            )(z)
        if z_lo_x_lo == z_hi_x_lo:
            # print("interp1d, z == z")
            return interp1d([x_lo, x_hi], [vs[0], vs[2]], fill_value="extrapolate")(x)
        # z_lo_x_lo, z_hi_x_lo = self._lo_hi(a=self.zs[x_lo][0], b=z)
        # z_lo_x_hi, z_hi_x_hi = self._lo_hi(a=self.zs[x_hi][0], b=z)
        # zs = [z_lo_x_lo, z_hi_x_lo, z_lo_x_hi, z_hi_x_hi]
        # print(x, z)
        # print(xs)
        # print(self.zs[x_lo][0])
        # print(self.zs[x_hi][0])
        # print(zs)
        # print(xs)
        # print(zs)
        # print(vs)
        # print("interp2d")
        return interp2d(x=xs, y=zs, z=vs)(x, z)

    def _lo_hi(self, a: List[float], b: float) -> Tuple[int, int]:
        """Indices of the z positions of sensors either side of z.

        TODO: Assert sorted.
        TODO: Test this.
        TODO: Switch to numpy.searchsorted for performance.

        """
        # print(f"b = {b}")
        # If only one point, return that.
        if len(a) == 1:
            return a[0], a[0]
        # Points are sorted, so find the first equal or greater.
        for i in range(len(a)):
            if np.isclose(a[i], b):
                return a[i], a[i]
            if a[i] > b and i > 0:
                return a[i - 1], a[i]
        # Else the last point.
        return a[i], a[i]

    def _at_deck_snap(self, x: float, z: float):
        """Deck response from nearest available sensor."""
        y = 0
        x_ind = nearest_index(self.xs, x)
        x_near = self.xs[x_ind]
        z_ind = nearest_index(self.zs[x_near][y], z)
        z_near = self.zs[x_near][y][z_ind]
        return self.responses[0][x_near][y][z_near]


class SimResponses(Responses):
    """Responses of one sensor type for one FE simulation."""

    def __init__(
        self,
        c: Config,
        sim_params: SimParams,
        sim_runner: "FEMRunner",
        response_type: ResponseType,
        responses: List[Response],
        build: bool = True,
    ):
        self.c = c
        self.sim_params = sim_params
        self.sim_runner = sim_runner
        super().__init__(response_type=response_type, responses=responses, build=build)

    def save(self):
        """Save theses simulation responses to disk."""
        path = _responses_path(
            sim_runner=self.sim_runner,
            sim_params=self.sim_params,
            response_type=self.response_type,
        )
        with open(path, "wb") as f:
            pickle.dump(self.raw_responses, f)
