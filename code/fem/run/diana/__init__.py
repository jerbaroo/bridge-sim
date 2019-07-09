"""Run FEM simulations of bridge 705 with Diana."""
import subprocess
from collections import defaultdict
from timeit import default_timer as timer
from typing import TypeVar

import numpy as np

from config import Config, bridge_705_config
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from model import *
from util import *


def diana_loads(c: Config, loads: [Load]):
    """Diana load commands for a .dat file."""
    # https://dianafea.com/manuals/d101/Analys/node32.html
    return "\n".join(
        ( f"CASE {i + 1}"
        + f"\nMOBILE"
        + f"\n\tELEMEN 1-57219"
        + f"\n\tCODE NONE"
        + f"\n\tAXFORC -{int(l.weight)}"
        + f"\n\tQUADIM 960 900"
        + f"\n\tAXWIDT 2300"
        + f"\n\tAXDIST 3600 1350 1500"
        + f"\n\tPATH 0 8200 4165 {int(c.di_max_x_elem * l.x_pos)} 8200 4165"
        + f"\n\tPOSINC 1000")
        for i, l in enumerate(loads))


def build_model(c: Config, fem_params: FEMParams):
    """Build a Diana model file."""
    return
    print_i("Diana: ignoring Config.Bridge")
    with open(c.di_model_template_path) as f:
        in_tcl = f.read()
    out_tcl = in_tcl.replace("<<LOADS>>", diana_loads(c, fem_params.loads))
    with open(c.di_model_path, "w") as f:
        f.write(out_tcl)


def run_model(c: Config):
    """Run a Diana simulation."""
    return
    out = ".out"
    assert c.di_out_path.endswith(out)
    subprocess.run([c.di_exe_path, c.di_model_path, c.di_cmd_path,
                    c.di_out_path[:-len(out)], c.di_filos_path])


P = TypeVar("P")


def parse_translation(c: Config):
    """Parse translation responses as tuples, indexed by timestep.

    NOTE: timestep starts at 0.

    """
    with open(c.di_translation_path) as f:
        lines = f.readlines()
    time = 0
    time_header = True
    data = defaultdict(list)  # Data for each subsequent timestep.
    for line in lines:
        # Need to find beginning of data.
        if time_header:
            if line.strip().startswith("Nodnr"):
                time_header = False
        else:
            nums = line.split()
            # Else parse data if possible.
            if len(nums) == 7:
                line_data = list(map(float, nums))
                data[time].append(line_data)
            # Else beginning of new header.
            else:
                time += 1
                time_header = True
    return data


def parse_responses(c: Config, response_types: [ResponseType]) -> P:
    """Parse responses from a Diana simulation."""

    def parse_type(response_type: ResponseType):
        return response_type in response_types or response_types is None

    if (parse_type(ResponseType.XTranslation)
            or parse_type(ResponseType.YTranslation)):
        start = timer()
        parsed_translation = parse_translation(c)
        print_i(f"Diana: Parsed translation responses in {timer() - start:.2f}s")
        


di_runner = FEMRunner("Diana", build_model, run_model, parse_responses, None)


if __name__ == "__main__":
    c = bridge_705_config
    response_type = ResponseType.YTranslation
    fem_params = FEMParams([Load(0.5, 5e4), Load(0.2, 5e5)], [response_type])

    di_runner.run(c, fem_params)
    print(str(fem_params))
    n = FEMResponses(0, 0, 0, [
        Response(1, x=1, y=2, z=3),
        Response(2, x=1, y=4, z=3),
        Response(3, x=1, y=1, z=3),
        Response(4, x=1, y=2, z=1),
        Response(5, x=2, y=2, z=3)])
    print(n.at(0.5).value)
