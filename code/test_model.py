"""Test model.py."""
import pytest

from model import *


def mk_bridge(
        name="test", length=1, width=1, fixed_nodes=[], sections=[None],
        lanes=[], load_density=[(1, 100)]):
    """A bridge with valid but uninteresting values."""
    return Bridge(
        name=name, length=length, width=width, fixed_nodes=fixed_nodes,
        sections=sections, lanes=lanes, load_density=load_density)


def test_bridge_fixed_x_dof():
    with pytest.raises(ValueError):
        mk_bridge(fixed_nodes=[Fix(1, x=False)])
    mk_bridge(fixed_nodes=[Fix(0, x=True), Fix(1, x=False)])


def test_bridge_load_density():
    with pytest.raises(ValueError):
        mk_bridge(load_density=[(0, 10), (0, 80)])
    mk_bridge(load_density=[(0, 20), (0, 80)])
