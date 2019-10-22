"""Make all plots for the thesis.

These function provide data to functions in '/plot'.

"""
import os
from itertools import chain
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
    plot_bridge_first_section, plt
from plot.geom import plot_cloud_of_nodes
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il
from plot.responses import plot_contour_deck
from plot.vehicles import plot_density, plot_length_vs_axles,\
    plot_length_vs_weight, plot_weight_vs_axles
from model.bridge import Dimensions, Point
from model.load import PointLoad, MvVehicle
from model.response import ResponseType
from util import print_d, print_i, pstr
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


def make_contour_plots(c: Config, y: float, response_types: List[ResponseType]):
    """Make contour plots for given response types at a fixed y position."""
    fem_runner = OSRunner(c)
    lane_zs = sorted(
        chain.from_iterable([l.z_min, l.z_max] for l in c.bridge.lanes))
    for response_type in response_types:
        for load_x, load_z in [
                # (41.677, 1.8687), (35.011, 25.032 - 16.6),
                # (2.46273, 0.6 - 16.6)]:
                # (55.732, 15.479 - 16.6)]:
                # (35.011, 25.032 - 16.6)]:
                (35.011, lane_zs[-1]), (c.bridge.length / 2, 0),
                (c.bridge.x(0.9), lane_zs[1]), (c.bridge.x(0.99), lane_zs[0])]:
            print_i(f"Contour plot at x, z, = {load_x}, {load_z}")
            pload = PointLoad(
                x_frac=c.bridge.x_frac(load_x), z_frac=c.bridge.z_frac(load_z),
                kn=100)
            print_d(D, f"response_types = {response_types}")
            fem_params = FEMParams(
                ploads=[pload], response_types=response_types)
            print_d(D, f"loading response type = {response_type}")
            fem_responses = load_fem_responses(
                c=c, fem_params=fem_params, response_type=response_type,
                fem_runner=fem_runner)
            plot_contour_deck(
                c=c, fem_responses=fem_responses, y=y, ploads=[pload], save=(
                c.image_path(pstr(
                    f"contour-{response_type.name()}-ploadx={load_x}"
                    + f"-ploadz={load_z}"))))


def make_cloud_of_nodes_plots(c: Config):
    """Make all variations of the cloud of nodes plots."""
    # Create the directory if not exists.
    cloud_of_nodes_dir = os.path.join(c.images_dir, "cloud-of-points")
    if not os.path.exists(cloud_of_nodes_dir):
        os.makedirs(cloud_of_nodes_dir)

    def both_axis_plots(prop: str, *args, **kwargs):
        """Make cloud of nodes plots for full and equal axes."""
        # Cloud of nodes without axis correction.
        plot_cloud_of_nodes(
            *args, **kwargs, c=c,
            save=os.path.join(cloud_of_nodes_dir, f"cloud{prop}-full-axis"))

        # Cloud of nodes with equal axes.
        plot_cloud_of_nodes(
            *args, **kwargs, c=c, equal_axis=True,
            save=os.path.join(cloud_of_nodes_dir, f"cloud{prop}-equal-axis"))

    def all_plots(prop: str, *args, **kwargs):
        """Make both axis plots for all deck and pier variants."""
        both_axis_plots(prop, *args, deck=True, piers=True, **kwargs)
        both_axis_plots(prop, *args, deck=True, piers=False, **kwargs)
        both_axis_plots(prop, *args, deck=False, piers=True, **kwargs)

    # Standard plots.
    all_plots("")

    # Standard plots.
    all_plots("-density", node_prop=lambda n: n.section.density)


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


def make_geom_plots(c: Config):
    """Make plots of the geometry (with some vehicles) of each bridge."""
    from plot.geom import top_view_bridge
    from plot.load import top_view_vehicles

    # First create some vehicles.
    mk = lambda init_x_frac, lane, length: MvVehicle(
        kn=100 * length, axle_distances=[length], axle_width=2, kmph=40,
        lane=lane, init_x_frac=init_x_frac)
    mv_vehicles = [[], [mk(0.1, 0, 2.5), mk(0.4, 0, 4), mk(0, 1, 7)]]

    # Create a plot for each set of vehicles.
    for i, set_mv_vehicles in enumerate(mv_vehicles):
        # First the top view.
        plt.close()
        top_view_bridge(c.bridge)
        top_view_vehicles(bridge=c.bridge, mv_vehicles=set_mv_vehicles, time=2)
        plt.savefig(c.get_image_path("geom", f"top-view-{i + 1}"))

        # Then the side view.
        plt.close()
        # top_view_bridge(c.bridge)
        # top_view_vehicles(bridge=bridge)
        # plt.savefig(c.get_image_path("geom", f"top-view-{i + 1}"))


def make_traffic_animations(c: Config):
    """Make animations of different traffic scenarios."""
    from plot.animate.traffic import animate_traffic_top_view

    max_time, time_step, lam = 5, 0.01, 10
    for traffic_scenario in [normal_traffic(c=c, lam=lam)]:
        traffic = traffic_scenario.traffic(
            bridge=c.bridge, max_time=max_time, time_step=time_step,
            after_warm_up=False)
        animate_traffic_top_view(
            bridge=c.bridge,
            title=f"{traffic_scenario.name} on {c.bridge.name}",
            traffic=traffic, time_step=time_step, save=c.get_image_path(
                "animations", f"{traffic_scenario.name}.mp4"))


def make_all_3d(c: Config):
    """Make all plots for a 3D bridge for the thesis."""
    # plot_convergence_with_shell_size(
    #     max_shell_areas=list(np.linspace(0.5, 0.8, 10)))
    # make_il_plots(c)
    # make_geom_plots(c)
    make_traffic_animations(c)
    # make_cloud_of_nodes_plots(c)
    # make_contour_plots(c=c, y=0, response_types=[ResponseType.YTranslation])
    # make_event_plots_from_normal_mv_loads(c)
