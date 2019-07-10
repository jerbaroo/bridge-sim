"""Run FEM simulations of bridge 705 with Diana."""
import subprocess
from collections import defaultdict
from timeit import default_timer as timer
from typing import Dict, List, TypeVar

import numpy as np

from config import Config, bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from model import *
from util import *


def diana_mobile_load(c: Config, expt_params: ExptParams):
    """Diana MOBILE load command for a .dat file."""
    # https://dianafea.com/manuals/d101/Analys/node32.html

    def diana_path():
        return " ".join(
            f"{int(c.di_max_x_elem * f.loads[0].x_pos)} 8200 4165"
            for f in expt_params.fem_params)

    return (
          f"CASE 2"
        + f"\nMOBILE"
        + f"\n     ELEMEN 1-57129"
        + f"\n     DIRECT 3"
        + f"\n     CODE NONE"
        + f"\n     AXFORC -{int(expt_params.fem_params[0].loads[0].weight)}"
        + f"\n     QUADIM 960 900"
        + f"\n     AXWIDT 2300"
        + f"\n     AXDIST 3600 1350 1500"
        + f"\n     PATH 0 8200 4165 20784 8200 4165"
        + f"\n     POSINC 1000")


def build_models(c: Config, expt_params: ExptParams):
    """Build Diana model files.

    All simulations must consist of a single load of the same weight, a single
    simulation will be run using the MOBILE Diana load.

    """
    expt_params.mobile_load = True
    return expt_params
    print_i("Diana: ignoring Config.Bridge")
    with open(c.di_model_template_path) as f:
        in_tcl = f.read()
    # MOBILE Diana load.
    mobile_load = True
    for fem_params in expt_params.fem_params:
        if len(fem_params.loads) != 1:
            mobile_load = False
    if mobile_load:
        for fp1, fp2 in zip(
                expt_params.fem_params[:-1], expt_params.fem_params[1:]):
            if fp1.loads[0].weight != fp2.loads[0].weight:
                mobile_load = False
    expt_params.mobile_load = mobile_load
    if mobile_load:
        out_tcl = in_tcl.replace(
            "<<MOBILE>>", diana_mobile_load(c, expt_params))
        print_i(diana_mobile_load(c, expt_params))
        with open(c.di_model_path, "w") as f:
            f.write(out_tcl)
        return expt_params
    raise ValueError("Only mobile load supported")
    # Individual FEMParams unsupported.
    for fem_params in expt_params.fem_params:
        # out_tcl = in_tcl.replace("<<LOADS>>", diana_loads(c, fem_params.loads))
        with open(fem_params.built_model_file, "w") as f:
            f.write(out_tcl)


def run_model(c: Config, expt_params: ExptParams):
    """Run a Diana simulation."""
    assert expt_params.mobile_load
    out = ".out"
    assert c.di_out_path.endswith(out)
    result = subprocess.run(
        [c.di_exe_path, c.di_model_path, c.di_cmd_path,
         c.di_out_path[:-len(out)], c.di_filos_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        print(result.stdout.decode("utf-8"))
    if result.stderr:
        print(result.stderr.decode("utf-8"))
        with open(c.di_out_path) as f:
            print(f.read())


Parsed = TypeVar("Parsed")


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


def parse_strain(c: Config):
    """Parse strain responses as tuples, indexed by timestep.

    NOTE: timestep starts at 0.

    """
    with open(c.di_strain_path) as f:
        lines = f.readlines()
    time = 0
    elmnr = None
    time_header = True
    data = defaultdict(list)  # Data for each subsequent timestep.
    for line in lines:
        # Need to find beginning of data.
        if time_header:
            if line.strip().startswith("Elmnr"):
                time_header = False
        else:
            nums = line.split()
            # Else parse data (with new element number) if possible.
            if len(nums) == 12:
                line_data = list(map(float, nums))
                data[time].append(line_data)
                elmnr = line_data[0]
            # Else parse data if possible.
            elif len(nums) == 11:
                line_data = [elmnr] + list(map(float, nums))
                data[time].append(line_data)
            # Else beginning of new header.
            else:
                time += 1
                time_header = True
    return data


def parse_responses(c: Config, response_types: [ResponseType]) -> Parsed:
    """Parse responses from a Diana simulation."""
    return None
    results = dict()

    def parse_type(response_type: ResponseType):
        return response_type in response_types or response_types is None

    if (parse_type(ResponseType.XTranslation)
            or parse_type(ResponseType.YTranslation)):
        start = timer()
        parsed_translation = parse_translation(c)
        print_i(f"Diana: Parsed translation responses in {timer() - start:.2f}s")
        results["translation"] = parsed_translation

    if (parse_type(ResponseType.Strain)):
        start = timer()
        parsed_strain = parse_strain(c)
        print_i(f"Diana: Parsed strain responses in {timer() - start:.2f}s")
        results["strain"] = parsed_strain

    return results


def convert_responses(c: Config, parsed: Parsed, response_types: [ResponseType]
                     ) -> Dict[ResponseType, List[Response]]:
    """Convert parsed responses to Responses."""
    results = dict()
    if ResponseType.XTranslation in response_types:
        results[ResponseType.XTranslation] = [
            Response(dx, x=x, y=y, z=z, time=time, node_id=node_id)
            for time in parsed["translation"]
            for node_id, dx, _dy, _dz, x, y, z in parsed["translation"][time]]
    if ResponseType.YTranslation in response_types:
        results[ResponseType.YTranslation] = [
            Response(dy, x=x, y=y, z=z, time=time, node_id=node_id)
            for time in parsed["translation"]
            for node_id, _dx, dy, _dz, x, y, z in parsed["translation"][time]]
    if ResponseType.Strain in response_types:
        results[ResponseType.Strain] = [
            Response(ey, x=x, y=y, z=z, time=time, elem_id=elem_id,
                     srf_id=srf_id, node_id=node_id)
            for time in parsed["strain"]
            for elem_id, srf_id, node_id, _ex, ey, _ez, gx, gy, gz, x, y, z
            in parsed["strain"][time]]
    return results


di_runner = FEMRunner(
    "Diana", build_models, run_model, parse_responses, convert_responses)


if __name__ == "__main__":
    c = bridge_705_config
    response_type = ResponseType.Strain
    fem_params = ExptParams([
        FEMParams(
            [Load(0, 87375)],
            [response_type]),
        FEMParams(
            [Load(0.1, 87375)],
            [response_type])
    ])

    di_runner.run(c, fem_params)
