"""Make all plots for the thesis."""
import numpy as np

from config import Config
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import load_il_matrix
from fem.run.opensees import os_runner
from plot import animate_mv_load, plot_bridge_deck_side, plot_bridge_deck_top, plot_bridge_first_section
from plot.features import plot_events_from_normal_mv_loads
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il
from plot.vehicles import plot_density, plot_length_vs_axles, plot_length_vs_weight, plot_weight_vs_axles
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import Load, MovingLoad
from model.response import ResponseType
from util import pstr, clean_generated
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
        plot_bridge_deck_side(
            c.bridge, loads=loads,
            save=c.image_path(f"bridges/side-{load_str}"))
        plot_bridge_deck_top(
            c.bridge, loads=loads,
            save=c.image_path(f"bridges/top-{load_str}"))


def make_il_plots(c: Config):
    """Make plots of the influence lines."""
    for response_type in ResponseType:
        num_ils, num_x = 100, 100
        il_matrix = load_il_matrix(
            c=c, response_type=response_type, fem_runner=os_runner(c),
            num_loads=num_ils)
        imshow_il(
            c=c, il_matrix=il_matrix, num_ils=num_ils, num_x=num_x,
            save=c.image_path(
                f"ils/il-imshow-{il_matrix.fem_runner_name}"
                + f"-{response_type.name()}"
                + f"-{num_ils}-{num_x}"))
        rows, cols = 4, 3
        matrix_subplots(
            c, il_matrix, rows=rows, cols=cols, plot_func=plot_il,
            save=c.image_path(
                f"ils/il-subplots-{il_matrix.fem_runner_name}"
                + f"-{response_type.name()}-{rows}-{cols}"))


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
                + f"-{response_type.name()}"))


def make_normal_mv_load_animations(c: Config, per_axle: bool = False):
    """Make animations of a load moving across a bridge."""
    mv_load = MovingLoad.from_vehicle(
        x_frac=0, vehicle=sample_vehicle(c), lane=0)
    per_axle_str = f"-peraxle" if per_axle else ""
    for response_type in ResponseType:
        animate_mv_load(
            c, mv_load, response_type, os_runner(c), per_axle=per_axle,
            save=pstr(c.image_path(
                f"animations/{c.bridge.name}-{os_runner(c).name}"
                + f"-{response_type.name()}{per_axle_str}"
                + f"-load-{mv_load.str_id()}")).lower() + ".mp4")


def make_vehicle_plots(c: Config):
    """Plot vehicle information based on Config.vehicle_density."""
    plot_density(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-density"))
    plot_length_vs_axles(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-length-vs-axles"))
    plot_length_vs_weight(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-length-vs-weight"))
    plot_weight_vs_axles(c, save=c.image_path(
        f"vehicles/{c.bridge.name}-weight-vs-axles"))


# def make_threshold_plots(c: Config):
#     """Plot threshold information."""
#     for response_type in [ResponseType.YTranslation]:
#         plot_normal_threshold_distribution(
#             c, response_type, os_runner(c), at=Point(x=c.bridge.x(0.4)),
#             num_loads=100, num_thresholds=1000)


def make_event_plots_from_normal_mv_loads(c: Config):
    """Make plots of events from a moving load."""
    for fem_runner in [os_runner(c)]:
        for response_type in ResponseType:
            for num_loads in [5]:
                for x_frac in np.linspace(0, 1, num=10):
                    plot_events_from_normal_mv_loads(
                        c=c, response_type=response_type,
                        fem_runner=os_runner(c),
                        at=Point(x=c.bridge.x(x_frac)), rows=4,
                        loads_per_row=num_loads, save=(
                            c.image_path(pstr(
                                f"events/{fem_runner.name}"
                                + f"-rt-{response_type.name()}"
                                + f"-numloads-{num_loads}"
                                + f"-at-{x_frac:.2f}"))))


def make_all(c: Config, clean = True):
    """Make all plots for the thesis."""
    if clean:
        clean_generated(c)
    # make_bridge_plots(c)
    make_il_plots(c)
    # make_dc_plots(c)
    # make_normal_mv_load_animations(c)
    # make_normal_mv_load_animations(c, per_axle=True)
    # make_vehicle_plots(c)
    # make_event_plots_from_normal_mv_loads(c)


if __name__ == "__main__":
    make_all(bridge_705_config(), clean=True)
