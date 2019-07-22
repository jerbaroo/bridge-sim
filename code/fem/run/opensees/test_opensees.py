"""Test that OpenSees builds model files correctly."""
from config import bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.run import fem_file_path
from fem.run.opensees import os_runner
from fem.run.opensees.build import build_model
from model import *
from util import *


def test_build():
    # Setup.
    c = bridge_705_config()
    c.bridge.length = 10
    c.os_node_step = 0.5
    c.bridge.fixed_nodes = [Fix(0, x=True), Fix(0.5, y=True), Fix(1, rot=True)]
    expt_params = ExptParams([
        FEMParams(loads=[Load(0.65, 1234)],
                  response_types=[
                      ResponseType.YTranslation, ResponseType.Strain])])

    # Build model file and read.
    fem_runner = os_runner(c)
    build_model(c, expt_params, fem_runner)
    with open(fem_file_path(expt_params.fem_params[0], fem_runner)) as f:
        lines = f.readlines()
    print([line for line in lines if "dof" in line])

    # Check nodes.
    expected_nodes = c.bridge.length / c.os_node_step + 1
    assert expected_nodes == sum(line.startswith("node ") for line in lines)
    assert any(line == "node 21 10.0 0\n" for line in lines)

    # Check fix.
    assert any(line == "fix 1 1 0 0\n" for line in lines)
    assert any(line == "fix 11 0 1 0\n" for line in lines)
    assert any(line == "fix 21 0 0 1\n" for line in lines)

    # Check node recorders.
    assert not any(line.endswith("-dof 1 disp\n") for line in lines)
    assert any(line.endswith("-dof 2 disp\n") for line in lines)


def test_build_displacement_ctrl():
    # Setup.
    c = bridge_705_config()
    c.bridge.length = 10
    c.os_node_step = 0.5
    c.bridge.fixed_nodes = [Fix(0, y=True), Fix(0.5, y=True), Fix(1, y=True)]
    expt_params = ExptParams([
        FEMParams(displacement_ctrl=DisplacementCtrl(0.1, 1),
                  response_types=[
                      ResponseType.YTranslation, ResponseType.Strain])])

    # Build model file and read.
    build_model(c, expt_params, os_runner(c))
    with open(fem_file_path(expt_params.fem_params[0], os_runner(c))) as f:
        lines = f.readlines()

    assert any(line == "load 11 0 10 0\n" for line in lines)
    assert any(line == "test NormDispIncr 1.0e-12 100\n" for line in lines)
    assert any(line == "integrator DisplacementControl 11 2 0.1\n"
               for line in lines)
