from copy import deepcopy

import matplotlib as mpl
import numpy as np

from classify.data.responses.convert import loads_to_traffic_array
from classify.data.responses import (
    responses_to_traffic_array,
    responses_to_vehicles_d,
)
from classify.data.traffic import load_traffic
from classify.vehicle import wagen1
from classify.scenarios import healthy_scenario
from classify.scenario.bridge import HealthyDamage, transverse_crack
from classify.scenario.bridge import healthy_damage_w_transverse_crack_nodes
from classify.scenario.traffic import normal_traffic
from classify import temperature
from config import Config
from fem.build import BuildContext, get_bridge_shells
from fem.params import ExptParams, SimParams
from fem.responses import Responses, load_fem_responses
from fem.responses.matrix.il import ILMatrix
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.bridge import Point
from model.load import MvVehicle, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from bridge_sim.util import flatten, print_i, round_m, safe_str

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
        # Load and plot fem.
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
    """Compare fem between uniaxle vehicles and Truck 1."""
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
    plt.title(f"{num_times} fem with ULS = {c.il_num_loads} (Wagen 1 (4 axles))")
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
    plt.title(f"{num_times} fem with ULS = {c.il_num_loads} (2 axles)")
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
    plt.title(f"{num_times} fem with ULS = {c.il_num_loads} (1 axle)")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))

    plt.tight_layout()
    plt.savefig(c.get_image_path("system-verification", "compare-axles.pdf"))


def compare_responses(c: Config):
    """Compare fem to Truck 1, direct simulation and matmul."""
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

    # Start with fem from direct simulation.
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
    plt.title(f"{len(wagen1_times)} fem")
    plt.plot(wagen1_times, responses_not_binned)

    # Then fem from direct simulation with binning.
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
    plt.title(f"{len(wagen1_times)} fem (binned)")
    plt.plot(wagen1_times, responses_binned)
    xlim = plt.xlim()

    num_times = int(end_time / c.sensor_hz)
    wagen1_times = np.linspace(0, end_time, num_times)

    # Then from 'TrafficArray' we get fem, without binning.
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
    plt.title(f"{num_times} fem with ULS = {c.il_num_loads} traffic_array")
    plt.plot(wagen1_times, np.array(responses_ulm).reshape(-1, 1))
    plt.xlim(xlim)

    # # Then from 'TrafficArray' we get fem, with binning.
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
        f"{num_times} fem from {c.il_num_loads} il_num_loads\ntraffic_array binned"
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


