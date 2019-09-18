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

    # Build model file.
    expt_params = ExptParams([FEMParams(
        loads=[Load(0.65, 1234)],
        response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    build_model(c=c, expt_params=expt_params, fem_runner=fem_runner)
    with open(fem_runner.fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl")) as f:
        lines = f.readlines()

    # Assert first and last nodes have correct coordinates.
    node_lines = [line for line in lines if "node " in line]
    assert "node 0 0 0 0" in node_lines[0]
    assert "node 1 0.25 0 0" in node_lines[1]
    assert "102.5 0 33.2" in node_lines[-2]
    assert "102.75 0 33.2" in node_lines[-1]

    # Assert section 0 is inserted.
    section_lines = [line for line in lines if "section " in line]
    assert (
        f"section ElasticMembranePlateSection 0 38400 0.2 0.75 0.002724"
        in section_lines[0])
