from copy import deepcopy

import matplotlib as mpl
import numpy as np

from classify.data.responses.convert import loads_to_traffic_array
from classify.data.responses import (
    responses_to_traffic_array,
    responses_to_vehicles_d,
)
from classify.vehicle import wagen1
from classify.scenarios import healthy_scenario
from classify.scenario.bridge import transverse_crack
from config import Config
from fem.build import BuildContext
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.responses.matrix.il import ILMatrix
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.bridge import Point
from model.load import MvVehicle, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import flatten, print_i, safe_str

uni_axle_vehicle = MvVehicle(
    kn=wagen1.total_kn(),
    axle_distances=[],
    axle_width=2.5,
    kmph=wagen1.kmph,
    lane=0,
    init_x_frac=0,
)

bi_axle_vehicle = MvVehicle(
    kn=wagen1.total_kn(),
    axle_distances=[2],
    axle_width=2.5,
    kmph=wagen1.kmph,
    lane=0,
    init_x_frac=0,
)


def mesh_refinement(c: Config, build: bool, plot: bool):
    """Generate TCL files for debugging mesh refinement."""
    response_type = ResponseType.YTranslation
    min_config = deepcopy(c)
    min_config.bridge.type = "debugging"
    # min_config.bridge.base_mesh_deck_max_x = 100
    # min_config.bridge.base_mesh_deck_max_z = 100
    # min_config.bridge.base_mesh_pier_max_long = 10
    pload = PointLoad(x_frac=0.5, z_frac=0.5, kn=100)

    def build_with_refinement(refinement_radii):
        sim_params = SimParams(
            response_types=[response_type],
            ploads=[pload],
            refinement_radii=refinement_radii,
        )
        # Build and save the model file.
        if build:
            build_model_3d(
                c=min_config,
                expt_params=ExptParams([sim_params]),
                os_runner=OSRunner(min_config),
            )
        # Load and plot responses.
        if plot:
            sim_responses = load_fem_responses(
                c=min_config,
                sim_runner=OSRunner(min_config),
                response_type=response_type,
                sim_params=sim_params,
                run=True,
            )
            for scatter in [True, False]:
                top_view_bridge(
                    min_config.bridge, abutments=True, piers=True, lanes=True
                )
                plot_contour_deck(
                    c=min_config, responses=sim_responses, scatter=scatter, levels=100,
                )
                plt.title(f"{refinement_radii}")
                plt.savefig(
                    min_config.get_image_path(
                        "debugging",
                        safe_str(
                            f"{response_type.name()}-{refinement_radii}-scatter-{scatter}"
                        )
                        + ".pdf",
                    )
                )
                plt.close()

    build_with_refinement([])
    build_with_refinement([10])


def compare_axles(c: Config):
    """Compare responses between uniaxle vehicle and Truck 1."""
    assert c.il_num_loads == 600

    point = Point(x=c.bridge.x_max / 2, y=0, z=-8.4)
    end_time = wagen1.time_left_bridge(bridge=c.bridge)
    num_times = int(end_time / c.sensor_hz)
    wagen1_times = np.linspace(0, end_time, num_times)
    plt.portrait()

    wagen1_loads = [
        flatten(wagen1.to_wheel_track_loads(c=c, time=time), PointLoad)
        for time in wagen1_times
    ]
    responses_ulm = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=wagen1_loads),
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    )
    plt.subplot(3, 1, 1)
    plt.title(f"{num_times} responses with ULS = {c.il_num_loads} (Wagen 1 (4 axles))")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))

    bi_axle_loads = [
        flatten(bi_axle_vehicle.to_wheel_track_loads(c=c, time=time), PointLoad)
        for time in wagen1_times
    ]
    responses_ulm = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=bi_axle_loads),
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    )
    plt.subplot(3, 1, 2)
    plt.title(f"{num_times} responses with ULS = {c.il_num_loads} (2 axles)")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))

    uni_axle_loads = [
        flatten(uni_axle_vehicle.to_wheel_track_loads(c=c, time=time), PointLoad)
        for time in wagen1_times
    ]
    responses_ulm = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=uni_axle_loads),
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    )
    plt.subplot(3, 1, 3)
    plt.title(f"{num_times} responses with ULS = {c.il_num_loads} (1 axle)")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))

    plt.tight_layout()
    plt.savefig(c.get_image_path("system-verification", "compare-axles.pdf"))


