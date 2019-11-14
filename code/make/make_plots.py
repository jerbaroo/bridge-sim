"""Make all plots for the thesis.

These function provide data to functions in '/plot'.

"""
import os
from itertools import chain
from typing import List, Optional

import numpy as np

from classify.scenario.bridge import HealthyBridge
from classify.scenario.traffic import heavy_traffic_1, normal_traffic
from classify.data.responses import responses_to_traffic
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import OSRunner
from plot import animate_mv_vehicle, plot_bridge_deck_side,\
    plot_bridge_first_section, plt
from plot.geom import plot_cloud_of_nodes
from model.bridge import Dimensions, Point
from model.bridge.util import wheel_tracks
from model.load import PointLoad, MvVehicle
from model.response import ResponseType
from util import print_d, print_i, safe_str
from vehicles.sample import sample_vehicle

from make.plot import animate, contour, matrix, vehicle, verification

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


def make_normal_mv_load_animations(c: Config, per_axle: bool = False):
    """Make animations of a pload moving across a bridge."""
    plt.close()
    mv_load = MovingLoad.from_vehicle(
        x_frac=0, vehicle=sample_vehicle(c), lane=0)
    per_axle_str = f"-peraxle" if per_axle else ""
    for response_type in ResponseType:
        animate_mv_load(
            c, mv_load, response_type, OSRunner(c), per_axle=per_axle,
            save=safe_str(c.image_path(
                f"animations/{c.bridge.name}-{OSRunner(c).name}"
                + f"-{response_type.name()}{per_axle_str}"
                + f"-load-{mv_load.str_id()}")).lower() + ".mp4")


def make_event_plots(c: Config):
    """Make plots of events in different scenarios."""
    from plot.features import plot_events_from_traffic

    fem_runner = OSRunner(c)
    bridge_scenario = BridgeScenarioNormal()
    max_time, time_step, lam, min_d = 20, 0.01, 5, 2
    c.time_step = time_step
    sensor_zs = [lane.z_center() for lane in c.bridge.lanes]
    points = [Point(x=35, y=0, z=z) for z in sensor_zs]

    for response_type in [ResponseType.YTranslation]:
        for traffic_scenario in [
                normal_traffic(c=c, lam=lam, min_d=min_d),
                heavy_traffic_1(c=c, lam=lam, min_d=min_d, prob_heavy=0.01)]:

            # Generate traffic under a scenario.
            traffic, start_index = traffic_scenario.traffic(
                bridge=c.bridge, max_time=max_time, time_step=time_step)
            traffic = traffic[start_index:]

            # Plot events from traffic.
            plot_events_from_traffic(
                c=c, bridge=c.bridge, bridge_scenario=bridge_scenario,
                traffic_name=traffic_scenario.name, traffic=traffic,
                start_time=start_index * time_step, time_step=time_step,
                response_type=ResponseType.YTranslation,
                points=points, fem_runner=OSRunner(c),save=c.get_image_path(
                "events", safe_str(
                    f"bs-{bridge_scenario.name}-ts-{traffic_scenario.name}"
                    f"-rt-{response_type.name()}")))


def make_cloud_of_nodes_plots(c: Config):
    """Make all variations of the cloud of nodes plots."""

    def both_axis_plots(prop: str, *args, **kwargs):
        """Make cloud of nodes plots for full and equal axes."""
        # Cloud of nodes without axis correction.
        plot_cloud_of_nodes(
            *args, **kwargs, c=c, equal_axis=False,
            save=c.get_image_path(f"cloud-of-nodes{prop}", "cloud"))

        # Cloud of nodes with equal axes.
        plot_cloud_of_nodes(
            *args, **kwargs, c=c, equal_axis=True,
            save=c.get_image_path(f"cloud-of-nodes{prop}-equal-axis", "cloud"))

    def all_plots(prop: str, *args, **kwargs):
        """Make both axis plots for all deck and pier variants."""
        both_axis_plots(prop, *args, deck=True, piers=False, **kwargs)
        both_axis_plots(prop, *args, deck=False, piers=True, **kwargs)
        both_axis_plots(prop, *args, deck=True, piers=True, **kwargs)

    # Plots of some node property.
    all_plots("-density", node_prop=lambda s: s.density)
    all_plots("-thickness", node_prop=lambda s: s.thickness)


def make_all_2d(c: Config):
    """Make all plots for a 2D bridge for the thesis."""
    make_contour_plots_for_verification(
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
        top_view_vehicles(
            bridge=c.bridge, mv_vehicles=set_mv_vehicles, time=2)
        plt.savefig(c.get_image_path("geom", f"top-view-{i + 1}"))

        # Then the side view.
        plt.close()
        # top_view_bridge(c.bridge)
        # top_view_vehicles(bridge=bridge)
        # plt.savefig(c.get_image_path("geom", f"top-view-{i + 1}"))


def make_distribution_plots(c: Config):
    max_time, time_step, lam, min_d = 20, 0.01, 5, 2
    points = [Point(x=35, y=0, z=8.4), Point(x=35, y=0, z=-8.4)]
    response_type = ResponseType.YTranslation

    # Generate heavy traffic.
    heavy_traffic, start_index = heavy_traffic_1(
        c=c, lam=lam, min_d=min_d, prob_heavy=0.01).traffic(
            bridge=c.bridge, max_time=max_time, time_step=time_step)

    # Filter out any normal traffic so it's just one heavy vehicle.
    for t, t_traffic in enumerate(heavy_traffic):
        heavy_traffic[t] = [v for v in t_traffic if v.kn == 500]
        assert len(heavy_traffic[t]) <= 1
        print(len(heavy_traffic[t]))
    assert any(len(t_traffic) == 1 for t_traffic in heavy_traffic)
    assert len(heavy_traffic[-1]) == 0

    heavy_responses = responses_to_traffic(
        c=c, traffic=heavy_traffic, bridge_scenario=BridgeScenarioNormal(),
        start_time=start_index * time_step, time_step=time_step,
        points=points, response_type=response_type, fem_runner=OSRunner(c))
    heavy_responses_values = [[
        r.responses[0][point.x][point.y][point.z]
        for r in heavy_responses] for point in points]

    # heavy_responses_values[0] = [r for r in heavy_responses_values[0] if r != 0]
    # heavy_responses_values[1] = [r for r in heavy_responses_values[1] if r != 0]

    print("first lane")
    [print(v) for v in heavy_responses_values[0] if v != 0]
    print("second lane")
    [print(v) for v in heavy_responses_values[1] if v != 0]

    plt.plot(heavy_responses_values[0])
    plt.show()
    plt.plot(heavy_responses_values[1])
    plt.show()


def make_all_3d(c: Config):
    """Make all plots for a 3D bridge for the thesis."""
    # contour.plot_of_unit_loads(c)
    # verification.make_convergence(c, run=True, plot=False)
    verification.plot_convergence(c)
    # make_geom_plots(c)
    # vehicle.vehicle_plots(c)
    # make_il_plots(c)
    # matrix.dc_plots(c)
    # make_event_plots(c)
    # animate.traffic(c)
    # make_distribution_plots(c)
    # make_cloud_of_nodes_plots(c)
    # contour.plots_for_verification(
    #     c=c, y=0, response_types=[ResponseType.YTranslation])
    # contour.plots_of_pier_displacement(
    #     c=c, y=0, response_types=[ResponseType.YTranslation])
