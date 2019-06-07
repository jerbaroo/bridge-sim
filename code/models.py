"""
Bridge model and simulation parameters.
"""
from config import Config
from model import *

bridge_705 = Bridge(
    length=60,
    fixed_nodes=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)],
    sections=[Section([
        Patch(-0.2, -1.075, 0, 1.075),
        Patch(-1.25, -0.25, -0.2, 0.25)
    ])])

bridge_705_config = Config(bridge_705)
