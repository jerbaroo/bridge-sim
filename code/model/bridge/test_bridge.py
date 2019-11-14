"""Test model.bridge."""
from typing import Optional, List

import numpy as np
import pytest

from model.bridge import (
    Bridge,
    Dimensions,
    Fix,
    Lane,
    Patch,
    Section,
    Section2D,
    Section3D,
    Support3D,
    Support,
)

# Some sections and supports to reuse.

a_2d_section = Section2D(
    patches=[Patch(y_min=-1, y_max=0, z_min=-10, z_max=10)]
)
a_3d_section = Section3D(density=1, thickness=2, youngs=3, poissons=4)
a_3d_support = Support3D(
    x=50, z=0, length=4, height=2, width_top=3, width_bottom=1, sections=[]
)


def mk_bridge(
    supports: List[Support] = [],
    sections: List[Section] = [a_2d_section],
    dimensions: Dimensions = Dimensions.D2,
):
    """A bridge with valid but uninteresting values."""
    return Bridge(
        name="test",
        length=100,
        width=20,
        supports=supports,
        sections=sections,
        lanes=[],
        dimensions=dimensions,
        base_mesh_deck_nodes_x=10,
        base_mesh_deck_nodes_z=10,
        base_mesh_pier_nodes_y=10,
        base_mesh_pier_nodes_z=10,
    )


def test_2d_bridge_too_many_sections():
    """A 2D bridge may only have 1 section."""
    with pytest.raises(ValueError) as e:
        mk_bridge(sections=[a_2d_section, a_2d_section])
    assert "1 section" in str(e.value)
    mk_bridge(sections=[a_2d_section])


def test_2d_bridge_fixed_x_dof():
    """A 2D bridge must have first Fix, fixed in x direction."""
    with pytest.raises(ValueError) as e:
        mk_bridge(supports=[Fix(x_frac=0, x=False)])
    assert "node at x=0 fixed" in str(e.value)
    mk_bridge(supports=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])


def test_2d_bridge_mixed_supports():
    """A 2D bridge with mixed 2D and 3D supports."""
    with pytest.raises(AttributeError) as e:
        mk_bridge(supports=[Fix(x_frac=1, x=True), a_3d_support])
    assert "'Support3D' object has no attribute 'z_min_max'" in str(e.value)
    mk_bridge(supports=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])


def test_3d_bridge_mixed_supports():
    """A 3D bridge with mixed 2D and 3D supports."""
    with pytest.raises(ValueError) as e:
        bridge = Bridge(
            name="test",
            length=12,
            width=50,
            supports=[a_3d_support, Fix(0, True)],
            sections=[a_3d_section],
            lanes=[],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "Support3D supports" in str(e.value)
    bridge = Bridge(
        name="test",
        length=12,
        width=50,
        supports=[a_3d_support, a_3d_support],
        sections=[a_3d_section],
        lanes=[],
        dimensions=Dimensions.D3,
        base_mesh_deck_nodes_x=10,
        base_mesh_deck_nodes_z=10,
        base_mesh_pier_nodes_y=10,
        base_mesh_pier_nodes_z=10,
    )


def test_3d_bridge_lane_or_support_out_of_range():
    with pytest.raises(ValueError) as e:
        bridge = Bridge(
            name="test",
            length=12,
            width=8,
            supports=[a_3d_support, a_3d_support],
            sections=[a_3d_section],
            lanes=[Lane(-4.1, 3, True)],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "Lane" in str(e.value)
    with pytest.raises(ValueError) as e:
        bridge = Bridge(
            name="test",
            length=12,
            width=8,
            supports=[a_3d_support, a_3d_support],
            sections=[a_3d_section],
            lanes=[Lane(1, 5, True)],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "Lane" in str(e.value)
    with pytest.raises(ValueError) as e:
        support = Support3D(
            x=50,
            z=0,
            length=4,
            height=2,
            width_top=10,
            width_bottom=1,
            sections=[],
        )
        bridge = Bridge(
            name="test",
            length=12,
            width=8,
            supports=[support],
            sections=[a_3d_section],
            lanes=[],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "Support" in str(e.value)
    bridge = Bridge(
        name="test",
        length=12,
        width=8,
        supports=[a_3d_support, a_3d_support],
        sections=[a_3d_section],
        lanes=[Lane(-1, 1, True)],
        dimensions=Dimensions.D3,
        base_mesh_deck_nodes_x=10,
        base_mesh_deck_nodes_z=10,
        base_mesh_pier_nodes_y=10,
        base_mesh_pier_nodes_z=10,
    )


def test_3d_bridge_height():
    """A 3D bridge has correct computed height."""
    # Bridge should have height of the support.
    support = Support3D(
        x=50,
        z=0,
        length=4,
        height=2.1,
        width_top=3,
        width_bottom=1,
        sections=[],
    )
    section = Section3D(density=1, thickness=0.6, youngs=3, poissons=4)
    bridge = Bridge(
        name="test",
        length=12,
        width=10,
        supports=[support],
        sections=[section],
        lanes=[],
        dimensions=Dimensions.D3,
        base_mesh_deck_nodes_x=10,
        base_mesh_deck_nodes_z=10,
        base_mesh_pier_nodes_y=10,
        base_mesh_pier_nodes_z=10,
    )
    assert bridge.height == support.height

    # Bridge should have height of the section.
    section.thickness = 3
    bridge = Bridge(
        name="test",
        length=12,
        width=10,
        supports=[support],
        sections=[section],
        lanes=[],
        dimensions=Dimensions.D3,
        base_mesh_deck_nodes_x=10,
        base_mesh_deck_nodes_z=10,
        base_mesh_pier_nodes_y=10,
        base_mesh_pier_nodes_z=10,
    )
    assert bridge.height == section.thickness


def test_3d_bridge_sections():
    """A 3D bridge must have correctly constructed sections."""
    # First section doesn't start at 0.
    with pytest.raises(ValueError) as e:
        section_1 = Section3D(
            density=1, thickness=2, youngs=3, poissons=4, start_x_frac=0.1
        )
        bridge = Bridge(
            name="test",
            length=12,
            width=7,
            supports=[a_3d_support],
            sections=[section_1],
            lanes=[],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "must start at 0" in str(e.value)

    # Order of sections is incorrect.
    with pytest.raises(ValueError) as e:
        section_1 = Section3D(
            density=1, thickness=2, youngs=3, poissons=4, start_x_frac=0
        )
        section_2 = Section3D(
            density=1, thickness=2, youngs=3, poissons=4, start_x_frac=0.5
        )
        section_3 = Section3D(
            density=1, thickness=2, youngs=3, poissons=4, start_x_frac=0.2
        )
        bridge = Bridge(
            name="test",
            length=12,
            width=7,
            supports=[a_3d_support],
            sections=[section_1, section_2, section_3],
            lanes=[],
            dimensions=Dimensions.D3,
            base_mesh_deck_nodes_x=10,
            base_mesh_deck_nodes_z=10,
            base_mesh_pier_nodes_y=10,
            base_mesh_pier_nodes_z=10,
        )
    assert "Sections not in order" in str(e.value)


def test_patch_points():
    """Test a Patch's points are as expected."""
    patch = Patch(y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=5)
    expected_y = -0.5
    expected_z = [-0.8, -0.4, 0, 0.4, 0.8]
    for i, point in enumerate(patch.points()):
        assert point.y == expected_y
        assert np.isclose(point.z, expected_z[i])
