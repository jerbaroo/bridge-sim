import plot
from config import bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from model import *


if __name__ == "__main__":
    c = bridge_705_config
    at_load = 1
    at_fiber = 0
    response_type = Response.Stress
    runner = os_runner

    # Plot response from the ILMatrix.
    il_matrix = ILMatrix.load(c, response_type, runner)
    data = np.array(il_matrix.fem_responses.responses[at_load][at_fiber])
    plot.animate_bridge_response(c.bridge, data)

    plot.plot_section(bridge_705_config.bridge.sections[0])
