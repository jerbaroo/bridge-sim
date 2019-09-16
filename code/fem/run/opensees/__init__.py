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
            parse=parse_responses, convert=convert_responses)

    def translation_path(self, fem_params: FEMParams, axis: str):
        return self.fem_file_path(
            fem_params=fem_params, ext="out", append=f"node-{axis}")

    def x_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params=fem_params, axis="x")

    def y_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params=fem_params, axis="y")

    def patch_paths(self, fem_params: FEMParams, patch: Patch):
        return [
            self.fem_file_path(
                fem_params=fem_params, ext="out",
                append=f"-patch-{point.y:.5f}-{point.z:.5f}")
            for point in patch.points()]

    def layer_paths(self, fem_params: FEMParams, layer: Layer):
        return [
            self.fem_file_path(
                fem_params=fem_params, ext="out",
                append=f"-layer-{point.y:.5f}-{point.z:.5f}")
            for point in layer.points()]

    def element_path(self, fem_params: FEMParams):
        return self.fem_file_path(
            fem_params=fem_params, ext="out", append="-elems")