def compare_responses(c: Config):
    """Compare responses to Truck 1, direct simulation and matmul."""
    assert c.il_num_loads == 600
    num_times = 50
    close_times = 200
    # Running time:
    # responses_to_vehicles_d: num_times * 8
    # responses_to_vehicles_d: 4 * il_num_loads
    # responses_to_loads_m: 0 (4 * il_num_loads)
    # responses_to_loads_m: 0 (4 * il_num_loads)
    # Wagen 1 from the experimental campaign.

    point = Point(x=c.bridge.x_max - (c.bridge.length / 2), y=0, z=-8.4)
    end_time = wagen1.time_left_bridge(bridge=c.bridge)
    wagen1_times = list(np.linspace(0, end_time, num_times))
    more_wagen1_times = list(
        np.linspace(
            wagen1.time_at(x=point.x - 2, bridge=c.bridge),
            wagen1.time_at(x=point.x + 2, bridge=c.bridge),
            close_times,
        )
    )
    wagen1_times = sorted(wagen1_times + more_wagen1_times)
    plt.portrait()

    # Start with responses from direct simulation.
    responses_not_binned = responses_to_vehicles_d(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[point],
        mv_vehicles=[wagen1],
        times=wagen1_times,
        sim_runner=OSRunner(c),
        binned=False,
    )
    plt.subplot(4, 1, 1)
    plt.title(f"{len(wagen1_times)} responses")
    plt.plot(wagen1_times, responses_not_binned)

    # Then responses from direct simulation with binning.
    c.shorten_paths = True
    responses_binned = responses_to_vehicles_d(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[point],
        mv_vehicles=[wagen1],
        times=wagen1_times,
        sim_runner=OSRunner(c),
        binned=True,
    )
    c.shorten_paths = False
    plt.subplot(4, 1, 2)
    plt.title(f"{len(wagen1_times)} responses (binned)")
    plt.plot(wagen1_times, responses_binned)
    xlim = plt.xlim()

    num_times = int(end_time / c.sensor_hz)
    wagen1_times = np.linspace(0, end_time, num_times)

    # Then from 'TrafficArray' we get responses, without binning.
    wagen1_loads = [
        flatten(wagen1.to_point_load_pw(time=time, bridge=c.bridge), PointLoad)
        for time in wagen1_times
    ]
    responses_ulm = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=wagen1_loads),
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    )
    plt.subplot(4, 1, 3)
    plt.title(f"{num_times} responses with ULS = {c.il_num_loads} traffic_array")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))
    plt.xlim(xlim)

    # # Then from 'TrafficArray' we get responses, with binning.
    wagen1_loads = [
        flatten(wagen1.to_wheel_track_loads(c=c, time=time), PointLoad)
        for time in wagen1_times
    ]
    responses_ulm_binned = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=wagen1_loads),
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    )
    plt.subplot(4, 1, 4)
    plt.title(
        f"{num_times} responses from {c.il_num_loads} il_num_loads\ntraffic_array binned"
    )
    plt.plot(wagen1_times, np.array(responses_ulm_binned).reshape(-1, 1))
    plt.xlim(xlim)

    plt.tight_layout()
    plt.savefig(c.get_image_path("system-verification", "compare-time-series.pdf"))