def wagen_1_contour_plot(
    c: Config,
    x: int,
    crack_x: float,
    response_type: ResponseType,
    scatter: bool,
    run: bool,
    length: float,
    outline: bool,
    wheels: bool,
    temp: bool,
):
    original_c = c
    LOADS = False
    temp_bottom, temp_top = [17, 25]
    time = wagen1.time_at(x=x, bridge=c.bridge)

    def plot_wheels():
        if wheels:
            wagen1.plot_wheels(c=c, time=time, label="Truck 1 wheels", zorder=100)

    center = c.bridge.x_max / 2
    min_x, max_x = center - 20, center + 20
    min_z, max_z = c.bridge.z_min, c.bridge.z_max

    def zoom_in():
        plt.ylim(min_z, max_z)
        plt.xlim(min_x, max_x)

    loads = wagen1.to_wheel_track_loads(c=c, time=time, flat=True)

    crack_f = lambda: transverse_crack(length=length, at_x=crack_x)
    c = healthy_damage_w_transverse_crack_nodes(crack_f).use(original_c)[0]
    deck_shells = get_bridge_shells(c.bridge)[0]
    healthy_responses = load_fem_responses(
        c=c,
        sim_params=SimParams(ploads=loads),
        response_type=response_type,
        sim_runner=OSRunner(c),
        run=run,
    ).at_shells(
        deck_shells
    )  # Convert fem to one per shell.
    if response_type in [ResponseType.Strain, ResponseType.StrainZZB]:
        # Resize by E-6 from microstrain to strain to match temperature units.
        healthy_responses = healthy_responses.resize()
    before_temp = healthy_responses.at_deck(Point(x=51, z=-8.4), interp=False)
    if temp:
        healthy_deck_points = healthy_responses.deck_points()  # Point of fem.
        temp_effect = temperature.effect(
            c=c,
            response_type=response_type,
            points=healthy_deck_points,
            temps_bt=([temp_bottom], [temp_top]),
        ).T[
            0
        ]  # Temperature effect at existing response points.
        healthy_responses = healthy_responses.add(temp_effect, healthy_deck_points)
    after_temp = healthy_responses.at_deck(Point(x=51, z=-8.4), interp=False)
    print_i(f"Healthy, before/after = {before_temp}, {after_temp}")
    if response_type in [ResponseType.Strain, ResponseType.StrainZZB]:
        healthy_responses = healthy_responses.map(lambda x: x * 1e6)
    else:
        healthy_responses = healthy_responses.resize()

    # Responses in cracked scenario.
    c = crack_f().use(original_c)[0]
    crack_responses = load_fem_responses(
        c=c,
        sim_params=SimParams(ploads=loads),
        response_type=response_type,
        sim_runner=OSRunner(c),
        run=run,
    ).at_shells(deck_shells)
    if response_type in [ResponseType.Strain, ResponseType.StrainZZB]:
        # Resize by E-6 from microstrain to strain to match temperature units.
        crack_responses = crack_responses.resize()
    before_temp = crack_responses.at_deck(Point(x=51, z=-8.4), interp=False)
    if temp:
        crack_deck_points = crack_responses.deck_points()  # Point of fem.
        temp_effect = temperature.effect(
            c=c,
            response_type=response_type,
            points=healthy_deck_points,
            temps_bt=([temp_bottom], [temp_top]),
        ).T[
            0
        ]  # Temperature effect at existing response points.
        crack_responses = crack_responses.add(temp_effect, healthy_deck_points)
    after_temp = crack_responses.at_deck(Point(x=51, z=-8.4), interp=False)
    print_i(f"Crack, before/after = {before_temp}, {after_temp}")
    if response_type in [ResponseType.Strain, ResponseType.StrainZZB]:
        crack_responses = crack_responses.map(lambda x: x * 1e6)
    else:
        crack_responses = crack_responses.resize()

    # Limit to points in crack zone.
    without_cm = 35
    print(f"Avoid {without_cm} cm around crack zone")
    _without_crack_zone = crack_f().without(c.bridge, without_cm / 100)
    without_crack_zone = lambda p: not _without_crack_zone(p)
    if response_type in [ResponseType.Strain, ResponseType.StrainZZB]:
        healthy_responses = healthy_responses.without(without_crack_zone)
        crack_responses = crack_responses.without(without_crack_zone)

    # Norm calculation.
    vmin = min(healthy_responses.values())
    vmax = max(healthy_responses.values())
    vmin = min(vmin, min(crack_responses.values()))
    vmax = max(vmax, max(crack_responses.values()))
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    print(f"Norm min/max = {vmin}, {vmax}")

    plt.portrait()
    plt.subplot(3, 1, 1)
    plot_contour_deck(
        c=c,
        responses=healthy_responses,
        ploads=loads if LOADS else [],
        scatter=scatter,
        norm=norm,
        decimals=2,
    )

    c_x_start, c_z_start, c_x_end, c_z_end = list(
        map(round_m, crack_f().crack_area(c.bridge))
    )

    def plot_outline(label="Crack zone"):
        if outline:
            plt.gca().add_patch(
                mpl.patches.Rectangle(
                    (c_x_start, c_z_start),
                    c_x_end - c_x_start,
                    c_z_end - c_z_start,
                    fill=not scatter,
                    edgecolor="black",
                    facecolor="white",
                    alpha=1,
                    label=label,
                )
            )

    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_outline(label="Responses not considered")
    plot_wheels()
    zoom_in()

    def legend():
        plt.legend(
            loc="upper right",
            borderpad=0.2,
            labelspacing=0.2,
            borderaxespad=0,
            handletextpad=0.2,
            columnspacing=0.2,
        )

    legend()
    plt.title(f"Healthy bridge")
    plt.xlabel("")
    plt.tick_params(bottom=False, labelbottom=False)

    plt.subplot(3, 1, 2)
    plot_contour_deck(
        c=c,
        responses=crack_responses,
        ploads=loads if LOADS else [],
        scatter=scatter,
        norm=norm,
        decimals=2,
    )

    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_outline()
    plot_wheels()
    zoom_in()

    legend()
    plt.title(f"Cracked bridge")
    plt.xlabel("")
    plt.tick_params(bottom=False, labelbottom=False)

    plt.subplot(3, 1, 3)
    responses = []
    for x in healthy_responses.deck_xs:
        for z in healthy_responses.zs[x][0]:
            responses.append(
                (
                    healthy_responses.responses[0][x][0][z]
                    - crack_responses.at_deck(Point(x=x, z=z), interp=False),
                    Point(x=x, z=z),
                )
            )
            # try:
            #     fem.append((
            #         healthy_responses.fem[0][x][0][z]
            #         - crack_responses.fem[0][x][0][z],
            #         Point(x=x, z=z)
            #     ))
            # except KeyError:
            #     pass
            #
    diff_responses = responses = Responses(
        response_type=response_type, responses=responses, units=healthy_responses.units,
    )
    plot_contour_deck(
        c=c,
        responses=diff_responses,
        ploads=loads if LOADS else [],
        cmap=mpl.cm.get_cmap("PiYG"),
        scatter=scatter,
        decimals=2,
    )

    print("********")
    print("********")
    print("********")
    grid_x, grid_z = 600, 200
    grid_points = list(
        filter(
            lambda p: not without_crack_zone(p),
            [
                Point(x=x, y=0, z=z)
                for x in np.linspace(c.bridge.x_min, c.bridge.x_max, grid_x)
                for z in np.linspace(c.bridge.z_min, c.bridge.z_max, grid_z)
            ],
        )
    )
    print(f"Amount grid points = {len(grid_points)}")
    grid_x_len = c.bridge.length / grid_x
    grid_z_len = c.bridge.width / grid_z
    grid_area = grid_x_len * grid_z_len
    print(f"Grid area = {grid_area}")
    print("Interpolating diff fem")
    interp_diff_responses = diff_responses.at_decks(grid_points)
    count_interp = len(interp_diff_responses)
    interp_diff_responses = interp_diff_responses[~np.isnan(interp_diff_responses)]
    print(
        f"Removed {count_interp - len(interp_diff_responses)} of {count_interp} fem, remaining = {len(interp_diff_responses)}"
    )
    print("Finished interpolating diff fem")
    count_min, count_max = 0, 0
    d_min, d_max = min(diff_responses.values()), max(diff_responses.values())
    print(f"diff min, max = {d_min}, {d_max}")
    d_min08, d_max08 = d_min * 0.8, d_max * 0.8
    for interp_r in interp_diff_responses:
        if interp_r < d_min08:
            count_min += 1
        if interp_r > d_max08:
            count_max += 1
    print(f"Count = {count_min}, {count_max}")
    save_path = original_c.get_image_path(
        "verification",
        safe_str(
            f"truck1-contour-x-{x}{crack_x}{length}-{response_type.name()}-{temp}"
        ),
    )
    with open(save_path + ".txt", "w") as f:
        f.write(f"{count_min}, {count_max}\n")
        f.write(f"{count_min * grid_area}, {count_max * grid_area}")
    print(f"Wrote results to {save_path}.txt")

    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_outline()
    plot_wheels()
    zoom_in()

    legend()
    temp_str = f"\nT_bot = {temp_bottom} °C, T_top = {temp_top} °C" if temp else ""
    plt.title(f"Difference of healthy & cracked bridge")
    rt_name = (
        f"Microstrain {response_type.ss_direction()}"
        if response_type in [ResponseType.Strain, ResponseType.StrainZZB]
        else response_type.name()
    )

    plt.suptitle(f"{rt_name}: Truck 1 on healthy & cracked bridge{temp_str}")
    plt.tight_layout(rect=[0, 0.03, 1, 0.93 if temp else 0.95])
    plt.savefig(save_path + ".pdf")


