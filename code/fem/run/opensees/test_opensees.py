"""Test that OpenSees builds model files correctly."""
from config import Config, bridge_705_config
from fem.params import ExptParams, FEMParams
from fem.run import fem_file_path
from fem.run.opensees import os_runner
from fem.run.opensees.build import build_model
from model import *


def test_build():
    # Config.
    c = bridge_705_config()
    c.bridge.length = 10
    c.os_node_step = 0.5
    c.bridge.fixed_nodes = [Fix(0, x=True), Fix(0.5, y=True), Fix(1, rot=True)]
    expt_params = ExptParams([
        FEMParams([Load(0.65, 1234)], [ResponseType.XTranslation])
    ])

    # Run and read.
    fem_runner = os_runner(c)
    build_model(c, expt_params, fem_runner)
    with open(fem_file_path(expt_params.fem_params[0], fem_runner)) as f:
        lines = f.readlines()

    # Nodes.
    expected_nodes = c.bridge.length / c.os_node_step + 1
    assert expected_nodes == sum(line.startswith("node ") for line in lines)
    assert any(line == "node 21 10.0 0\n" for line in lines)

    # Fix
    assert any(line == "fix 1 1 0 0\n" for line in lines)
    assert any(line == "fix 11 0 1 0\n" for line in lines)
    assert any(line == "fix 21 0 0 1\n" for line in lines)
