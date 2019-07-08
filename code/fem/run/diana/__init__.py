"""Run FEM simulations of bridge 705 with Diana."""
import subprocess
from collections import defaultdict

import numpy as np

from config import bridge_705_config, Config
from model import *
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from util import *


def build_model(c: Config, loads=[]):
    """Build a Diana model file."""
    with open(c.di_model_template_path) as f:
        in_tcl = f.read()
    out_tcl = in_tcl.replace("<<LOADS>>")


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
