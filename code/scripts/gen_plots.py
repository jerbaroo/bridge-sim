"""Generate plots."""
from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from model import *


def plot_influence_lines(c: Config):
    for response_type in ResponseType:
        il_matrix = ILMatrix.load(c, response_type, os_runner(c))
        il_matrix.imshow(save=True)
        il_matrix.plot_ils(save=True)


if __name__ == "__main__":
    c = bridge_705_config()
    plot_influence_lines(c)
    # at_load = 1
    # at_fiber = 0
    # response_type = Response.Stress
    # runner = os_runner

    # Plot response from the ILMatrix.
    # il_matrix = ILMatrix.load(c, response_type, runner)
    # data = np.array(il_matrix.fem_responses.responses[at_load][at_fiber])
    # plot.animate_bridge_response(c.bridge, data)
    # plot.plot_section(bridge_705_config.bridge.sections[0])
