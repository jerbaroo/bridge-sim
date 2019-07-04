"""Run FEM simulations with OpenSees."""
from config import Config, bridge_705_config
from fem.params import FEMParams
from fem.responses import load_fem_responses
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.run import run_model
from model import *


def _os_runner(c: Config, fem_params: FEMParams):
    """Generate FEMResponses for given FEMParams."""
    build_model(c, loads=fem_params.loads)
    return run_model(c)


os_runner = FEMRunner(_os_runner, "OpenSees")


if __name__ == "__main__":
    fem_params = FEMParams([Load(0.5, 5e3), Load(0.2, 5e1)])
    os_runner.run(bridge_705_config, fem_params)
    load_fem_responses(
        bridge_705_config, fem_params, 199, Response.Stress, os_runner)
