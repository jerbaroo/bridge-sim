"""Test model.py."""
import pytest

from model import *


def test_fixed_x_dof():
    with pytest.raises(ValueError):
        Bridge(1, 1, [Fix(1, x=False)])
    Bridge(1, 1, [Fix(0, x=True), Fix(1, x=False)], sections=[None])
