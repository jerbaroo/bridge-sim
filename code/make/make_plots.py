"""Make all plots for the thesis."""
import os
from typing import List, Optional

import numpy as np

from config import Config
from fem.params import FEMParams
from fem.responses import load_fem_responses
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import OSRunner
from plot import animate_mv_load, plot_bridge_deck_side, plot_bridge_deck_top, plot_bridge_first_section, plt
from plot.bridge import plot_cloud_of_nodes
from plot.features import plot_events_from_normal_mv_loads
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il
from plot.responses import plot_contour_deck
from plot.vehicles import plot_density, plot_length_vs_axles, plot_length_vs_weight, plot_weight_vs_axles
from plot.verification import plot_convergence_with_shell_size
from model.bridge import Point
from model.load import Load, MovingLoad
from model.response import ResponseType
from util import print_d, pstr
from vehicles.sample import sample_vehicle

# Print debug information for this file.
D: str = "make.make_plots"
# D: bool = False


def make_bridge_plots(
        c: Config, loads: List[List[Load]]=[
            [],
            [Load(0.4, 500)],
            [Load(0.6, 200, axle_distances=[2, 1.5]),
             Load(0.5, 200, axle_distances=[2, 1.5]),
             Load(0.6, 200, axle_distances=[2, 1.5], lane=1)]]):
    """Make plots of the bridge with and without load."""
    plt.close()
    plot_bridge_first_section(
        bridge=c.bridge, save=c.image_path("bridges/bridge-section"))
    for loads_ in loads:
        load_str = "-".join(str(l).replace(".", ",") for l in loads_)
        plot_bridge_deck_side(
            c.bridge, loads=loads_,
            save=c.image_path(f"bridges/side-{load_str}"))
        plot_bridge_deck_top(
            c.bridge, loads=loads_,
            save=c.image_path(f"bridges/top-{load_str}"))


def make_il_plots(
        c: Config, num_subplot_ils: int = 10, num_imshow_ils: int = 100,
        num_loads: int = 100, fem_runner: Optional[FEMRunner] = None):
    """Make plots of the influence lines.

    Args:
        num_subplot_ils: int, the number of influence lines on the subplots.
        num_imshow_ils: int, the number of influence lines on the imshow plot.
        num_loads: int, the number of loading positions on x-axis to plot.

    """
    plt.close()
    original_num_ils = c.il_num_loads
    c.il_num_loads = num_loads
    if fem_runner is None:
        fem_runner = OSRunner(c)
    for response_type in fem_runner.supported_response_types(c.bridge):
        for interp_sim in [False]:
            for interp_response in [False]:
                interp_sim_str = "-interp-sim" if interp_sim else ""
                interp_response_str = (
                    "-interp-response" if interp_response else "")

                # Make the influence line imshow matrix.
                il_matrix = ILMatrix.load(
                    c=c, response_type=response_type, fem_runner=fem_runner)
                imshow_il(
                    c=c, il_matrix=il_matrix, num_ils=num_imshow_ils,
                    num_x=num_loads, interp_sim=interp_sim,
                    interp_response=interp_response, save=c.image_path(
                        f"ils/il-imshow-{il_matrix.fem_runner.name}"
                        + f"-{response_type.name()}"
                        + f"-{c.il_num_loads}-{num_loads}" + interp_sim_str
                        + interp_response_str))

                # Make the matrix of influence lines.

                # A plotting function with interpolation arguments filled in.
                def plot_func(
                        c=None, resp_matrix=None, expt_index=None,
                        response_frac=None, num_x=None):
                    return plot_il(
                        c=c, resp_matrix=resp_matrix, expt_index=expt_index,
                        response_frac=response_frac, num_x=num_x,
                        interp_sim=interp_sim, interp_response=interp_response)

                matrix_subplots(
                    c=c, resp_matrix=il_matrix, num_subplots=num_subplot_ils,
                    num_x=num_loads, plot_func=plot_func, save=c.image_path(
                        f"ils/il-subplots-{il_matrix.fem_runner.name}"
                        + f"-{response_type.name()}"
                        + f"-numexpts-{il_matrix.num_expts}"
                        + interp_sim_str + interp_response_str))
    c.il_num_loads = original_num_ils


