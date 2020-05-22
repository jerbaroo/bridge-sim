"""Test that OpenSees builds 3D model files correctly."""
import itertools
from typing import List, Optional

import numpy as np

from fem.params import ExptParams, SimParams
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import (
    build_model_3d,
    get_node,
    reset_elem_ids,
    reset_nodes,
    opensees_deck_nodes,
    opensees_pier_elements,
    opensees_support_nodes,
    get_all_support_nodes,
    get_x_positions_of_pier_bottom_nodes,
    get_x_positions_of_pier_deck_nodes,
    get_z_positions_of_pier_bottom_nodes,
    get_z_positions_of_pier_deck_nodes,
    get_deck_positions,
    get_pier_elements,
)
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import PointLoad
from model.response import ResponseType
from bridge_sim.util import round_m


def get_lines(
    contains: str, lines: List[str], after: str = "", before: Optional[str] = None,
):
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
    c.bridge.base_mesh_deck_nodes_x = 11
    c.bridge.base_mesh_deck_nodes_z = 11
    c.bridge.base_mesh_pier_nodes_y = 4
    c.bridge.base_mesh_pier_nodes_z = 5
    os_runner = OSRunner(c=c)

    # Build model file.
    expt_params = ExptParams(
        [
            SimParams(
                ploads=[PointLoad(0.65, 0.35, 1234)],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )
    build_model_3d(c=c, expt_params=expt_params, os_runner=os_runner, simple_mesh=True)
    with open(
        os_runner.fem_file_path(fem_params=expt_params.fem_params[0], ext="tcl")
    ) as f:
        lines = f.readlines()

    # Assert first and last nodes have correct coordinates.
    deck_node_lines = get_lines(
        contains="node ",
        lines=lines,
        after="Begin deck nodes",
        before="End deck nodes",
    )
    assert "node 100 0 0 -16.6" in deck_node_lines[0]
    assert "node 101 10.275 0 -16.6" in deck_node_lines[1]
    assert "92.475 0 16.6" in deck_node_lines[-2]
    assert "102.75 0 16.6" in deck_node_lines[-1]
    assert len(deck_node_lines) == (
        c.bridge.base_mesh_deck_nodes_x * c.bridge.base_mesh_deck_nodes_z
    )

    # Assert section 1 is inserted correctly.
    section_lines = get_lines(
        contains="section ",
        lines=lines,
        after="Begin deck sections",
        before="End deck sections",
    )
    sline = section_lines[0]
    # Check youngs.
    id_, youngs, poissons, thickness, density = list(map(float, sline.split()[2:]))
    assert id_ == 1
    assert youngs == 38400 * 1e6
    assert poissons == 0.2
    assert thickness == 0.75
    assert np.isclose(density, 0.002724)

    # Assert first shell is inserted.
    first_element = f"element ShellMITC4 1 100 101 201 200 1"
    element_lines = get_lines(
        contains="ShellMITC4 ",
        lines=lines,
        after="Begin deck shell elements",
        before="End deck shell elements",
    )
    assert first_element in element_lines[0]

    # Should have y-translation but not other translations.
    y_out_line = next(line for line in lines if "y.out" in line)
    assert not any(("x.out" in line) for line in lines)
    # Check all nodes are recorded.
    deck_node_str = y_out_line.split(" -node ")[1].split(" -dof ")[0].strip()
    deck_node_ids = list(map(int, deck_node_str.split()))
    assert len(deck_node_ids) == (
        c.bridge.base_mesh_deck_nodes_x * c.bridge.base_mesh_deck_nodes_z
        + c.bridge.base_mesh_pier_nodes_y
        * c.bridge.base_mesh_pier_nodes_z
        * len(c.bridge.supports)
        * 2
    )

    # Support nodes of the deck shouldn't appear again.
    assert all(["comment should not exist" not in line for line in lines])


def test_build_d3_fixed_nodes():
    """Test the fixed nodes of the deck and supports."""
    # Setup.
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.bridge.base_mesh_deck_nodes_x = 4
    c.bridge.base_mesh_deck_nodes_z = 3  # Ensures no overlap with supports.
    c.bridge.base_mesh_pier_nodes_z = 6
    os_runner = OSRunner(c=c)

    # Build model file.
    expt_params = ExptParams(
        [SimParams(ploads=[], response_types=[ResponseType.YTranslation])]
    )
    build_model_3d(c=c, expt_params=expt_params, os_runner=os_runner)
    with open(
        os_runner.fem_file_path(fem_params=expt_params.fem_params[0], ext="tcl")
    ) as f:
        lines = f.readlines()

    # Check amount of fixed deck nodes.
    deck_fix_lines = get_lines(
        contains="fix ",
        lines=lines,
        after="Begin fixed deck nodes",
        before="End fixed deck nodes",
    )
    one_side_deck_fix = c.bridge.base_mesh_deck_nodes_z
    one_side_supports_fix = c.bridge.base_mesh_pier_nodes_z * 4
    # Check amount of fixed deck nodes.
    one_side_fix = one_side_deck_fix + one_side_supports_fix
    assert len(deck_fix_lines) == one_side_fix * 2

    # Check amount of fixed pier nodes.
    pier_fix_lines = get_lines(
        contains="fix ",
        lines=lines,
        after="Begin fixed support nodes",
        before="End fixed support nodes",
    )
    assert len(pier_fix_lines) == (
        len(c.bridge.supports) * c.bridge.base_mesh_pier_nodes_z
    )


def test_build_d3_loads():
    """Test loads are placed correctly on the deck."""
    # Setup.
    c = bridge_705_test_config(bridge=bridge_705_3d)
    # Nodes along z will jump to next 100, since we divide by 10.
    c.bridge.base_mesh_deck_nodes_x = 11
    c.bridge.base_mesh_deck_nodes_z = 11
    os_runner = OSRunner(c=c)
    load = PointLoad(x_frac=0.5, z_frac=0.5, kn=1234)

    # Build model file.
    expt_params = ExptParams(
        [SimParams(ploads=[load], response_types=[ResponseType.YTranslation])]
    )
    build_model_3d(c=c, expt_params=expt_params, os_runner=os_runner, simple_mesh=True)
    with open(
        os_runner.fem_file_path(fem_params=expt_params.fem_params[0], ext="tcl")
    ) as f:
        lines = f.readlines()

    load_lines = [line.strip() for line in lines if "load" in line]
    # 11 nodes along z, and along x. So we expect a load at node 605:
    # 100, 200, 300, 400, 500, 600 <- 5th along z
    # 600, 601, 602, 603, 604, 605 <- 5th along x
    assert "load 605 0 1234000 0 0 0 0" in load_lines


def test_x_positions_of_pier_deck_nodes():
    """Test the x positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    x_positions = list(
        itertools.chain.from_iterable(get_x_positions_of_pier_deck_nodes(c))
    )
    # There are 4 supports at each x position, with two lines of deck nodes.
    assert len(x_positions) == len(c.bridge.supports) * 2
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        x_min = round_m(support.x - (support.length / 2))
        x_max = round_m(support.x + (support.length / 2))
        assert x_min in x_positions
        assert x_max in x_positions


def test_z_positions_of_pier_deck_nodes():
    """Test the z positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    # Simple mesh should not affect anything here due to ([], []).
    z_positions = list(
        itertools.chain.from_iterable(
            get_z_positions_of_pier_deck_nodes(
                c=c, deck_positions=([], []), simple_mesh=False
            )
        )
    )
    # Test there are the correct amount.
    assert len(z_positions) == (
        len(c.bridge.supports) * c.bridge.base_mesh_pier_nodes_z
    )
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        z_min = round_m(support.z - (support.width_top / 2))
        z_max = round_m(support.z + (support.width_top / 2))
        assert z_min in z_positions
        assert z_max in z_positions


def test_x_positions_of_pier_bottom_nodes():
    """Test the x positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    x_positions = get_x_positions_of_pier_bottom_nodes(c)
    assert len(x_positions) == len(c.bridge.supports)
    # Each support meets at a point.
    for positions in x_positions:
        assert len(positions) == 1


def test_z_positions_of_pier_bottom_nodes():
    """Test the z positions where the supports have deck nodes."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    positions_deck = get_z_positions_of_pier_deck_nodes(
        c=c, deck_positions=([], []), simple_mesh=False
    )
    z_positions = list(
        itertools.chain.from_iterable(
            get_z_positions_of_pier_bottom_nodes(c=c, positions_deck=positions_deck)
        )
    )
    assert len(z_positions) == (
        len(c.bridge.supports) * c.bridge.base_mesh_pier_nodes_z
    )
    # Check each of the supports explicitly.
    for support in c.bridge.supports:
        z_min = round_m(support.z - (support.width_bottom / 2))
        z_max = round_m(support.z - (support.width_bottom / 2))
        assert z_min in z_positions
        assert z_max in z_positions
    # Check each z position is in range of bridge.
    for z_position in z_positions:
        assert c.bridge.z_min <= z_position <= c.bridge.z_max


def test_get_node():
    """Test an already created node is returned."""
    reset_nodes()
    node1 = get_node(1, 1, 1)
    node2 = get_node(1, 1, 1)
    node3 = get_node(1, 1, 2)
    assert node1.n_id == node2.n_id
    assert node3.n_id != node2.n_id


def test_support_nodes():
    """Test the correct amount of support nodes."""
    reset_nodes()
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.bridge.base_mesh_pier_nodes_z = 4
    c.bridge.base_mesh_pier_nodes_y = 5
    deck_positions = get_deck_positions(
        c=c, fem_params=SimParams([], []), simple_mesh=True
    )
    all_support_nodes = get_all_support_nodes(
        c=c, deck_positions=deck_positions, simple_mesh=True
    )

    # Test the amount of pier nodes in the base mesh is correct. This will
    # include those nodes which are also part of the bridge deck's base mesh
    # will and include the bottom nodes of the piers which are in both walls.
    count = 0
    for s_nodes in all_support_nodes:
        assert len(s_nodes) == 2
        count += len(list(itertools.chain.from_iterable(s_nodes[0])))
        count += len(list(itertools.chain.from_iterable(s_nodes[1])))
    nodes_per_wall = c.bridge.base_mesh_pier_nodes_y * c.bridge.base_mesh_pier_nodes_z
    expected = len(c.bridge.supports) * nodes_per_wall * 2
    assert expected == count

    # Test the amount of pier nodes without overlap between bottom nodes.
    reset_nodes()
    node_lines = opensees_support_nodes(
        c=c, deck_nodes=[[]], all_support_nodes=all_support_nodes, simple_mesh=True,
    )
    num_nodes = len(node_lines.split("\n")) - 3  # Minus comments.
    # Subtract 1x overlap of bottom nodes, per support.
    expected_wo_overlap = expected - (
        len(c.bridge.supports) * c.bridge.base_mesh_pier_nodes_z
    )
    assert num_nodes == expected_wo_overlap

    # Test the amount of nodes without overlap of bottom and deck nodes.
    reset_nodes()
    # Start with full deck nodes..
    deck_positions = get_deck_positions(
        c=c, fem_params=SimParams([], []), simple_mesh=False
    )
    _, deck_nodes = opensees_deck_nodes(
        c=c, fem_params=SimParams([], []), deck_positions=deck_positions
    )
    # ..then get pier nodes, without deck positions added to pier's mesh.
    all_support_nodes = get_all_support_nodes(
        c=c, deck_positions=deck_positions, simple_mesh=True
    )
    # This time, the pier nodes that are at the very top, and part of the deck,
    # should not be included.
    node_lines = opensees_support_nodes(
        c=c,
        deck_nodes=deck_nodes,
        all_support_nodes=all_support_nodes,
        simple_mesh=True,
    )
    num_nodes = len(node_lines.split("\n")) - 3  # Minus comments.
    print(expected_wo_overlap)
    assert num_nodes == expected_wo_overlap - (
        len(c.bridge.supports) * c.bridge.base_mesh_pier_nodes_z * 2
    )


def test_support_elements():
    """Test that support elements are correctly generated."""
    reset_elem_ids()
    reset_nodes()
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.bridge.base_mesh_pier_nodes_y = 5
    c.bridge.base_mesh_pier_nodes_z = 4
    # opensees_deck_nodes(c, support_nodes=True)  # To set ff_mod.
    # Simple mesh should not affect anything here due to ([], []).
    all_pier_nodes = get_all_support_nodes(
        c=c, deck_positions=([], []), simple_mesh=False
    )
    all_pier_elements = get_pier_elements(c=c, all_support_nodes=all_pier_nodes)
    lines = opensees_pier_elements(c=c, all_pier_elements=all_pier_elements).split("\n")
    lines = get_lines(
        contains="ShellMITC4 ",
        lines=lines,
        after="Begin pier shell elements",
        before="End pier shell elements",
    )

    # Test the amount of elements is correct.
    # Two walls per support.
    expected = len(c.bridge.supports) * 2
    # A grid of elements per wall.
    expected *= c.bridge.base_mesh_pier_nodes_y - 1
    expected *= c.bridge.base_mesh_pier_nodes_z - 1
    assert len(lines) == expected


def test_support_elements_from_small_example():
    """Test support elements from small example for manual inspection."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.bridge.base_mesh_deck_nodes_x = 3
    c.bridge.base_mesh_deck_nodes_z = 3
    c.bridge.base_mesh_pier_nodes_y = 2
    c.bridge.base_mesh_pier_nodes_z = 2
    os_runner = OSRunner(c=c)

    # Build model file.
    expt_params = ExptParams(
        [
            SimParams(
                ploads=[PointLoad(x_frac=0.5, z_frac=0.5, kn=1234)],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )
    build_model_3d(c=c, expt_params=expt_params, os_runner=os_runner)

    # Get lines of support elements.
    with open(
        os_runner.fem_file_path(fem_params=expt_params.fem_params[0], ext="tcl")
    ) as f:
        lines = f.readlines()
    lines = get_lines(
        contains="ShellMITC4 ",
        lines=lines,
        after="Begin pier shell elements",
        before="End pier shell elements",
    )

    # Test the first element has correct nodes.
    assert any("201 1200 1300 301" in l and "ShellMITC4" in l for l in lines)
    assert any("202 1200 1300 302" in l and "ShellMITC4" in l for l in lines)


def test_make_small_example():
    """Make a small example tcl file for manual inspection."""
    c = bridge_705_test_config(bridge=bridge_705_3d)
    c.os_node_step = c.bridge.length / 2
    c.os_node_step_z = c.bridge.width / 2
    c.os_support_num_nodes_z = 2
    c.os_support_num_nodes_y = 2
    os_runner = OSRunner(c=c)
    # Build model file.
    expt_params = ExptParams(
        [
            SimParams(
                ploads=[PointLoad(x_frac=0.5, z_frac=0.5, kn=1234)],
                response_types=[ResponseType.YTranslation, ResponseType.Strain],
            )
        ]
    )
    build_model_3d(c=c, expt_params=expt_params, os_runner=os_runner)
