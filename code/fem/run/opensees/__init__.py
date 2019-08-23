"""Run FEM simulations with OpenSees."""
from config import Config
from fem.params import FEMParams
from fem.run import FEMRunner, fem_file_path
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
        return fem_file_path(fem_params, self, f"node-{axis}.out")

    def x_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params, "x")

    def y_translation_path(self, fem_params: FEMParams):
        return self.translation_path(fem_params, "y")

    def patch_path(self, fem_params: FEMParams, patch: Patch):
        center = patch.center()
        return fem_file_path(
            fem_params, self, f"-patch-{center.y:.5f}-{center.z:.5f}.out")

    def layer_paths(self, fem_params: FEMParams, layer: Layer):
        return [
            fem_file_path(
                fem_params, self, f"-layer-{point.y:.5f}-{point.z:.5f}.out")
            for point in layer.points()]

    def element_path(self, fem_params: FEMParams):
        return fem_file_path(fem_params, self, f"-elems.out")


def os_runner(c: Config) -> OSRunner:
    """TODO: Remove, for backwards compatibility."""
    return OSRunner(c)


if __name__ == "__main__":
    from fem.params import ExptParams
    from fem.responses import load_fem_responses
    from model.bridge.bridge_705 import bridge_705_config
    from model.load import Load
    from model.response import ResponseType

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
            response_types=[ResponseType.XTranslation, response_type])
    ])

    # os_runner(c).run(c, expt_params, run=True, save=True)
    fem_responses = load_fem_responses(
        c, expt_params.fem_params[0], response_type, os_runner(c))
    fem_responses.plot_x()