def compare_load_positions(c: Config):
    """Compare load positions (normal vs. buckets)."""
    c.il_num_loads = 10
    num_times = 1000

    # Wagen 1 from the experimental campaign.
    point = Point(x=c.bridge.x_max / 2, y=0, z=-8.4)
    end_time = uni_axle_vehicle.time_left_bridge(bridge=c.bridge)
    vehicle_times = list(np.linspace(0, end_time, num_times))
    plt.portrait()

    pw_loads = [
        flatten(
            uni_axle_vehicle.to_point_load_pw(time=time, bridge=c.bridge), PointLoad
        )
        for time in vehicle_times
    ]
    pw_load_xs = [
        [c.bridge.x(l.x_frac) for l in pw_loads[time_ind]]
        for time_ind in range(len(pw_loads))
    ]
    plt.subplot(3, 1, 1)
    # for l in pw_load_xs:
    #     print(l)
    plt.plot([l[0] for l in pw_load_xs])
    plt.plot([l[1] for l in pw_load_xs])

    wt_loads = [
        flatten(uni_axle_vehicle.to_wheel_track_loads(c=c, time=time), PointLoad)
        for time in vehicle_times
    ]
    wt_load_xs = [
        [c.bridge.x(l.x_frac) for l in wt_loads[time_ind]]
        for time_ind in range(len(wt_loads))
    ]
    plt.subplot(3, 1, 2)
    plt.scatter(vehicle_times, [l[0] for l in wt_load_xs], label="0")
    plt.scatter(vehicle_times, [l[1] for l in wt_load_xs], label="1")
    plt.legend()

    wt_load_kn = [
        [l.kn for l in wt_loads[time_ind]] for time_ind in range(len(wt_loads))
    ]
    plt.subplot(3, 1, 3)
    for l in wt_load_kn:
        print(l)
    plt.scatter(vehicle_times, [l[0] for l in wt_load_kn], label="0")
    plt.scatter(vehicle_times, [l[1] for l in wt_load_kn], label="1")
    plt.legend()

    plt.tight_layout()
    plt.savefig(c.get_image_path("verification", "compare-load-positions.pdf"))
    plt.close()


def uls_contour_plot(c: Config, x_i: int, z_i: int, response_type: ResponseType):
    wheel_xs = c.bridge.wheel_track_xs(c)
    wheel_x = wheel_xs[x_i]
    wheel_zs = c.bridge.wheel_track_zs(c)
    wheel_z = wheel_zs[z_i]
    print_i(f"Wheel (x, z) = ({wheel_x}, {wheel_z})")
    plt.landscape()
    plt.subplot(2, 1, 1)
    healthy = list(
        ILMatrix.load_wheel_track(
            c=c,
            response_type=response_type,
            fem_runner=OSRunner(c),
            load_z_frac=c.bridge.z_frac(wheel_z),
            run_only=False,
            indices=[x_i],
        )
    )[0].resize()
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=healthy, sci_format=True, decimals=6)
    plt.title("Healthy")
    c = transverse_crack().use(c)[0]
    cracked = list(
        ILMatrix.load_wheel_track(
            c=c,
            response_type=response_type,
            fem_runner=OSRunner(c),
            load_z_frac=c.bridge.z_frac(wheel_z),
            run_only=False,
            indices=[x_i],
        )
    )[0].resize()
    plt.subplot(2, 1, 2)
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=cracked, sci_format=True, decimals=6)
    plt.title("Cracked")
    plt.tight_layout()
    plt.savefig(
        c.get_image_path(
            "verification",
            safe_str(f"uls-contour-x-{wheel_x}-z-{wheel_z}-{response_type.name()}")
            + ".pdf",
        )
    )


def wagen_1_contour_plot(c: Config, x: int, response_type: ResponseType):
    original_c = c
    LOADS = False
    time = wagen1.time_at(x=x, bridge=c.bridge)
    loads = wagen1.to_wheel_track_loads(c=c, time=time, flat=True)
    healthy_responses = load_fem_responses(
        c=c,
        sim_params=SimParams(ploads=loads),
        response_type=response_type,
        sim_runner=OSRunner(c),
    )
    vmin, vmax = min(healthy_responses.values()), max(healthy_responses.values())
    c = transverse_crack().use(c)[0]
    crack_responses = load_fem_responses(
        c=c,
        sim_params=SimParams(ploads=loads),
        response_type=response_type,
        sim_runner=OSRunner(c),
    )
    if response_type == ResponseType.YTranslation:
        healthy_responses = healthy_responses.resize()
        crack_responses = crack_responses.resize()
    vmin = min(vmin, min(crack_responses.values()))
    vmax = max(vmax, max(crack_responses.values()))
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    plt.landscape()
    plt.subplot(2, 1, 1)
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(
        c=c,
        responses=healthy_responses,
        ploads=loads if LOADS else [],
        scatter=True,
        norm=norm,
    )
    plt.title("Truck 1 on healthy bridge")
    plt.subplot(2, 1, 2)
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(
        c=c,
        responses=crack_responses,
        ploads=loads if LOADS else [],
        scatter=True,
        norm=norm,
    )
    plt.title("Truck 1 on cracked bridge")
    plt.tight_layout()
    plt.savefig(
        original_c.get_image_path(
            "verification",
            safe_str(f"truck1-contour-x-{x}-{response_type.name()}") + ".pdf",
        )
    )
    plt.close()
