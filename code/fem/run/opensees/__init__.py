"""Run FEM simulations with OpenSees."""
import os

from config import Config, bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.responses import load_fem_responses
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.convert import convert_responses
from fem.run.opensees.parse import parse_responses
from fem.run.opensees.run import run_model
from model import *


def os_runner(c: Config):
    return FEMRunner(
        "OpenSees", build_model, run_model, parse_responses, convert_responses,
        "tcl", c.generated_dir)


if __name__ == "__main__":
    c = bridge_705_config
    response_type = ResponseType.XTranslation
    expt_params = ExptParams([
        # FEMParams(
        #     [Load(0, 87375)],
        #     [response_type]),
        # FEMParams(
        #     [Load(0.1, 87375)],
        #     [response_type]),
        FEMParams(
            [Load(0.2, 87375)],
            [response_type])
    ])

    os_runner(c).run(c, expt_params, run=False, save=True)
    # fem_responses = load_fem_responses(
    #     c, expt_params.fem_params[0], response_type, os_runner)
    # fem_responses.plot_x()