def cracked_concrete_plot(c: Config):
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    sensor_point = Point(x=51.8, y=0, z=-8.4)
    # Generate traffic data.
    total_mins = 2
    total_seconds = total_mins * 60
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, traffic, traffic_array = load_traffic(
        c=c, traffic_scenario=traffic_scenario, max_time=total_seconds,
    )
    # Split the traffic array in half, the crack will happen halfway through.
    half_i = int(len(traffic_array) / 2)
    traffic_array_0, traffic_array_1 = traffic_array[:half_i], traffic_array[half_i:]
    assert len(traffic_array_0) + len(traffic_array_1) == len(traffic_array)
    # Collect fem due to traffic.
    responses = []
    for rt in response_types:
        responses_healthy_cracked = []
        for ds, ta in [
            (healthy_damage, traffic_array_0),
            (transverse_crack(), traffic_array_1),
        ]:
            print(f"Sections in damage scenario = {len(ds.use(c)[0].bridge.sections)}")
            responses_healthy_cracked.append(
                responses_to_traffic_array(
                    c=c,
                    traffic_array=ta,
                    response_type=rt,
                    damage_scenario=ds,
                    points=[sensor_point],
                ).T[0]
            )  # Responses from a single point.
        responses.append(np.concatenate(responses_healthy_cracked))
    responses = np.array(responses)
    # Plot the cracked time series.
    x0 = np.arange(half_i) * c.sensor_hz / 60
    x1 = np.arange(half_i, len(responses[0])) * c.sensor_hz / 60
    plt.landscape()
    plt.subplot(2, 1, 1)
    plt.plot(x0, responses[0][:half_i] * 1000, label="Healthy")
    plt.plot(x1, responses[0][half_i:] * 1000, label="Cracked")
    plt.legend()
    plt.ylabel("Y translation (mm)")
    plt.xlabel("Time (minutes)")
    # plt.plot(np.arange(half_i, len(fem[0])), fem[0][half_i:])
    plt.subplot(2, 1, 2)
    plt.plot(x0, responses[1][:half_i], label="Healthy")
    plt.plot(x1, responses[1][half_i:], label="Cracked")
    plt.legend()
    plt.ylabel("Microstrain")
    plt.xlabel("Time (minutes)")
    # plt.plot(np.arange(half_i, len(fem[1])), fem[1][half_i:])
    plt.savefig(c.get_image_path("verify/cracked", "crack-time-series.pdf"))
