"""Test model.bridge."""
from typing import Optional, List

import numpy as np
import pytest

from model.bridge import Bridge, Dimensions, Fix, Patch, Section, Support3D, Support

a_section = Section(patches=[Patch(y_min=-1, y_max=0, z_min=-10, z_max=10)])


def mk_bridge(
        supports: List[Support] = [], sections: List[Section] = [a_section]):
    """A bridge with valid but uninteresting values."""
    return Bridge(
        name="test", length=100, width=20, supports=supports, sections=sections,
        lanes=[], dimensions=Dimensions.D2)


def test_too_many_sections():
    with pytest.raises(ValueError) as e:
        mk_bridge(sections=[a_section, a_section])
    assert "1 section" in str(e.value)
    mk_bridge(sections=[a_section])


def test_bridge_fixed_x_dof():
    with pytest.raises(ValueError) as e:
        mk_bridge(supports=[Fix(x_frac=1, x=False)])
    assert "fixed node" in str(e.value)
    mk_bridge(supports=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])


def test_bridge_mixed_supports():
    with pytest.raises(ValueError) as e:
        mk_bridge(supports=[
            Fix(x_frac=1, x=True),
            Support3D(x=50, z=0, length=4, height=2)])
    assert "supports" in str(e.value)
    mk_bridge(supports=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])


def test_patch():
    patch = Patch(y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=5)
    expected_y = -0.5
    expected_z = [-0.8, -0.4, 0, 0.4, 0.8]
    for i, point in enumerate(patch.points()):
        assert point.y == expected_y
        assert np.isclose(point.z, expected_z[i])
