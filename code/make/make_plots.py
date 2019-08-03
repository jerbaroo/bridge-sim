"""Make all plots for the thesis."""
from config import Config
from fem.responses.matrix import DCMatrix, ILMatrix
from fem.run.opensees import os_runner
from plot import *
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il
from plot.vehicles import *
from model import *
from model.bridge_705 import bridge_705_config
from util import *
from vehicles.sample import sample_vehicle


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


def make_normal_mv_load_animations(c: Config):
    """Make animations of a load moving across a bridge."""
    mv_load = MovingLoad.from_vehicle(
        x_frac=0, vehicle=sample_vehicle(c), lane=0)
    for fem_runner in [os_runner(c)]:
        for response_type in ResponseType:
            animate_mv_load(
                c, mv_load, response_type, fem_runner,
                save=pstr(c.image_path(
                    f"animations/{c.bridge.name}-{fem_runner.name}"
                    + f"-{response_type_name(response_type)}-load"
                    + f"-{mv_load.str_id()}")).lower() + ".mp4")


def make_vehicle_plots(c: Config):
    plot_density(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-density"))
    plot_length_vs_axles(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-length-vs-axles"))
    plot_length_vs_weight(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-length-vs-weight"))
    plot_weight_vs_axles(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-weight-vs-axles"))


def make_all(c: Config, clean=True):
    """Make all plots for the thesis."""
    if clean: clean_generated(c)
    # make_bridge_plots(c)
    # make_il_plots(c)
    # make_dc_plots(c)
    make_normal_mv_load_animations(c)
    make_vehicle_plots(c)


if __name__ == "__main__":
    make_all(bridge_705_config(), clean=False)
