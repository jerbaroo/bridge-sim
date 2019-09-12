"""Test that OpenSees builds model files correctly."""
import pytest

from fem.params import ExptParams, FEMParams
from fem.run.opensees import os_runner
from fem.run.opensees.build import build_model
from model.bridge import Fix, Patch, Section
from model.bridge.bridge_705 import bridge_705_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType


def test_build():
    # Setup.
    num_sub_div_z = 20
    c = bridge_705_config(
        width=2,
        length=10,
        layers=[],
        patches=[Patch(
            y_min=-1, y_max=1, z_min=-1, z_max=1,
            num_sub_div_z=num_sub_div_z)],
        supports=[Fix(0, x=True), Fix(0.5, y=True), Fix(1, rot=True)])
    c.os_node_step = 0.5
    expt_params = ExptParams([FEMParams(
        loads=[Load(0.65, 1234)],
        response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])

    # Build model file and read it into memory.
    fem_runner = os_runner(c)
    build_model(c=c, expt_params=expt_params, fem_runner=fem_runner)
    with open(fem_runner.fem_file_path(expt_params.fem_params[0])) as f:
        lines = f.readlines()
    [print(line) for line in lines]

    # Test nodes.
    expected_nodes = c.bridge.length / c.os_node_step + 1
    assert expected_nodes == sum(line.startswith("node ") for line in lines)
    assert any(line == "node 21 10.0 0\n" for line in lines)

    # Test fixed nodes.
    assert any(line == "fix 1 1 0 0\n" for line in lines)
    assert any(line == "fix 11 0 1 0\n" for line in lines)
    assert any(line == "fix 21 0 0 1\n" for line in lines)

    # Test node recorders.
    # X-translation is not in the FEMParams, y-translation is.
    assert not any(line.endswith("-dof 1 disp\n") for line in lines)
    assert any(line.endswith("-dof 2 disp\n") for line in lines)

    # Test patches.
    patch_lines = [line for line in lines if "patch-" in line]
    assert len(patch_lines) == num_sub_div_z
    assert len(set(patch_lines)) == num_sub_div_z


def test_build_displacement_ctrl():
    # Setup.
    c = bridge_705_config()
    c.bridge.length = 10
    c.os_node_step = 0.5
    c.bridge.fixed_nodes = [Fix(0, y=True), Fix(0.5), Fix(1, y=True)]
    expt_params = ExptParams([
        FEMParams(displacement_ctrl=DisplacementCtrl(0.1, 1),
                  loads=[],
                  response_types=[
                      ResponseType.YTranslation, ResponseType.Strain])])

    # Build model file and read.
    build_model(c, expt_params, os_runner(c))
    with open(os_runner(c).fem_file_path(expt_params.fem_params[0])) as f:
        lines = f.readlines()

    assert any(line == "load 11 0 10000 0\n" for line in lines)
    assert any(line == "test NormDispIncr 1.0e-12 100\n" for line in lines)
    assert any(line == "integrator DisplacementControl 11 2 0.1\n"
               for line in lines)

    # No error if the displacement control node is not fixed in y direction.
    c.bridge.fixed_nodes = [Fix(0, y=True), Fix(0.5, y=False), Fix(1, y=True)]
    expt_params = ExptParams([
        FEMParams(displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1),
                  loads=[],
                  response_types=[
                      ResponseType.YTranslation, ResponseType.Strain])])
    build_model(c=c, expt_params=expt_params, fem_runner=os_runner(c))

    # Error if the displacement control node is fixed in y direction.
    c.bridge.fixed_nodes = [Fix(0, y=True), Fix(0.5, y=True), Fix(1, y=True)]
    expt_params = ExptParams([
        FEMParams(displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1),
                  loads=[],
                  response_types=[
                      ResponseType.YTranslation, ResponseType.Strain])])
    with pytest.raises(ValueError):
        build_model(c=c, expt_params=expt_params, fem_runner=os_runner(c))
