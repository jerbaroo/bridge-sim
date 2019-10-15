"""Make all plots for the thesis."""
import os
from typing import List, Optional

import numpy as np

from classify.data.scenarios import normal_traffic
from config import Config
from fem.params import FEMParams
from fem.responses import load_fem_responses
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import OSRunner
from plot import animate_mv_vehicle, plot_bridge_deck_side,\
    plot_bridge_deck_top, plot_bridge_first_section, plt
from plot.bridge import plot_cloud_of_nodes
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il
from plot.responses import plot_contour_deck
from plot.vehicles import plot_density, plot_length_vs_axles,\
    plot_length_vs_weight, plot_weight_vs_axles
from model.bridge import Dimensions, Point
from model.load import PointLoad, MvVehicle
from model.response import ResponseType
from util import print_d, pstr
from vehicles.sample import sample_vehicle

# Print debug information for this file.
D: str = "make.make_plots"
# D: bool = False


def make_bridge_plots(
        c: Config, mv_vehicles: Optional[List[List[MvVehicle]]]=None):
    """Make plots of the bridge with and without vehicles."""
    if mv_vehicles is None:
        mk = lambda x_frac, lane: MvVehicle(
            kn=0, axle_distances=[2.5, 1.5], axle_width=0, kmph=0, lane=lane,
            init_x_frac=x_frac)
        mv_vehicles = [
            [],
            [mk(0.6, 0)],
            [mk(0.6, 0), mk(0.5, 0), mk(0.4, 1)]]
    plt.close()
    plot_bridge_first_section(
        bridge=c.bridge, save=c.image_path("bridges/bridge-section"))
    for mv_vehicles_ in mv_vehicles:
        mv_vehicles_str = "-".join(str(l).replace(".", ",") for l in mv_vehicles_)
        plot_bridge_deck_side(
            c.bridge, mv_vehicles=mv_vehicles_,
            save=c.image_path(f"bridges/side-{mv_vehicles_str}"))
        plot_bridge_deck_top(
            c.bridge, mv_vehicles=mv_vehicles_,
            save=c.image_path(f"bridges/top-{mv_vehicles_str}"))


def make_il_plots(
        c: Config, num_subplot_ils: int = 10, num_imshow_ils: int = 100,
        num_ploads: int = 100, fem_runner: Optional[FEMRunner] = None):
    """Make plots of the influence lines.

    Args:
        c: Config, global configuration object.
        num_subplot_ils: int, the number of influence lines on the subplots.
        num_imshow_ils: int, the number of influence lines on the imshow plot.
        num_ploads: int, the number of loading positions on x-axis to plot.
        fem_runner: Optional[FEMRunner], FEM program to run simulations with,
            defaults to OpenSees.

    """
    plt.close()
    original_num_ils = c.il_num_loads
    c.il_num_loads = num_ploads
    if fem_runner is None:
        fem_runner = OSRunner(c)

    pload_z_fracs = []
    # If a 3D FEM of a bridge then generate IL plots for each wheel track.
    if c.bridge.dimensions == Dimensions.D3:
        # A moving vehicle for each bridge lane.
        mv_vehicles = [
            next(normal_traffic(c).mv_vehicles(lane=lane))
            for lane in range(len(c.bridge.lanes))]
        # From the moving vehicles we can calculate wheel tracks on the bridge.
        for mv_vehicle in mv_vehicles:
            for wheel_z_frac in mv_vehicle.wheel_tracks(
                    bridge=c.bridge, meters=False):
                pload_z_fracs.append(wheel_z_frac)
    print_d(D, "make_il_plots: pload_z_fracs = {pload_z_fracs}")

    for pload_z_frac in pload_z_fracs:
        for response_type in fem_runner.supported_response_types(c.bridge):
            # TODO: Remove once Stress and Strain are fixed.
            if c.bridge.dimensions == Dimensions.D3 and response_type in [
                    ResponseType.Stress, ResponseType.Strain]:
                continue
            for interp_sim in [False]:
                for interp_response in [False]:
                    interp_sim_str = "-interp-sim" if interp_sim else ""
                    interp_response_str = (
                        "-interp-response" if interp_response else "")

                    # Make the influence line imshow matrix.
                    il_matrix = ILMatrix.load(
                        c=c, response_type=response_type, fem_runner=fem_runner,
                        load_z_frac=pload_z_frac)
                    imshow_il(
                        c=c, il_matrix=il_matrix, num_ils=num_imshow_ils,
                        num_x=num_ploads, interp_sim=interp_sim,
                        title_append=f" z = {c.bridge.z(pload_z_frac)}",
                        interp_response=interp_response, save=c.image_path(pstr(
                            f"ils/il-imshow-{il_matrix.fem_runner.name}"
                            + f"-loadzfrac={pload_z_frac}"
                            + f"-{response_type.name()}"
                            + f"-{c.il_num_loads}-{num_ploads}"
                            + interp_sim_str + interp_response_str)))

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
                        num_x=num_ploads, plot_func=plot_func, save=c.image_path(
                            f"ils/il-subplots-{il_matrix.fem_runner.name}"
                            + f"-{response_type.name()}"
                            + f"-numexpts-{il_matrix.num_expts}"
                            + interp_sim_str + interp_response_str))
    c.il_num_loads = original_num_ils


def make_dc_plots(
        c: Config, num_subplot_ils: int = 10, num_imshow_ils: int = 100,
        num_ploads: int = 100):
    """Make plots of the displacement control responses.

    Args:
        num_subplot_ils: int, the number of influence lines on the subplots.
        num_imshow_ils: int, the number of influence lines on the imshow plot.
        num_ploads: int, the number of loading positions on x-axis to plot.

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
    """Make animations of a pload moving across a bridge."""
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

def make_contour_plot(
        c: Config, y: float, fem_runner: FEMRunner,
        response_types: List[ResponseType], response_type: ResponseType,
        load_x: float, load_z: float, load_kn: float=100):
    load_x_frac = c.bridge.x_frac(load_x)
    load_z_frac = c.bridge.z_frac(load_z)
    pload = PointLoad(x_frac=load_x_frac, z_frac=load_z_frac, kn=load_kn)
    print_d(D, f"response_types = {response_types}")
    fem_params = FEMParams(ploads=[pload], response_types=response_types)
    print_d(D, f"loading response type = {response_type}")
    fem_responses = load_fem_responses(
        c=c, fem_params=fem_params, response_type=response_type,
        fem_runner=fem_runner)
    plot_contour_deck(
        c=c, fem_responses=fem_responses, y=y, ploads=[pload], save=(
        c.image_path(pstr(
            f"contour-{response_type.name()}-ploadxfrac={load_x}-"
            + f"-ploadzfrac={load_z}-ploadkn={load_kn}"))))


def make_contour_plots(c: Config, y: float, response_types: List[ResponseType]):
    """Make contour plots for given response types at a fixed y position."""
    fem_runner = OSRunner(c)
    for response_type in response_types:
        for load_x in [35, c.bridge.length / 2, 100]:
            for load_z in [-5, 0, 8.4]:
                make_contour_plot(
                    c=c, y=y, fem_runner=fem_runner,
                    response_types=response_types, response_type=response_type,
                    load_x=load_x, load_z=load_z)


def make_all_2d(c: Config):
    """Make all plots for a 2D bridge for the thesis."""
    make_contour_plots(
        c, y=-0.5, response_types=[ResponseType.Stress, ResponseType.Strain])
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
    import sys; sys.exit();
    make_il_plots(c)
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
