"""Test model.bridge."""
from typing import Optional, List

import numpy as np
import pytest

from model.bridge import Bridge, Dimensions, Fix, Patch, Section, Section2D, Section3D, Support3D, Support

a_2d_section = Section2D(
    patches=[Patch(y_min=-1, y_max=0, z_min=-10, z_max=10)])
a_3d_section = Section3D(density=1, thickness=2, youngs=3)
a_3d_support = Support3D(
    x=50, z=0, length=4, height=2, width_top=3, width_bottom=1)


def mk_bridge(
        supports: List[Support] = [], sections: List[Section] = [a_2d_section],
        dimensions: Dimensions = Dimensions.D2):
    """A bridge with valid but uninteresting values."""
    return Bridge(
        name="test", length=100, width=20, supports=supports,
        sections=sections, lanes=[], dimensions=dimensions)


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
    """A 2D bridge with 2D (Fix) and 3D supports."""
    with pytest.raises(ValueError) as e:
        mk_bridge(supports=[Fix(x_frac=1, x=True), a_3d_support])
    assert "Fix supports" in str(e.value)
    mk_bridge(supports=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])


def test_3d_bridge_mixed_supports():
    """A 3D bridge with 2D (Fix) and 3D supports."""
    with pytest.raises(ValueError) as e:
        mk_bridge(
            supports=[Fix(x_frac=1, x=True), a_3d_support],
            dimensions=Dimensions.D3)
    assert "Support3D supports" in str(e.value)
    mk_bridge(supports=[], dimensions=Dimensions.D3)


def test_3d_bridge_length_width():
    """A 3D bridge has length and width."""
    bridge = Bridge(
        name="test", length=12, width=a_3d_support.width_top,
        supports=[a_3d_support], sections=[a_3d_section], lanes=[],
        dimensions=Dimensions.D3)
    assert bridge.length == 12
    assert bridge.width == a_3d_support.width_top


def test_patch_points():
    """Test a Patch's points are as expected."""
    patch = Patch(y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=5)
    expected_y = -0.5
    expected_z = [-0.8, -0.4, 0, 0.4, 0.8]
    for i, point in enumerate(patch.points()):
        assert point.y == expected_y
        assert np.isclose(point.z, expected_z[i])
