"""Run FEM simulations with OpenSees."""
import os

from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses import load_fem_responses
from fem.run import FEMRunner, fem_file_path
from fem.run.opensees.build import build_model
from fem.run.opensees.convert import convert_responses
from fem.run.opensees.parse import parse_responses
from fem.run.opensees.run import run_model
from model import *
from model.bridge_705 import bridge_705_config


def os_runner(c: Config):
    """A FEMRunner based on OpenSees."""

    fem_runner = FEMRunner(
        c, "OpenSees", build_model, run_model, parse_responses,
        convert_responses, "tcl")

    def translation_path(fem_params: FEMParams, axis: str):
        return fem_file_path(fem_params, fem_runner, f"node-{axis}.out")

    def patch_path(fem_params: FEMParams, patch: Patch):
        center = patch.center()
        return fem_file_path(
            fem_params, fem_runner,
            f"-patch-{center.y:.5f}-{center.z:.5f}.out")

    def layer_paths(fem_params: FEMParams, layer: Layer):
        return [fem_file_path(
                    fem_params, fem_runner,
                    f"-layer-{point.y:.5f}-{point.z:.5f}.out")
                for point in layer.points()]

    def element_path(fem_params: FEMParams):
        return fem_file_path(fem_params, fem_runner, f"-elems.out")

    fem_runner.x_translation_path = lambda fp: translation_path(fp, "x")
    fem_runner.y_translation_path = lambda fp: translation_path(fp, "y")
    fem_runner.patch_path = patch_path
    fem_runner.layer_paths = layer_paths
    fem_runner.element_path = element_path
    return fem_runner


if __name__ == "__main__":
    c = bridge_705_config()
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
            [ResponseType.XTranslation, response_type])
    ])

    # os_runner(c).run(c, expt_params, run=True, save=True)
    fem_responses = load_fem_responses(
        c, expt_params.fem_params[0], response_type, os_runner(c))
    fem_responses.plot_x()
