import numpy as np

from bridge_sim import creep, shrinkage
from bridge_sim.util import convert_times


def test_creep_non_negative():
    days = np.arange(365)
    seconds = convert_times(f="day", t="second", times=days)
    strain = creep.creep(shrinkage.CementClass.Normal, h_0=250, times=seconds)
    assert strain[0] >= 0
