"""Test creep module."""

import numpy as np

from bridge_sim import configs, creep, shrinkage
from bridge_sim.util import convert_times


def test_creep_non_negative():
    config, _ = configs.test_config(msl=10)
    days = np.arange(365)
    seconds = convert_times(f="day", t="second", times=days)
    strain = creep.creep_coeff(config, shrinkage.CementClass.Normal, times=seconds, x=51)
    assert strain[0] >= 0
