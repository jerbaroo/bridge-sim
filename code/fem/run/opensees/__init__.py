"""Run FEM simulations with OpenSees."""
import os

from config import Config, bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.responses import load_fem_responses
from fem.run import FEMRunner, fem_file_path
from fem.run.opensees.build import build_model
from fem.run.opensees.convert import convert_responses
from fem.run.opensees.parse import parse_responses
from fem.run.opensees.run import run_model
from model import *


def os_runner(c: Config):
    """A FEMRunner based on OpenSees."""

    fem_runner = FEMRunner(
        "OpenSees", build_model, run_model, parse_responses, convert_responses,
        "tcl", c.generated_dir)

    def translation_path(fem_params: FEMParams, axis: str):
        return os.path.splitext(
            fem_file_path(fem_params, fem_runner))[0] + f"node-{axis}.out"

    def patch_path(fem_params: FEMParams, patch: Patch):
        return (os.path.splitext(fem_file_path(fem_params, fem_runner))[0]
                + f"patch-{patch.fiber_cmd_id}.out")

    def layer_paths(fem_params: FEMParams, layer: Layer):
        return [os.path.splitext(fem_file_path(fem_params, fem_runner))[0]
                + f"{layer.fiber_cmd_id}-{point.y:.5f}-{point.z:.5f}.out"
                for point in layer.points()]

    def element_path(fem_params: FEMParams):
        return os.path.splitext(
            fem_file_path(fem_params, fem_runner))[0] + f"elems.out"

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
            [response_type])
    ])

    os_runner(c).run(c, expt_params, run=True, save=True)
    # fem_responses = load_fem_responses(
    #     c, expt_params.fem_params[0], response_type, os_runner)
    # fem_responses.plot_x()
