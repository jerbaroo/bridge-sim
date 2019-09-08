"""Test model.py."""
import numpy as np
import pytest

from model.bridge import Bridge, Fix, Patch, Section


def test_patch():
    patch = Patch(y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=5)
    expected_y = -0.5
    expected_z = [-0.8, -0.4, 0, 0.4, 0.8]
    for i, point in enumerate(patch.points()):
        assert point.y == expected_y
        assert np.isclose(point.z, expected_z[i])


def test_bridge_fixed_x_dof():

    def mk_bridge(
            name="test", length=1, width=1, fixed_nodes=[], sections=None,
            lanes=[]):
        """A bridge with valid but uninteresting values."""
        if sections is None: 
            sections = [Section(patches=[Patch(
                y_min=-1, y_max=0, z_min=-1, z_max=1)])]
        return Bridge(
            name=name, length=length, fixed_nodes=fixed_nodes,
            sections=sections, lanes=lanes)

    with pytest.raises(ValueError):
        mk_bridge(fixed_nodes=[Fix(x_frac=1, x=False)])
    mk_bridge(fixed_nodes=[Fix(x_frac=0, x=True), Fix(x_frac=1, x=False)])
