"""
Bridge models and simulation parameters.
"""
from model import *

bridge_705_model = Bridge(
    length=60,
    fixed_nodes=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)]
)

bridge_705_config = Config(bridge_705_model)
