########################################
# Example 1: responses to a point-load #
########################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim

config = configs.opensees_default(bridges.bridge_705(msl=10))
point_loads = [model.PointLoad(x=5, z=0, load=100)]
responses = sim.responses.load(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config.bridge, piers=True)
plt.tight_layout()
plt.show()

