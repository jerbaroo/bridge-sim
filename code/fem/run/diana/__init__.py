"""Run FEM simulations of bridge 705 with Diana."""
import subprocess

from config import bridge_705_config, Config
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from util import *


def _run_model(c: Config, fem_params: FEMParams):
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
        _run_model(c, fem_params)
        responses[i] = {
            Response.XTranslation: [],
            Response.YTranslation: [],
            Response.Stress: [],
            Response.Strain: []
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
    di_runner.run(c, fem_params)
