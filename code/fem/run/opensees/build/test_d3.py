"""Test that OpenSees builds 3D model files correctly."""
from typing import List, Optional

from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.build.d3 import next_node_id, reset_node_ids, ff_node_ids, next_pow_10
from model.bridge import Dimensions
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType


def get_lines(
        contains: str, lines: List[str], after: str = "",
        before: Optional[str] = None):
    """Return lines that contain a string, after and before a string."""
    started = False
    result = []
    for line in lines:
        if not started:
            if after in line:
                started = True
        else:
            if before is not None and before in line:
                return result
            if contains in line:
                result.append(line)
    return result


def test_build_d3_deck_nodes_elems():
    """Test the deck nodes and elements are built correctly."""
    # Setup.
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.os_node_step = c.bridge.length / 10
    c.os_node_step_z = c.bridge.width / 10
    os_runner = OSRunner(c=c)

    # Build model file.
    expt_params = ExptParams([FEMParams(
        loads=[Load(0.65, 1234)], response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    build_model(c=c, expt_params=expt_params, os_runner=os_runner)
    with open(os_runner.fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl")) as f:
        lines = f.readlines()

    # Assert first and last nodes have correct coordinates.
    deck_node_lines = get_lines(
        contains="node ", lines=lines, after="Begin deck nodes",
        before="End deck nodes")
    assert "node 100 0 0 -16.6" in deck_node_lines[0]
    assert "node 101 10.275 0 -16.6" in deck_node_lines[1]
    assert "92.475 0 16.6" in deck_node_lines[-2]
    assert "102.75 0 16.6" in deck_node_lines[-1]

    # Assert section 0 is inserted.
    section_lines = [line for line in lines if "section " in line]
    assert (
        f"section ElasticMembranePlateSection 0 38400 0.2 0.75 0.002724"
        in section_lines[0])

    # Assert first shell is inserted.
    first_element = f"element ShellMITC4 1 100 101 201 200 0"
    element_lines = [line for line in lines if "ShellMITC4 " in line]
    assert first_element in element_lines[0]

    # Should have y-translation but not other translations.
    y_out_line = next(line for line in lines if "y.out" in line)
    assert not any(("x.out" in line) for line in lines)
    # Check all nodes are recorded.
    deck_node_str = y_out_line.split(" -node ")[1].split(" -dof ")[0].strip()
    deck_node_ids = list(map(int, deck_node_str.split()))
    num_deck_nodes = (
        ((c.bridge.length / c.os_node_step) + 1)
        * ((c.bridge.width / c.os_node_step_z) + 1))
    assert len(deck_node_ids) == num_deck_nodes


def test_build_d3_loads():
    """Test loads are placed correctly on the deck."""
    # Setup.
    c = bridge_705_test_config(bridge=bridge_705_3d)
    # Nodes along z will jump to next 100, since we divide by 10.
    c.os_node_step = c.bridge.length / 10
    c.os_node_step_z = c.bridge.width / 10
    os_runner = OSRunner(c=c)
    load = Load(x_frac=0.5, kn=1234)
    load.z_frac = 0.5

    # Build model file.
    expt_params = ExptParams([FEMParams(
        loads=[load], response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    build_model(c=c, expt_params=expt_params, os_runner=os_runner)
    with open(os_runner.fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl")) as f:
        lines = f.readlines()

    load_lines = [line.strip() for line in lines if "load" in line]
    # 11 nodes along z, and along x. So we expect a load at node 505.
    assert "load 605 0 1234000 0 0 0 0" in load_lines
