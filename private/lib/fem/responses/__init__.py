"""Responses to a load/vehicle across a bridge."""
from __future__ import annotations

import os
import dill
from collections import defaultdict
from timeit import default_timer as timer
from typing import Callable, List, NewType, Optional, Tuple, Union

import numpy as np
from scipy.interpolate import griddata, interp1d, interp2d

from lib.config import Config
from lib.fem.model import Shell
from lib.fem.params import ExptParams, SimParams
from lib.model.bridge import Bridge, Dimensions, Point
from lib.model.response import Response, ResponseType
from util import nearest_index, print_i, print_w, resize_units

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
    run: bool = False,
    run_only: bool = False,
    index: Optional[Tuple[int, int]] = None,
) -> FEMResponses:
    """Load responses of one sensor type from a FE simulation.

    Responses are loaded from disk, the simulation is only run if necessary

    NOTE: Running simulations attaches objects to the given 'SimParams'. If
    attribute 'clean_params' of the respective 'SimParams' is 'True' then these
    objects will be removed after running the simulation, this can avoid a
    memory error when running many simulations.

    Args:
        c: Config, global configuration object.
        sim_params: SimParams, simulation parameters. Response types are
            overridden, set to all supported response types.
        response_type: ResponseType, responses to load from disk and return.
        sim_runner: FEMRunner, FE program to run the simulation with.
        run: bool, run the simulation even if results are already saved.
        index: Optional[int], simulation progress (n/m) printed if given.

    NOTE: Note-to-self. This function is NOT to take a DamageScenario. The whole
    'fem' module of this package should be separate from that abstraction.

    """
    original_response_types = set(sim_params.response_types)
    sim_params.response_types = [
        rt
        for rt in sim_params.response_types
        if rt in c.fem_runner.supported_response_types(c.bridge)
    ]
    for rt in original_response_types:
        if rt not in sim_params.response_types:
            # print_w(
            #     f"Removing response type from SimParams: {rt}"
            #     f", not supported by {sim_runner.name} SimRunner"
            # )
            pass
    if response_type not in sim_params.response_types:
        raise ValueError(f"Can't load {response_type} if not in SimParams")

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
        sim_runner=c.fem_runner, sim_params=sim_params, response_type=response_type,
    )

    # Run the FEM simulation, and/or clean build artefacts, if requested.
    if run or not os.path.exists(path):
        print_prog(f"Running simulation")
        c.fem_runner.run(ExptParams([sim_params]))
        if sim_params.clean_build:
            print_i("Cleaning SimParams of build artefacts")
            del sim_params.bridge_shells
            del sim_params.deck_shells
            del sim_params.pier_shells
            del sim_params.bridge_nodes
            del sim_params.deck_nodes
            del sim_params.pier_nodes
    else:
        print_prog(f"Not running simulation")
    # If only running was requested then we are done.
    if run_only:
        return None

    # And set the node as fixed again after running.
    if c.bridge.dimensions == Dimensions.D2:
        if set_y_false:
            fix.y = True

    start = timer()
    try:
        with open(path, "rb") as f:
            responses = dill.load(f)
    except Exception as e:
        print_i(f"\n{str(e)}\nremoving and re-running sim. {index} at {path}")
        os.remove(path)
        return load_fem_responses(
            c=c,
            sim_params=sim_params,
            response_type=response_type,
            run=run,
            run_only=run_only,
            index=index,
        )

    print_prog(f"Loaded Responses in {timer() - start:.2f}s, ({response_type})")

    start = timer()
    sim_responses = SimResponses(
        c=c,
        sim_params=sim_params,
        sim_runner=c.fem_runner,
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
        units: Optional[str] = None,
    ):
        assert isinstance(responses, list)
        if len(responses) == 0:
            raise ValueError("No responses found")
        assert isinstance(responses[0][1], Point)
        self.response_type = response_type
        self.units = response_type.units() if units is None else units
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

    def deck_points(self) -> List[Point]:
        """All the points on the deck where responses are collected."""
        return [
            Point(x=x, y=0, z=z)
            for _, (x, y, z) in self.values(point=True)
            if np.isclose(y, 0)
        ]

    def add(self, values: List[float], points: List[Point]):
        """Add the values corresponding to given points.

        The points must already be in the responses.

        """
        assert len(values) == len(points)
        for v, p in zip(values, points):
            before = self.responses[0][p.x][p.y][p.z]
            self.responses[0][p.x][p.y][p.z] += v
            after = self.responses[0][p.x][p.y][p.z]
            # print(before, after)
        return self

    def map(self, f, xyz: bool = False):
        """Map a function over the values of responses."""
        time = self.times[0]
        for x, y_dict in self.responses[time].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    if xyz:
                        self.responses[time][x][y][z] = f(response, x, y, z)
                    else:
                        self.responses[time][x][y][z] = f(response)
        return self

    def resize(self):
        """Returns the same responses, possibly resized."""
        responses = self
        resize_f, units = resize_units(self.units)
        if resize_f is not None:
            responses = responses.map(resize_f)
            responses.units = units
        return responses

    def without(self, remove: Callable[[Point], bool]) -> "Responses":
        responses = []
        for x, y_dict in self.responses[self.times[0]].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    p = Point(x=x, y=y, z=z)
                    if not remove(p):
                        responses.append((response, p))
                    # if abs(p.distance(of)) > radius:
        return Responses(
            response_type=self.response_type, responses=responses, units=self.units
        )

    def to_stress(self, bridge: Bridge):
        """Convert strains to stresses."""
        if self.response_type == ResponseType.Strain:
            self.response_type = ResponseType.Stress
        elif self.response_type == ResponseType.StrainT:
            self.response_type = ResponseType.StressT
        elif self.response_type == ResponseType.StrainZZB:
            self.response_type = ResponseType.StressZZB
        else:
            raise ValueError(f"Responses must be strain responses")
        if len(bridge.sections) == 1:
            youngs = bridge.sections[0].youngs
            self.map(lambda r: r * youngs)
        else:

            def _map(r, x, y, z):
                return r * bridge.deck_section_at(x=x, z=z).youngs

            self.map(_map, xyz=True)
        self.units = self.response_type.units()
        return self

    def values(self, point: bool = False):
        """Yield each response value."""
        time = self.times[0]
        for x, y_dict in self.responses[time].items():
            for y, z_dict in y_dict.items():
                for z, response in z_dict.items():
                    if point:
                        yield response, (x, y, z)
                    else:
                        yield response

    def at_shells(self, shells: List["Shell"]) -> Responses:
        responses = []
        for shell in shells:
            shell_center = shell.center()
            if shell_center.y != 0:
                raise ValueError("Can only get response on deck")
            responses.append((self.at_deck(shell_center, interp=False), shell_center))
        return Responses(response_type=self.response_type, responses=responses,)

    def at_deck(self, point: Point, interp: bool, grid_interp: bool = True):
        """Response at the deck (y = 0) with optional interpolation.

        NOTE: Interpolation cannot exptrapolate to points outside known data.

        """
        assert point.y == 0
        if not interp:
            return self._at_deck_snap(x=point.x, z=point.z)
        return self._at_deck_interp(x=point.x, z=point.z, grid_interp=grid_interp)

    def at_decks(self, points: List[Point]) -> List[float]:
        """Like 'at_deck' with grid interpolation, but more efficient for many points.

        NOTE: Interpolation cannot exptrapolate to points outside known data.

        """
        self._at_deck_interp(0, 0)  # Ensure the grid of points is calculated.
        xzs = np.array([[point.x, point.z] for point in points])
        points, values = self.griddata
        return griddata(points, values, xzs)
        # result = self.grid_interp2d(xzs[0].flatten(), xzs[1].flatten())[0]
        # return result

    def _at_deck_interp(self, x: float, z: float, grid_interp=True):
        # Assign to new variables, so they are not overwritten in loop.
        _x, _z = x, z
        # Determine grid of point and values for interpolation.
        if not hasattr(self, "griddata"):
            points = []
            values = []
            # For each x on the deck..
            for x in self.deck_xs:
                # for each z, for that x, determine value.
                for z in self.zs[x][0]:
                    points.append([x, z])
                    values.append(self.responses[0][x][0][z])
            self.griddata = np.array(points), np.array(values)
            # points = self.griddata[0].T
            # self.grid_interp2d = interp2d(points[0], points[1], values)
        # If grid interpolation selected then perform it.
        if grid_interp:
            points, values = self.griddata
            result = griddata(points, values, [[_x, _z]])[0]
            # result = self.grid_interp2d([_x], [_z])[0]
            # print(f"x = {_x}, z = {_z}, result = {result}")
            return result
        # Else (old method), needs update.
        assert False
        # _x, _z = x, z

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
        if np.isclose(x_lo, x_hi):
            if np.isclose(z_lo_x_lo, z_hi_x_lo):
                # print("interp1d, x == x, z == z")
                return vs[0]
            # print("interp1d, x == x")
            return interp1d(
                [z_lo_x_lo, z_hi_x_lo], [vs[0], vs[1]], fill_value="extrapolate"
            )(z)
        if np.isclose(z_lo_x_lo, z_hi_x_lo):
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
        x_ind = nearest_index(self.deck_xs, x)
        x_near = self.deck_xs[x_ind]
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
        try:
            print("About to save raw responses")
            with open(path, "wb") as f:
                dill.dump(self.raw_responses, f)
        except:
            print("Could not save raw responses", flush=True)
