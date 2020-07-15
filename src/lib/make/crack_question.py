import datetime
from copy import deepcopy
from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import crack, sim, traffic, plot, temperature
from bridge_sim.model import Config, Point, ResponseType, Vehicle
from bridge_sim.util import flatten, print_i, print_w


def plot_crack_detection(config: Config, crack_x: float, length: float, healthy: bool):
    response_type = ResponseType.YTrans
    og_config = config
    if not healthy:
        config = crack.transverse_crack(length=length, at_x=crack_x).crack(config)
    ts, tr, ta = traffic.load_traffic(config, traffic.normal_traffic(config), time=60)

    # Calculate positions of sensors.
    support_xs = sorted(set((s.x for s in config.bridge.supports)))
    print_i(f"Support xs = {support_xs}")
    x_delta = 1
    mid0 = ((support_xs[0] + support_xs[1]) / 2) + x_delta
    mid1 = ((support_xs[-1] + support_xs[-2]) / 2) + x_delta
    point_0, point_1 = Point(x=mid0, z=-8.4), Point(x=mid1, z=-8.4)
    print(f"X positions = {mid0}, {mid1}")

    ##########################
    # Testing the positions. #
    ##########################

    # rs = sim.responses.load(
    #     config=config,
    #     response_type=response_type,
    #     point_loads=[PointLoad(x=mid0, z=-8.4, load=100), PointLoad(x=mid1, z=-8.4, load=100)],
    # )
    # plot.contour_responses(config, rs)
    # plot.top_view_bridge(config.bridge, piers=True)
    # plt.show()

    # Collect responses at times that vehicles cross sensors.
    vehicles: List[Vehicle] = [
        v for v in flatten(ts.vehicles_per_lane, Vehicle) if v.lane == 0
    ]
    print_i(f"Amount of vehicles = {len(vehicles)}")
    responses_0, responses_1 = [], []
    responses = sim.responses.to_traffic_array(
        config=config,
        traffic_array=ta,
        response_type=response_type,
        points=[point_0, point_1],
    )
    max_i = len(responses[0]) - 1
    total_time = np.round(ts.final_time - ts.start_time, 6)
    print_i(
        f"Total time, sensor_f, responses.shape = {total_time}, {config.sensor_freq}, {responses.shape}"
    )
    for v in vehicles:
        time_0, time_1 = v.time_at(mid0, config.bridge), v.time_at(mid1, config.bridge)
        print_i(f"Times = {time_0}, {time_1}")
        index_0 = int((time_0 - ts.start_time) // config.sensor_freq)
        index_1 = int((time_1 - ts.start_time) // config.sensor_freq)
        print_i(f"Indices = {index_0}, {index_1}")
        if 0 <= index_0 <= max_i and 0 <= index_1 <= max_i:
            responses_0.append(responses[0][index_0])
            responses_1.append(responses[1][index_1])
            print(responses_0[-1], responses_1[-1])
    responses_0 = np.array(responses_0)
    responses_1 = np.array(responses_1)
    plt.plot(responses_0)
    plt.plot(responses_1)
    plt.savefig(og_config.get_image_path("classify/crack", f"delta-{healthy}.pdf"))
    plt.close()


def plot_q5_crack_substructures(
    config: Config, crack_x: float, length: float, use_max: bool = False
):
    plt.style.use("seaborn-bright")
    feature, feature_name = np.var, "Variance"
    if use_max:
        feature, feature_name = np.max, "Maximum"

    def legend():
        plt.legend(
            facecolor="white",
            loc="lower right",
            framealpha=1,
            fancybox=False,
            borderaxespad=0,
        )

    og_config = deepcopy(config)
    OFFSET = 0.35
    SENSOR_DISTS = [2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25, 0.1]
    # SENSOR_DISTS = [1]
    lane = 0
    cmap = mpl.cm.get_cmap("RdBu")
    response_types = [
        ResponseType.StrainXXB,
        ResponseType.StrainZZB,
        ResponseType.YTrans,
    ]

    TIME_OFFSET_STDS = [0, 1, 2]

    # Iterate through the SENSOR_DIST parameter and collect difference matrices!
    # For each sensor dist we collect under healthy (0) and cracked (0).
    matrices = [
        [[([], [], []) for _ in SENSOR_DISTS] for _ in TIME_OFFSET_STDS]
        for _ in response_types
    ]
    for tos_i, time_offset_std in enumerate(TIME_OFFSET_STDS):
        for SD_i, SENSOR_DIST in enumerate(SENSOR_DISTS):
            # None is also healthy but needs a different dataset.
            for hc_i, is_healthy in enumerate([None, True, False]):
                time = 60 * 10
                if is_healthy is None:
                    time = 60 * 5
                if is_healthy in [None, True]:
                    config = og_config
                else:
                    config = crack.transverse_crack(length=length, at_x=crack_x).crack(
                        config
                    )
                    # config.bridge.data_id = config.bridge.data_id.replace(",0", "")  # TODO: remove hack!

                # TODO: Different traffic per run.
                if False:
                    time += np.random.random(1)

                # First calculate vehicles on the bridge.
                ts, tr, ta = traffic.load_traffic(
                    config, traffic.normal_traffic(config), time=time
                )
                vehicles: List[Vehicle] = [
                    v for v in flatten(ts.vehicles_per_lane, Vehicle) if v.lane == lane
                ]
                print_i(f"Amount of vehicles = {len(vehicles)}")

                # Calculate positions of sensors.
                x_centers = sorted(set(support.x for support in config.bridge.supports))
                d = (config.bridge.supports[0].length / 2) + OFFSET
                # Maximum and minimum x positions of sensors in each mid-span, respectively.
                xs_0, xs_1 = [x_centers[0] + d], [x_centers[-2] + d]
                xs_1_max = crack_x - OFFSET
                xs_0_max = xs_0[0] + (xs_1_max - xs_1[0])
                assert xs_1_max < crack_x
                assert OFFSET > 0
                while True:
                    new_x_0 = xs_0[-1] + SENSOR_DIST
                    if new_x_0 >= xs_0_max:
                        break
                    xs_0.append(new_x_0)
                while True:
                    new_x_1 = xs_1[-1] + SENSOR_DIST
                    if new_x_1 >= xs_1_max:
                        break
                    xs_1.append(new_x_1)
                z_min = config.bridge.lanes[lane].z_min
                z_max = config.bridge.lanes[lane].z_max
                NUM_Z = int((z_max - z_min) / SENSOR_DIST)
                # These two 2d-arrays are the sensor points in each mid-span, respectively.
                sensors_0 = np.array(
                    [
                        [Point(x=x, z=z) for z in np.linspace(z_min, z_max, NUM_Z)]
                        for x in xs_0
                    ]
                )
                sensors_1 = np.array(
                    [
                        [Point(x=x, z=z) for z in np.linspace(z_min, z_max, NUM_Z)]
                        for x in xs_1
                    ]
                )
                assert sensors_0.shape == sensors_1.shape

                # Verify position of sensors.
                plot.top_view_bridge(
                    config.bridge, lanes=True, edges=True, piers=True, units="m"
                )
                for p in flatten(sensors_0, Point) + flatten(sensors_1, Point):
                    plt.scatter([p.x], [p.z], c="r")
                plt.title(f"Sensors for crack zone at X = {int(crack_x)} m")
                plt.savefig(
                    config.get_image_path(
                        "classify/q5", f"sensor-positions-sensor-dist-{SENSOR_DIST}.pdf"
                    )
                )
                plt.close()

                # Load 10 minutes of weather data.
                weather = temperature.load("holly-springs-18")
                weather["temp"] = temperature.resize(weather["temp"], year=2018)
                start_date = "14/05/2018 14:00"
                end_date = "14/05/2018 14:10"

                for r_i, response_type in enumerate(response_types):
                    # Calculate responses to traffic for both sets of sensors.
                    responses_0 = sim.responses.to(
                        config=config,
                        traffic_array=ta,
                        response_type=response_type,
                        points=flatten(sensors_0, Point),
                        weather=weather,
                        start_date=start_date,
                        end_date=end_date,
                        with_creep=False,
                    ) * (1e6 if response_type.is_strain() else 1e3)
                    responses_1 = sim.responses.to(
                        config=config,
                        traffic_array=ta,
                        response_type=response_type,
                        points=flatten(sensors_1, Point),
                        weather=weather,
                        start_date=start_date,
                        end_date=end_date,
                        with_creep=False,
                    ) * (1e6 if response_type.is_strain() else 1e3)

                    def time_func(v_: Vehicle, x_: float, b_: "Bridge") -> float:
                        if time_offset_std == 0:
                            return v_.time_at(x_, b_)
                        new_time = v_.time_at(
                            time_offset_std * np.random.random() + x_, b_
                        )
                        print(f"Time is {new_time}, was {v_.time_at(x_, b_)}")
                        return new_time

                    # For each vehicle find times and responses for each sensor.
                    max_index = len(responses_0[0])
                    for v_i, v in enumerate(vehicles):
                        avoid = False
                        matrix_0 = np.zeros(sensors_0.shape)
                        matrix_1 = np.zeros(sensors_1.shape)
                        for x_i in range(len(sensors_0)):
                            for z_i, sensor in enumerate(sensors_0[x_i]):
                                time = time_func(v, sensor.x, config.bridge)
                                print_i(f"Time = {time}")
                                index = round(
                                    (time - ts.start_time) / config.sensor_freq
                                )
                                result = (
                                    responses_0[x_i * NUM_Z + z_i][index]
                                    if 0 <= index < max_index
                                    else np.nan
                                )
                                if np.isnan(result):
                                    avoid = True
                                matrix_0[x_i][z_i] = result
                        for x_i in range(len(sensors_1)):
                            for z_i, sensor in enumerate(sensors_1[x_i]):
                                time = time_func(v, sensor.x, config.bridge)
                                print_i(f"Time = {time}")
                                index = round(
                                    (time - ts.start_time) / config.sensor_freq
                                )
                                result = (
                                    responses_1[x_i * NUM_Z + z_i][index]
                                    if 0 <= index < max_index
                                    else np.nan
                                )
                                if np.isnan(result):
                                    avoid = True
                                matrix_1[x_i][z_i] = result

                        # Plot the results for this vehicle.
                        # vmin = min(np.amin(matrix_0), np.amin(matrix_1))
                        # vmax = max(np.amax(matrix_0), np.amax(matrix_1))
                        # vmin, vmax = min(vmin, -vmax), max(vmax, -vmin)
                        # norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
                        # xticks = np.arange(len(matrix_0), dtype=np.int)
                        # plt.portrait()
                        # plt.subplot(3, 1, 1)
                        # plt.imshow(matrix_0.T, cmap=cmap, norm=norm, interpolation="nearest", aspect="auto")
                        # plt.title(f"Healthy, Var = {np.var(matrix_0.T):.2f}")
                        # plt.xticks(xticks)
                        # plt.colorbar()
                        # plt.subplot(3, 1, 2)
                        # plt.imshow(matrix_1.T, cmap=cmap, norm=norm, interpolation="nearest", aspect="auto")
                        # plt.title(f"Cracked, Var = {np.var(matrix_1.T):.2f}")
                        # plt.xticks(xticks)
                        # plt.colorbar()
                        # plt.subplot(3, 1, 3)
                        mat_delta = matrix_0.T - matrix_1.T
                        # plt.imshow(mat_delta, cmap=cmap, norm=norm, interpolation="nearest", aspect="auto")
                        # plt.xticks(xticks)
                        # plt.title(f"Difference, Var = {np.var(mat_delta):.2f}")
                        # plt.colorbar()
                        # plt.suptitle(f"{response_type.name()}, {length} m crack zone at {crack_x} m")
                        # plt.tight_layout(rect=[0, 0.03, 1, 0.95])
                        # plt.savefig(config.get_image_path("classify/q5/mat/", f"vehicle={v_i}-sensor-dist={SENSOR_DIST}-healthy={is_healthy}-{tos_i}.pdf"))
                        # plt.close()

                        if not avoid:
                            matrices[r_i][tos_i][SD_i][hc_i].append(mat_delta)

    plt.figure(figsize=(20, 16))
    for tos_i, time_offset_std in enumerate(TIME_OFFSET_STDS):
        # Each feature is a row.
        for r_i, response_type in enumerate(response_types):
            plt.subplot(
                len(response_types),
                len(TIME_OFFSET_STDS),
                r_i * len(TIME_OFFSET_STDS) + tos_i + 1,
            )

            # Matrix collection has finished!
            for SD_i, SENSOR_DIST in enumerate(SENSOR_DISTS):
                ref_mats, healthy_mats, crack_mats = matrices[r_i][tos_i][SD_i]
                ref_features = list(map(feature, ref_mats))
                healthy_features = list(map(feature, healthy_mats))
                cracked_features = list(map(feature, crack_mats))
                min_feature, max_feature = min(ref_features), max(ref_features) * 1.5
                print_i(
                    f"Sensor distance = {SENSOR_DIST}, feature = {feature_name}, min max ref = {min_feature}, {max_feature}"
                )
                print_i(
                    f"Sensor distance = {SENSOR_DIST}, feature = {feature_name}, min max healthy = {min(healthy_features)}, {max(healthy_features)}"
                )
                print_i(
                    f"Sensor distance = {SENSOR_DIST}, feature = {feature_name}, min max cracked = {min(cracked_features)}, {max(cracked_features)}"
                )

                fprs, tprs = [], []
                for TH in np.linspace(min_feature, max_feature, 100):
                    fp = len([1 for m in healthy_mats if feature(m) > TH])
                    fpr = fp / len(healthy_mats)
                    tp = len([1 for m in crack_mats if feature(m) > TH])
                    tpr = tp / len(crack_mats)
                    fprs.append(fpr)
                    tprs.append(tpr)

                plt.plot(fprs, tprs, label=f"d = {SENSOR_DIST}", lw=2)
                plt.xlabel("FPR")
                plt.ylabel("TPR")
            if tos_i == len(TIME_OFFSET_STDS) - 1 and r_i == len(response_types) - 1:
                legend()
            plt.title(f"{response_type.name()} (±{time_offset_std} m)")

    plt.suptitle(
        f"Receiver operating characteristic curves for {length} m crack zone at {crack_x} m (feature is '{feature_name.lower()}')"
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(
        config.get_image_path("classify/q5", f"roc{use_max}-{feature_name}.pdf")
    )
    plt.close()
