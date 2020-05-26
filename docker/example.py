from pathlib import Path

import bridge_sim.sim
import bridge_sim.sim.responses
import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, fem, model, plot

config = configs.opensees_default(bridges.bridge_narrow)
point_loads = [model.PointLoad(x=5, z=0, load=100)]
responses = bridge_sim.sim.responses.responses(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.savefig(Path("~/docker.png").expanduser().as_posix())
