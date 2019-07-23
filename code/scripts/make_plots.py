"""Make all plots for the thesis."""
from config import Config, bridge_705_config
from fem.responses.il import DCMatrix, ILMatrix
from fem.run.opensees import os_runner
from plot import *
from plot.il import *
from model import *
from util import *


def make_bridge_plots(c: Config):
    """Make plots of the bridge with and without load."""
    plot_bridge_first_section(
        c.bridge, save=c.image_path("bridges/bridge-section"))
    for loads in [
            [],
            [Load(0.4, 500)],
            [Load(0.6, 200, axle_distances=[2, 1.5]),
             Load(0.5, 200, axle_distances=[2, 1.5]),
             Load(0.6, 200, axle_distances=[2, 1.5], lane=1)]]:
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
        matrix_subplots(
            c, il_matrix, rows=rows, cols=cols, plot_func=plot_il,
            save=c.image_path(
                f"ils/il-subplots-{il_matrix.fem_runner_name}"
                + f"-{response_type_name(response_type)}-{rows}-{cols}"))


def make_dc_plots(c: Config):
    """Make plots of the displacement control responses."""
    for response_type in ResponseType:
        dc_matrix = DCMatrix.load(c, response_type, os_runner(c))
        # num_ils, num_x = 10, 100
        # imshow_il(c, il_matrix, save=c.image_path(
        #     f"ils/il-imshow-{il_matrix.fem_runner_name}"
        #     + f"-{response_type_name(response_type)}"
        #     + f"-{num_ils}-{num_x}"))
        # rows, cols = 4, 3
        matrix_subplots(
            c, dc_matrix, plot_func=plot_dc,
            save=c.image_path(
                f"dcs/dc-subplots-{dc_matrix.fem_runner_name}"
                + f"-{response_type_name(response_type)}"))


def make_mv_load_animations(c: Config):
    """Make animations of loads moving across a bridge."""
    mv_load = MovingLoad(Load(x_frac=0, kn=100), kmph=20)
    # for response_type in [ResponseType.YTranslation]:
    for response_type in ResponseType:
        animate_mv_load(
            c, mv_load, response_type, os_runner(c),
            show=True)
            # save=c.image_path(
            #     f"animations/-{c.bridge.name}"
            #     + f"-{response_type_name(response_type)}-1load"
            #     + f"-{mv_load.str_id()}"))


if __name__ == "__main__":
    c = bridge_705_config()
    # clean_generated(c)
    make_mv_load_animations(c)
    # make_bridge_plots(c)
    # make_il_plots(c)
    # make_dc_plots(c)
