from pathlib import Path

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim

config = configs.opensees_default(bridges.bridge_narrow)
point_loads = [model.PointLoad(x=5, z=0, load=100)]
responses = sim.responses.load(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.savefig(Path("~/docker.png").expanduser().as_posix())
