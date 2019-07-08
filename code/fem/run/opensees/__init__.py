"""Run FEM simulations with OpenSees."""
from config import bridge_705_config
from fem.params import FEMParams
from fem.responses import load_fem_responses
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.run import convert_responses, parse_responses, run_model
from model import *
from util import *


os_runner = FEMRunner(
    "OpenSees", build_model, run_model, parse_responses, convert_responses)


if __name__ == "__main__":
    c = bridge_705_config
    response_type = ResponseType.YTranslation
    fem_params = FEMParams([Load(0.5, 5e3), Load(0.2, 5e1)])

    # os_runner.run(c, fem_params, response_types=[response_type])
    fem_responses = load_fem_responses(c, fem_params, response_type, os_runner)
    fem_responses.plot_x()
