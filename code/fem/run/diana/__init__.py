"""Run FEM simulations of bridge 705 with Diana."""
import subprocess
from collections import OrderedDict, defaultdict

import numpy as np

from config import bridge_705_config, Config
from model import *
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from util import *


def run_model(c: Config, fem_params: FEMParams):
    """Run a Diana simulation."""
    print_i("TODO Add loads to Diana simulation.")
    out = ".out"
    assert c.di_out_path.endswith(out)
    subprocess.run([c.di_exe_path, c.di_model_path, c.di_cmd_path,
                    c.di_out_path[:-len(out)], c.di_filos_path])


def _di_runner(c: Config, fem_params: FEMParams, runner_name: str):
    """Generate FEMResponses for given FEMParams (for each ResponseType)."""
    responses = [0 for _ in range(len(fem_params.simulations))]
    for i, loads in enumerate(fem_params.simulations):
        print_i(f"Running Diana data file {c.di_model_path}")
        print_i("NOTE: Ignoring Config.Bridge")
        run_model(c, fem_params)
        responses[i] = {
            Response.XTranslation: [[]],
            Response.YTranslation: [[]],
            Response.Stress: [[]],
            Response.Strain: [[]]
        }
    for response_type in Response:
        FEMResponses(
            fem_params,
            runner_name,
            response_type,
            map(lambda r: r[response_type], responses)
        ).save(c)


di_runner = FEMRunner(_di_runner, "Diana")


class _Response:
    """A sensor response collected from a simulation."""
    def __init__(self, value, x=None, y=None, z=None, time=0, elmnr=None,
                 srfnr=None, nodnr=None, fibnr=None):
        self.value = value
        self.point = Point(x=x, y=y, z=z)
        self.time = time
        self.elmnr = elmnr
        self.srfnr = srfnr
        self.nodnr = nodnr
        self.fibnr = fibnr


class FEMResponse:
    """A sensor response kept in FEMResponses, saves space."""
    def __init__(self, response: _Response):
        self.value = response.value
        self.elmnr = response.elmnr
        self.srfnr = response.srfnr
        self.nodnr = response.nodnr
        self.fibnr = response.fibnr


class NewFEMResponses:
    """Responses of one sensor type for a number of simulations.

    Indexed as [simulation][time][x][y][z], where x, y, z are ordinates.

    To index using floats in [0 1] use the .at method.

    NOTE:
      - Assumption that all simulations have same points recorded.
    """
    def __init__(self, fem_params: FEMParams, runner_name: str,
                 response_type: Response, responses: [[_Response]]):
        self.fem_params = fem_params
        self.runner_name = runner_name
        self.response_type = response_type
        # Nested dictionaries for indexing responses.
        self.responses = [
            defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for _ in responses]
        # Add responses to nested dictionaries and position lists.
        for i, sim_responses in enumerate(responses):
            for r in sim_responses:
                self.responses[i][r.time][r.point.x][r.point.y][r.point.z] = (
                    FEMResponse(r))
        # Convert response ordinates to nested dictionaries.
        points = self.responses[0][0]
        self.xs = sorted(list(points.keys()))
        self.ys = {x: sorted(list(points[x].keys())) for x in self.xs}
        self.zs = {x: {y: sorted(list(points[x][y].keys()))
                       for y in self.ys[x]} for x in self.xs}

    def at(self, x, y=0, z=0, simulation=0, time=0):
        """Access a response using floats in [0 1]."""
        x_ind = int(np.interp(x, [0, 1], [0, len(self.xs) - 1]))
        x_ord = self.xs[x_ind]
        y_ind = int(np.interp(y, [0, 1], [0, len(self.ys[x_ord]) - 1]))
        y_ord = self.ys[x_ord][y_ind]
        z_ind = int(np.interp(z, [0, 1], [0, len(self.zs[x_ord][y_ord]) - 1]))
        z_ord = self.zs[x_ord][y_ord][z_ind]
        # print(f"({x}, {y}, {z}) ({x_ord}, {y_ord}, {z_ord})")
        return self.responses[simulation][time][x_ord][y_ord][z_ord]


if __name__ == "__main__":
    from model import *
    c = bridge_705_config
    fem_params = FEMParams(simulations=[[Load(0.6, 5e2)]])
    print(str(fem_params))
    n = NewFEMResponses(0, 0, 0, [[
        _Response(1, x=1, y=2, z=3),
        _Response(2, x=1, y=4, z=3),
        _Response(2, x=1, y=1, z=3),
        _Response(4, x=1, y=2, z=1),
        _Response(5, x=2, y=2, z=3)
    ]])
    print(n.at(0.5).value)
