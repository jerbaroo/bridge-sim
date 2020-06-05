"""Make all plots for the thesis.

These function provide data to functions in '/plot'.

"""
from typing import List, Optional

import bridge_sim.run
import bridge_sim.sim.responses
import bridge_sim.sim.run
import bridge_sim.sim.run.unit
from classify.scenario.traffic import heavy_traffic_1, normal_traffic
from config import Config
from fem.run.opensees import OSRunner
from plot import (
    plot_bridge_deck_side,
    plot_bridge_first_section,
    plt,
)
from model.bridge import Point
from model.load import MvVehicle
from model.response import ResponseType
from bridge_sim.util import print_i, safe_str
from vehicles.sample import sample_vehicle
from vehicles.stats import vehicle_data_noise_stats, vehicle_density_stats

from make.plot import contour

from make.data import simulations

# Print debug information for this file.
D: str = "make.make_plots"
# D: bool = False


def make_stats(c: Config):
    """Make all textual information for the thesis."""
    print_i("\n\n" + vehicle_density_stats(c) + "\n")
    print_i("\n\n" + vehicle_data_noise_stats(c) + "\n")


def make_bridge_plots(c: Config, mv_vehicles: Optional[List[List[MvVehicle]]] = None):
    """Make plots of the bridge with and without vehicles."""
    if mv_vehicles is None:
        mk = lambda x_frac, lane: MvVehicle(
            kn=0,
            axle_distances=[2.5, 1.5],
            axle_width=0,
            kmph=0,
            lane=lane,
            init_x_frac=x_frac,
        )
        mv_vehicles = [[], [mk(0.6, 0)], [mk(0.6, 0), mk(0.5, 0), mk(0.4, 1)]]
    plt.close()
    plot_bridge_first_section(
        bridge=c.bridge, save=c.image_path("bridges/bridge-section")
    )
    for mv_vehicles_ in mv_vehicles:
        mv_vehicles_str = "-".join(str(l).replace(".", ",") for l in mv_vehicles_)
        plot_bridge_deck_side(
            c.bridge,
            mv_vehicles=mv_vehicles_,
            save=c.image_path(f"bridges/side-{mv_vehicles_str}"),
        )
        plot_bridge_deck_top(
            c.bridge,
            mv_vehicles=mv_vehicles_,
            save=c.image_path(f"bridges/top-{mv_vehicles_str}"),
        )


def make_normal_mv_load_animations(c: Config, per_axle: bool = False):
    """Make animations of a pload moving across a bridge."""
    plt.close()
    mv_load = MovingLoad.from_vehicle(x_frac=0, vehicle=sample_vehicle(c), lane=0)
    per_axle_str = f"-peraxle" if per_axle else ""
    for response_type in ResponseType:
        animate_mv_load(
            c,
            mv_load,
            response_type,
            OSRunner(c),
            per_axle=per_axle,
            save=safe_str(
                c.image_path(
                    f"animations/{c.bridge.name}-{OSRunner(c).name}"
                    + f"-{response_type.name()}{per_axle_str}"
                    + f"-load-{mv_load.str_id()}"
                )
            ).lower()
            + ".mp4",
        )


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
            heavy_traffic_1(c=c, lam=lam, min_d=min_d, prob_heavy=0.01),
        ]:

            # Generate traffic under a scenario.
            traffic, start_index = traffic_scenario.traffic(
                bridge=c.bridge, max_time=max_time, time_step=time_step
            )
            traffic = traffic[start_index:]

            # Plot events from traffic.
            plot_events_from_traffic(
                c=c,
                bridge=c.bridge,
                bridge_scenario=bridge_scenario,
                traffic_name=traffic_scenario.name,
                traffic=traffic,
                start_time=start_index * time_step,
                time_step=time_step,
                response_type=ResponseType.YTranslation,
                points=points,
                fem_runner=OSRunner(c),
                save=c.get_image_path(
                    "events",
                    safe_str(
                        f"bs-{bridge_scenario.name}-ts-{traffic_scenario.name}"
                        f"-rt-{response_type.name()}"
                    ),
                ),
            )


def make_all_2d(c: Config):
    """Make all plots for a 2D bridge for the thesis."""
    make_contour_plots_for_verification(
        c, y=-0.5, response_types=[ResponseType.Stress, ResponseType.Strain]
    )
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
        kn=100 * length,
        axle_distances=[length],
        axle_width=2,
        kmph=40,
        lane=lane,
        init_x_frac=init_x_frac,
    )
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


def make_all_3d(c: Config):
    """Make all plots for a 3D bridge for the thesis."""
    # make_event_plots(c)

    ###################
    ##### Objects #####
    ###################
    # make_geom_plots(c)
    # vehicles.vehicle_plots(c)

    ######################
    ##### Simulation #####
    ######################
    bridge_sim.sim.run.unit.run_uls(c)
    # verification.make_convergence_data(c, run=True, plot=True)

    ########################
    ##### Verification #####
    ########################
    # verification.sensor_subplots(c)
    # contour.comparison_plots_705(c)
    # verification.plot_convergence(c)
    # verification.r2_plots(c)

    ###############################
    ##### System verification #####
    ###############################
    # sys_verification.plot_pier_displacement(c)

    ########################
    ##### Distribution #####
    ########################
    # make_distribution_plots(c)
    # distribution.distribution_plots(c)
    # distribution.deck_distribution_plots(c)

    ####################
    ##### Scenario #####
    ####################
    # contour.plot_of_unit_loads(c)
    # make_il_plots(c)
    # matrix.dc_plots(c)
    contour.plots_of_pier_displacement(c)
    # contour.gradient_pier_displacement_plots(c)

    #####################
    ##### Animation #####
    #####################
    # animate.traffic(c)
