"""Run FEM simulations with OpenSees."""
from config import Config
from fem.params import FEMParams
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.convert import convert_responses
from fem.run.opensees.parse import parse_responses
from fem.run.opensees.run import run_model
from model.bridge import Layer, Patch


class OSRunner(FEMRunner):
    def __init__(self, c: Config):
        super().__init__(
            c=c, name="OpenSees", build=build_model, run=run_model,
            parse=parse_responses, convert=convert_responses,
            built_model_ext="tcl")

    def translation_path(self, fem_params: FEMParams, axis: str):
        return self.fem_file_path(fem_params, f"node-{axis}.out")

    def x_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params, "x")

    def y_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params, "y")

    def patch_paths(self, fem_params: FEMParams, patch: Patch):
        return [
            self.fem_file_path(
                fem_params, f"-patch-{point.y:.5f}-{point.z:.5f}.out")
            for point in patch.points()]

    def layer_paths(self, fem_params: FEMParams, layer: Layer):
        return [
            self.fem_file_path(
                fem_params, f"-layer-{point.y:.5f}-{point.z:.5f}.out")
            for point in layer.points()]

    def element_path(self, fem_params: FEMParams):
        return self.fem_file_path(fem_params, f"-elems.out")


def os_runner(c: Config) -> OSRunner:
    """TODO: Remove. For backwards compatibility."""
    return OSRunner(c)
