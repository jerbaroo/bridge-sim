"""Run FEM simulations of bridge 705 with Diana."""
from config import Config
from fem.params import ExptParams, SimParams
from fem.run import FEMRunner
from fem.run.diana.build import build_models
from fem.run.diana.convert import convert_responses
from fem.run.diana.run import run_model
from fem.run.diana.parse import parse_responses
from model.load import PointLoad
from model.bridge.bridge_705 import bridge_705_config


def di_runner(c: Config):
    return FEMRunner(
        c, "Diana", build_models, run_model, parse_responses,
        convert_responses)


if __name__ == "__main__":
    c = bridge_705_config
    response_type = ResponseType.XTranslation
    expt_params = ExptParams([
        SimParams(
            [PointLoad(0, 87375)],
            [response_type]),
        SimParams(
            [PointLoad(0.1, 87375)],
            [response_type]),
        SimParams(
            [PointLoad(0.2, 87375)],
            [response_type])
    ])
    di_runner(c).run(expt_params)