def make_dc_plots(
        c: Config, num_subplot_ils: int = 10, num_imshow_ils: int = 100,
        num_loads: int = 100):
    """Make plots of the displacement control responses.

    Args:
        num_subplot_ils: int, the number of influence lines on the subplots.
        num_imshow_ils: int, the number of influence lines on the imshow plot.
        num_loads: int, the number of loading positions on x-axis to plot.

    """
    plt.close()
    num_dcs = len(c.bridge.supports)
    original_num_ils = c.il_num_loads
    c.il_num_loads = num_ils
    for response_type in ResponseType:
        for interp_sim in [False]:
            for interp_response in [False]:
                interp_sim_str = "-interp-sim" if interp_sim else ""
                interp_response_str = (
                    "-interp-response" if interp_response else "")

                # Make the influence line imshow matrix.
                dc_matrix = DCMatrix.load(
                    c=c, response_type=response_type, fem_runner=OSRunner(c))
                imshow_il(
                    c, il_matrix=dc_matrix, num_ils=num_dcs, num_x=num_x,
                    interp_sim=interp_sim, interp_response=interp_response,
                    save=c.image_path(
                        f"dcs/dc-imshow-{dc_matrix.fem_runner.name}"
                        + f"-{response_type.name()}"
                        + f"-{num_dcs}-{num_x}" + interp_sim_str
                        + interp_response_str))

                # Make the matrix of influence lines.

                # A plotting function with interpolation arguments filled in.
                def plot_func(
                        c=None, resp_matrix=None, expt_index=None,
                        response_frac=None, num_x=None):
                    return plot_dc(
                        c=c, resp_matrix=resp_matrix, expt_index=expt_index,
                        response_frac=response_frac, num_x=num_x,
                        interp_sim=interp_sim, interp_response=interp_response)

                matrix_subplots(
                    c=c, resp_matrix=dc_matrix, num_x=num_x,
                    plot_func=plot_func, save=c.image_path(
                        f"dcs/dc-subplots-{dc_matrix.fem_runner.name}"
                        + f"-{response_type.name()}"
                        + f"-numexpts-{dc_matrix.num_expts}"
                        + interp_sim_str + interp_response_str))
    c.il_num_loads = original_num_ils


def make_normal_mv_load_animations(c: Config, per_axle: bool = False):
    """Make animations of a load moving across a bridge."""
    plt.close()
    mv_load = MovingLoad.from_vehicle(
        x_frac=0, vehicle=sample_vehicle(c), lane=0)
    per_axle_str = f"-peraxle" if per_axle else ""
    for response_type in ResponseType:
        animate_mv_load(
            c, mv_load, response_type, OSRunner(c), per_axle=per_axle,
            save=pstr(c.image_path(
                f"animations/{c.bridge.name}-{OSRunner(c).name}"
                + f"-{response_type.name()}{per_axle_str}"
                + f"-load-{mv_load.str_id()}")).lower() + ".mp4")


def make_vehicle_plots(c: Config):
    plt.close()
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
#             c, response_type, OSRunner(c), at=Point(x=c.bridge.x(0.4)),
#             num_loads=100, num_thresholds=1000)


def make_event_plots_from_normal_mv_loads(c: Config):
    """Make plots of events from a moving load."""
    for fem_runner in [OSRunner(c)]:
        for response_type in ResponseType:
            for num_loads in [5]:
                for x_frac in np.linspace(0, 1, num=10):
                    plot_events_from_normal_mv_loads(
                        c=c, response_type=response_type,
                        fem_runner=OSRunner(c),
                        at=Point(x=c.bridge.x(x_frac)), rows=4,
                        loads_per_row=num_loads, save=(
                            c.image_path(pstr(
                                f"events/{fem_runner.name}"
                                + f"-rt-{response_type.name()}"
                                + f"-numloads-{num_loads}"
                                + f"-at-{x_frac:.2f}"))))


def make_contour_plots(
        c: Config, response_types: List[ResponseType], y: float):
    """Make contour plots for given response types at a fixed y position."""
    fem_runner = OSRunner(c)
    load_x = 35 / 102.75
    load_kn = 100
    load = Load(load_x, load_kn)
    load.z_frac = 25 / 33.2
    for response_type in response_types:
        print_d(D, f"response_types = {response_types}")
        fem_params = FEMParams(loads=[load], response_types=response_types)
        print_d(D, f"loading response type = {response_type}")
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=fem_runner)
        plot_contour_deck(
            c=c, fem_responses=fem_responses, y=y, loads=[load], save=(
            c.image_path(pstr(
                f"contour-{response_type.name()}-load-{load_x}-{load_kn}"))))


def make_all_2d(c: Config):
    """Make all plots for a 2D bridge for the thesis."""
    make_contour_plots(c, response_types=list(ResponseType), y=-0.5)
    make_bridge_plots(c)
    make_il_plots(c)
    # make_dc_plots(c)
    # make_normal_mv_load_animations(c)
    # make_normal_mv_load_animations(c, per_axle=True)
    # make_vehicle_plots(c)
    # make_event_plots_from_normal_mv_loads(c)


def make_all_3d(c: Config):
    """Make all plots for a 3D bridge for the thesis."""
    # plot_convergence_with_shell_size(
    #     max_shell_areas=list(np.linspace(0.5, 0.8, 10)))
    make_contour_plots(
        c=c, y=0, response_types=[ResponseType.YTranslation,
            ResponseType.ZTranslation, ResponseType.XTranslation])
    cloud_of_nodes_dir = os.path.join(c.images_dir, "cloud-of-points")
    if not os.path.exists(cloud_of_nodes_dir):
        os.makedirs(cloud_of_nodes_dir)
    plot_cloud_of_nodes(
        c=c, save=os.path.join(cloud_of_nodes_dir, "cloud-full-axis"))
    plot_cloud_of_nodes(
        c=c, equal_axis=True,
        save=os.path.join(cloud_of_nodes_dir, "cloud-equal-axis"))
