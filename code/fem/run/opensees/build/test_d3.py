"""Test that OpenSees builds 3D model files correctly."""
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build import build_model
from model.bridge import Dimensions
from model.bridge.bridge_705 import bridge_705_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType


def test_build_d3():
    c = bridge_705_config(dimensions=Dimensions.D3)
    c.os_node_step = 0.5
    expt_params = ExptParams([FEMParams(
        loads=[Load(0.65, 1234)],
        response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    fem_runner = OSRunner(c=c)
    build_model(c=c, expt_params=expt_params, fem_runner=fem_runner)
