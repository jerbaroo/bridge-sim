"""Test that OpenSees builds 3D model files correctly."""
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build import build_model
from model.bridge import Dimensions
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType


def test_build_d3():
    # Setup.
    c = bridge_705_test_config(bridge=bridge_705_3d)
    fem_runner = OSRunner(c=c)

    # Build and model file.
    expt_params = ExptParams([FEMParams(
        loads=[Load(0.65, 1234)],
        response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    build_model(c=c, expt_params=expt_params, fem_runner=fem_runner)
    with open(fem_runner.fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl")) as f:
        lines = f.readlines()
    [print(line) for line in lines]
