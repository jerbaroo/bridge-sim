"""
Description of bridge 705 and simulation parameters.
"""
from config import Config
from model import *

bridge_705 = Bridge(
    length=60,
    fixed_nodes=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)],
    sections=[Section(
        patches=[
            Patch(-0.2, -1.075, 0, 1.075),
            Patch(-1.25, -0.25, -0.2, 0.25)
        ], layers=[
            Layer(-0.04, -1.035, -0.04, 0.21, num_fibers=16, area_fiber=4.9e-4),
            Layer(-1.21, -0.21, -1.21, 0.21, num_fibers=5, area_fiber=4.9e-4),
            Layer(-1.16, -0.21, -1.16, 0.21, num_fibers=6, area_fiber=4.9e-4)
        ]
    )]
)

bridge_705_config = Config(bridge_705)
