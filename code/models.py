"""
Specifications of a model of bridge 705.
"""
from model import *

bridge_705 = Bridge(
    num_elems=300,
    node_step=0.2,
    fixed_nodes=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)])
