"""Test that OpenSees builds 2D model files correctly."""
import pytest

from fem.params import ExptParams, SimParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build import build_model_2d
from model.bridge import Fix, Patch, Section
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_test_config
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from util import clean_generated


def test_build_2d():
    return
    # Setup.
    num_sub_div_z = 20
    c = bridge_705_test_config(
        lambda: bridge_705_2d(
            width=2,
            length=10,
            layers=[],
            patches=[
                Patch(
                    y_min=-1,
                    y_max=1,
                    z_min=-1,
                    z_max=1,
                    num_sub_div_z=num_sub_div_z,
                )
            ],
            supports=[Fix(0, x=True), Fix(0.5, y=True), Fix(1, rot=True)],
        )
    )
    c.os_node_step = 0.5
    clean_generated(c)
    expt_params = ExptParams(
        [
            SimParams(
                ploads=[PointLoad(0.65, 0.35, 1234)],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )

    # Build model file and read it into memory.
    build_model_2d(c=c, expt_params=expt_params, os_runner=OSRunner(c))
    with open(
        OSRunner(c).fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl"
        )
    ) as f:
        lines = f.readlines()

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


def test_build_2d_displacement_ctrl():
    return
    # Setup.
    c = bridge_705_test_config(bridge_705_2d)
    c.bridge.length = 10
    c.os_node_step = 0.5
    c.bridge.supports = [Fix(0, y=True), Fix(0.5), Fix(1, y=True)]
    expt_params = ExptParams(
        [
            SimParams(
                displacement_ctrl=DisplacementCtrl(0.1, 1),
                loads=[],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )

    # Build model file and read.
    build_model_2d(c, expt_params, OSRunner(c))
    with open(
        OSRunner(c).fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl"
        )
    ) as f:
        lines = f.readlines()

    assert any(line == "load 11 0 10000 0\n" for line in lines)
    assert any(line == "test NormDispIncr 1.0e-12 100\n" for line in lines)
    assert any(
        line == "integrator DisplacementControl 11 2 0.1\n" for line in lines
    )

    # No error if the displacement control node is not fixed in y direction.
    c.bridge.supports = [Fix(0, y=True), Fix(0.5, y=False), Fix(1, y=True)]
    expt_params = ExptParams(
        [
            SimParams(
                displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1),
                loads=[],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )
    build_model_2d(c=c, expt_params=expt_params, os_runner=OSRunner(c))

    # Error if the displacement control node is fixed in y direction.
    c.bridge.supports = [Fix(0, y=True), Fix(0.5, y=True), Fix(1, y=True)]
    expt_params = ExptParams(
        [
            SimParams(
                displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1),
                loads=[],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )
    with pytest.raises(ValueError):
        build_model_2d(c=c, expt_params=expt_params, os_runner=OSRunner(c))
