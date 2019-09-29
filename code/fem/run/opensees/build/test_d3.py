"""Test that OpenSees builds 3D model files correctly."""
import itertools
from typing import List, Optional

from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d, next_node_id, get_node, reset_node_ids, ff_node_ids, next_pow_10, x_positions_of_bottom_support_nodes, x_positions_of_deck_support_nodes, z_positions_of_bottom_support_nodes, z_positions_of_deck_support_nodes
from model.bridge import Dimensions
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import DisplacementCtrl, Load
from model.response import ResponseType
from util import round_m


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
    build_model_3d(
        c=c, expt_params=expt_params, os_runner=os_runner,
        support_3d_nodes=False)
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
    section_lines = get_lines(
        contains="section ", lines=lines, after="Begin sections",
        before="End sections")
    assert (
        f"section ElasticMembranePlateSection 0 38400 0.2 0.75 0.002724"
        in section_lines[0])

    # Assert first shell is inserted.
    first_element = f"element ShellMITC4 1 100 101 201 200 0"
    element_lines = get_lines(
        contains="ShellMITC4 ", lines=lines, after="Begin deck elements",
        before="End deck elements")
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
    build_model_3d(
        c=c, expt_params=expt_params, os_runner=os_runner,
        support_3d_nodes=False)
    with open(os_runner.fem_file_path(
            fem_params=expt_params.fem_params[0], ext="tcl")) as f:
        lines = f.readlines()

    load_lines = [line.strip() for line in lines if "load" in line]
    # 11 nodes along z, and along x. So we expect a load at node 605:
    # 100, 200, 300, 400, 500, 600 <- 5th along z
    # 600, 601, 602, 603, 604, 605 <- 5th along x
    assert "load 605 0 1234000 0 0 0 0" in load_lines


def test_x_positions_of_deck_support_nodes():
    """Test the x positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    x_positions = list(itertools.chain.from_iterable(
        x_positions_of_deck_support_nodes(c)))
    # There are 4 supports at each x position, with two lines of deck nodes.
    assert len(x_positions) == len(c.bridge.supports) * 2
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        x_min = round_m(support.x - (support.length / 2))
        x_max = round_m(support.x + (support.length / 2))
        assert x_min in x_positions
        assert x_max in x_positions


def test_z_positions_of_deck_support_nodes():
    """Test the z positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    z_positions = list(itertools.chain.from_iterable(
        z_positions_of_deck_support_nodes(c)))
    # There are 4 supports at each x position.
    assert len(z_positions) == (
        len(c.bridge.supports) * c.os_support_num_nodes_z)
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        z_min = round_m(support.z - (support.width_top / 2))
        z_max = round_m(support.z + (support.width_top / 2))
        assert z_min in z_positions
        assert z_max in z_positions


def test_x_positions_of_bottom_support_nodes():
    """Test the x positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    x_positions = x_positions_of_bottom_support_nodes(c)
    assert len(x_positions) == len(c.bridge.supports)
    # Each support meets at a point.
    for positions in x_positions:
        assert len(positions) == 1


def test_z_positions_of_bottom_support_nodes():
    """Test the z positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    z_positions = list(itertools.chain.from_iterable(
        z_positions_of_bottom_support_nodes(c)))
    assert len(z_positions) == (
        len(c.bridge.supports) * c.os_support_num_nodes_z)
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        z_min = round_m(support.z - (support.width_bottom / 2))
        z_max = round_m(support.z - (support.width_bottom / 2))
        assert z_min in z_positions
        assert z_max in z_positions


def test_get_node():
    """Test an already created node is returned."""
    reset_node_ids()
    node1 = get_node(1, 1, 1)
    node2 = get_node(1, 1, 1)
    node3 = get_node(1, 1, 2)
    assert node1.n_id == node2.n_id
    assert node3.n_id != node2.n_id
