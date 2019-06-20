"""
Plot a few results.
"""
import numpy as np

import plot
from influence_line import ILMatrix
from model import *
from models import bridge_705_config


if __name__ == "__main__":
    c = bridge_705_config
    num_loads = 3
    at_load = 1
    at_fiber = 0
    response_type = Response.Stress

    # Plot response from the ILMatrix.
    il_matrix = ILMatrix.load(c, num_loads, response_type)
    data = np.array(il_matrix.responses[at_load][at_fiber])
    print(data.shape)
    plot.animate_bridge_response(c.bridge, data)

    plot.plot_section(bridge_705_config.bridge.sections[0])
