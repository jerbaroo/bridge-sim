"""Make all plots for the thesis."""
from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from plot import *
from model import *


def make_bridge_plots(c: Config):
    """Make plots of the bridge with and without load."""
    # plot_bridge_first_section(c.bridge, save=c.image_path(f"bridge-section"))
    for loads in [
            [],
            [Load(0.4, 500)],
            [Load(0.6, [79, 101, 45], axle_distances=[2, 1.5]),
             Load(0.5, [79, 101, 45], axle_distances=[2, 1.5]),
             Load(0.6, [79, 101, 45], axle_distances=[2, 1.5], lane=1)]]:
        load_str = "-".join(str(l).replace(".", ",") for l in loads)
        plot_bridge_deck_side(c.bridge, loads=loads,
            save=c.image_path(f"bridges/side-{load_str}"))
        plot_bridge_deck_top(c.bridge, loads=loads,
            save=c.image_path(f"bridges/top-{load_str}"))


def make_influence_lines(c: Config):
    """Make plots of the influence lines."""
    for response_type in ResponseType:
        il_matrix = ILMatrix.load(c, response_type, os_runner(c))
        il_matrix.imshow(save=True)
        il_matrix.plot_ils(save=True)


if __name__ == "__main__":
    c = bridge_705_config()
    make_bridge_plots(c)
    # gen_influence_lines(c)
    # at_load = 1
    # at_fiber = 0
    # response_type = Response.Stress
    # runner = os_runner

    # Plot response from the ILMatrix.
    # il_matrix = ILMatrix.load(c, response_type, runner)
    # data = np.array(il_matrix.fem_responses.responses[at_load][at_fiber])
    # plot.animate_bridge_response(c.bridge, data)
    # plot.plot_section(bridge_705_config.bridge.sections[0])
