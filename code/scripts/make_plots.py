"""Make all plots for the thesis."""
from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from plot import *
from plot.il import imshow_il, plot_ils
from model import *
from util import *


def make_bridge_plots(c: Config):
    """Make plots of the bridge with and without load."""
    plot_bridge_first_section(
        c.bridge, save=c.image_path("bridges/bridge-section"))
    for loads in [
            [],
            [Load(0.4, 500)],
            [Load(0.6, [0, 0, 0], axle_distances=[2, 1.5]),
             Load(0.5, [0, 0, 0], axle_distances=[2, 1.5]),
             Load(0.6, [0, 0, 0], axle_distances=[2, 1.5], lane=1)]]:
        load_str = "-".join(str(l).replace(".", ",") for l in loads)
        plot_bridge_deck_side(c.bridge, loads=loads,
            save=c.image_path(f"bridges/side-{load_str}"))
        plot_bridge_deck_top(c.bridge, loads=loads,
            save=c.image_path(f"bridges/top-{load_str}"))


def make_il_plots(c: Config):
    """Make plots of the influence lines."""
    for response_type in ResponseType:
        il_matrix = ILMatrix.load(
            c, response_type, os_runner(c), num_loads=100)
        num_ils, num_x = 10, 100
        imshow_il(c, il_matrix, save=c.image_path(
            f"ils/il-imshow-{il_matrix.fem_runner_name}"
            + f"-{response_type_name(response_type)}"
            + f"-{num_ils}-{num_x}"))
        rows, cols = 4, 3
        plot_ils(
            c, il_matrix, rows=rows, cols=cols,
            save=c.image_path(
                f"ils/il-subplots-{il_matrix.fem_runner_name}"
                + f"-{response_type_name(response_type)}-{rows}-{cols}"))


def make_dc_plots(c: Config):
    """Make plots of the displacement control responses."""
    for response_type in ResponseType:
        il_matrix = ILMatrix.load(
            c, response_type, os_runner(c), num_loads=100)
        num_ils, num_x = 10, 100
        imshow_il(c, il_matrix, save=c.image_path(
            f"ils/il-imshow-{il_matrix.fem_runner_name}"
            + f"-{response_type_name(response_type)}"
            + f"-{num_ils}-{num_x}"))
        rows, cols = 4, 3
        plot_ils(
            c, il_matrix, rows=rows, cols=cols,
            save=c.image_path(
                f"ils/il-subplots-{il_matrix.fem_runner_name}"
                + f"-{response_type_name(response_type)}-{rows}-{cols}"))


if __name__ == "__main__":
    c = bridge_705_config()
    # clean_generated(c)
    # make_bridge_plots(c)
    make_il_plots(c)
    # at_load = 1
    # at_fiber = 0
    # response_type = Response.Stress
    # runner = os_runner

    # Plot response from the ILMatrix.
    # il_matrix = ILMatrix.load(c, response_type, runner)
    # data = np.array(il_matrix.fem_responses.responses[at_load][at_fiber])
    # plot.animate_bridge_response(c.bridge, data)
    # plot.plot_section(bridge_705_config.bridge.sections[0])
