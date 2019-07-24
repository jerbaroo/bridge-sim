"""Test model.py."""
import pytest

from model import *


def mk_bridge(
        name="test", length=1, width=1, fixed_nodes=[], sections=[None],
        lanes=[], load_frequencies=[(1, 1)]):
    """A bridge with valid but uninteresting values."""
    return Bridge(
        name=name, length=length, width=width, fixed_nodes=fixed_nodes,
        sections=sections, lanes=lanes, load_frequencies=load_frequencies)


def test_bridge_fixed_x_dof():
    with pytest.raises(ValueError):
        mk_bridge(fixed_nodes=[Fix(1, x=False)])
    mk_bridge(fixed_nodes=[Fix(0, x=True), Fix(1, x=False)])


def test_bridge_load_frequencies():
    with pytest.raises(ValueError):
        mk_bridge(load_frequencies=[(0, 0.1), (0, 0.8)])
    mk_bridge(load_frequencies=[(0, 0.2), (0, 0.8)])
