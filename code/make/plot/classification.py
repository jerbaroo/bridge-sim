import itertools

import matplotlib as mpl
import numpy as np
from scipy import stats
from sklearn.svm import OneClassSVM

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.noise import add_displa_noise
from classify.temperature import add_temperature_effect, estimate_temp_effect, load_temperature_month, temperature_effect
from classify.scenario.bridge import HealthyDamage
from classify.scenario.traffic import normal_traffic
from classify.scenarios import each_pier_scenarios, healthy_and_cracked_scenarios, healthy_scenario
from fem.responses import Responses
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array
from model.bridge import Point
from model.response import ResponseType
from model.scenario import to_traffic_array
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import print_i


def events(c: Config, x: float, z: float):
    """Plot events due to normal traffic."""
    point = Point(x=x, y=0, z=z)
    # 10 seconds of 'normal' traffic.
    max_time = 10
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    # Create the 'TrafficSequence' and 'TrafficArray'.
    traffic_sequence = traffic_scenario.traffic_sequence(
        bridge=c.bridge, max_time=max_time
    )
    traffic_array = to_traffic_array(
        c=c, traffic_sequence=traffic_sequence, max_time=max_time
    )
    # Find when the simulation has warmed up, and when 'TrafficArray' begins.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)
    traffic_array_starts = (int(warmed_up_at / c.sensor_hz) + 1) * c.sensor_hz
    print(f"warmed up at = {warmed_up_at}")
    print(f"traffic_array_starts = {traffic_array_starts}")
    traffic_array_ends = traffic_array_starts + (len(traffic_array) * c.sensor_hz)
    print(f"traffic_array_ends = {traffic_array_ends}")
    point_lane_ind = c.bridge.closest_lane(z)
    vehicles = list(set(ts[0] for ts in traffic_sequence))
    print(len(vehicles))
    print(vehicles[0])
    vehicles = sorted(set(ts[0] for ts in traffic_sequence if ts[0].lane == point_lane_ind), key=lambda v: -v.init_x_frac)
    print(len(vehicles))
    print(vehicles[0])
    event_indices = []
    vehicle_times = [v.time_at(x=x - 2, bridge=c.bridge) for v in vehicles]
    for v, t in zip(vehicles, vehicle_times):
        print(f"Vehicle {v.init_x_frac} {v.mps} at time {t}")
        start_time = int(t / c.sensor_hz) * c.sensor_hz
        print(f"start_time = {start_time}")
        ta_start_time = np.around(start_time - traffic_array_starts, 8)
        print(f"ta start time = {ta_start_time}")
        ta_start_index = int(ta_start_time / c.sensor_hz)
        print(f"ta start index = {ta_start_index}")
        ta_end_index = ta_start_index + int(c.event_time_s / c.sensor_hz)
        print(f"ta end index = {ta_end_index}")
        if ta_start_index >= 0 and ta_end_index < len(traffic_array):
            event_indices.append((ta_start_index, ta_end_index))
    print(event_indices)
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=traffic_array,
        response_type=ResponseType.YTranslation,
        damage_scenario=healthy_scenario,
        points=[point],
        sim_runner=OSRunner(c),
    ) * 1000
    # responses = add_displa_noise(responses)
    print(responses.shape)
    plt.portrait()
    for event_ind, (event_start, event_end) in enumerate(event_indices):
        plt.subplot(len(event_indices), 1, event_ind + 1)
        plt.plot(responses[event_start:event_end + 1])
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/events", "events.pdf"))
    plt.close()


def temperature_effect_month(c: Config, month: str):
    temp = load_temperature_month(month)
    point = Point(x=51, y=0, z=-8.4)
    plt.landscape()
    def plot_hours():
        label_set = False
        for dt in temp["datetime"]:
            if np.isclose(float(dt.hour + dt.minute), 0):
                label = None
                if not label_set:
                    label = "Time at vertical line = 00:00"
                    label_set = True
                plt.axvline(x=dt, linewidth=1, color="black", label=label)
    # Plot the temperature.
    plt.subplot(2, 1, 1)
    plot_hours()
    plt.scatter(temp["datetime"], temp["temp"], c=temp["missing"], cmap=mpl.cm.get_cmap("bwr"), s=1)
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Date")
    plt.gcf().autofmt_xdate()
    plt.title(f"Temperature in {str(month[0]).upper()}{month[1:]}")
    plt.legend()
    # Plot the effect at a point.
    response_type = ResponseType.YTranslation
    plt.subplot(2, 1, 2)
    plot_hours()
    effect = temperature_effect(c=c, response_type=response_type, point=point, temps=temp["temp"])
    plt.scatter(temp["datetime"], effect * 1000, c=temp["missing"], cmap=mpl.cm.get_cmap("bwr"), s=1)
    plt.ylabel(f"{response_type.name()} (mm)")
    plt.xlabel("Date")
    plt.gcf().autofmt_xdate()
    plt.title(f"{response_type.name()} to unit thermal loading in {month}")
    # Save.
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/temperature", f"{month}.pdf"))
    plt.close()


def temperature_removal_month(c: Config, month: str):
    response_type = ResponseType.YTranslation
    temp = load_temperature_month(month)
    point = Point(x=51, y=0, z=-8.4)
    mins = 5
    speed_up_temp = 60
    plt.landscape()
    # Responses to normal traffic.
    normal_traffic_array = load_normal_traffic_array(c, mins=mins)
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=normal_traffic_array,
        response_type=response_type,
        damage_scenario=HealthyDamage(),
        points=[point],
        sim_runner=OSRunner(c),
    ).flatten()
    print(f"responses.shape = {responses.shape}")
    x_mins = c.sensor_hz * np.arange(len(responses)) / 60
    plt.subplot(3, 1, 1)
    plt.plot(x_mins, responses * 1000, color="b")
    plt.ylabel(f"{response_type.name()} (mm)")
    plt.title(f"{response_type.name()} due to {mins} minutes of traffic")
    # Add temperature and noise.
    print("Adding effect")
    responses_w_temp = add_temperature_effect(
        c=c,
        response_type=response_type,
        point=point,
        temps=temp["temp"],
        responses=responses,
        speed_up=speed_up_temp,
    )
    print(f"responses_w_temp = {responses_w_temp.shape}")
    print("Adding noise")
    responses_w_noise = add_displa_noise(responses_w_temp)
    print(f" responses_w_noise shape = {responses_w_noise.shape}")
    temp_effect = responses_w_temp - responses
    print(responses.shape)
    plt.subplot(3, 1, 2)
    print("plotting")
    plt.scatter(x_mins, responses_w_noise * 1000, color="b", label=f"Response to traffic and temperature", s=1)
    plt.scatter(x_mins, temp_effect * 1000, color="r", label=f"Temperature effect ({speed_up_temp} x speedup)", s=1)
    plt.ylabel(f"{response_type.name()} (mm)")
    plt.xlabel("Time (m)")
    plt.title(f"Sensor noise and temperature effect added")
    legend = plt.legend()
    #change the marker size manually for both lines
    legend.legendHandles[0]._sizes = [50]
    legend.legendHandles[1]._sizes = [50]
    # Equalize y limits.
    ylim = (np.inf, -np.inf)
    for p in [1, 2, 1]:
        plt.subplot(3, 1, p)
        ylim = (min(ylim[0], plt.ylim()[0]), max(ylim[1], plt.ylim()[1]))
    for p in [1, 2]:
        plt.subplot(3, 1, p)
        plt.ylim(ylim)
    # Remove effect of temperature.
    temp_fit = estimate_temp_effect(c=c, responses=responses_w_noise, speed_up=speed_up_temp)
    print(len(temp_fit))
    print(len(responses_w_noise))
    plt.subplot(3, 1, 3)
    plt.plot([0], [0], label="TODO: Estimate & remove temp effect")
    # plt.plot(temp_fit * 1000, label="estimate")
    # plt.plot(temp_effect * 1000, label="real")
    # plt.plot(temp_fit * 1000 - temp_effect * 1000, label="error")
    plt.legend()
    # Save.
    print("tight")
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/temperature", f"{month}-removal.pdf"))
    plt.close()


def oneclass(c: Config):
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    bridge_scenarios = [HealthyDamage()] + each_pier_scenarios(c)
    response_type = ResponseType.YTranslation
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max / 2, 20),
            np.linspace(c.bridge.z_min, c.bridge.z_max / 2, 3),
        )
    ]
    results = []

    for b, bridge_scenario in enumerate(bridge_scenarios):
        print_i(f"One class: bridge scenario {bridge_scenario.name}")
        responses = responses_to_traffic_array(
            c=c,
            traffic_array=normal_traffic_array,
            response_type=response_type,
            bridge_scenario=bridge_scenario,
            points=points,
            fem_runner=OSRunner(c),
        ).T
        print(len(normal_traffic_array))
        print(responses.shape)

        # Fit on the healthy scenario.
        if b == 0:
            assert len(responses) == len(points)
            clfs = []
            for r, rs in enumerate(responses):
                print_i(f"Training classifier {r} / {len(responses)}")
                clfs.append(OneClassSVM().fit(rs.reshape(-1, 1)))

        scenario_results = []
        for p, _ in enumerate(points):
            print_i(f"Predicting points {p} / {len(points)}")
            prediction = clfs[p].predict(responses[p].reshape(-1, 1))
            print(prediction)
            print(len(prediction[prediction < 0]))
            print(len(prediction[prediction > 0]))


def ks_no_outliers(d0, d1):
    """D statistic of ks_2samp with outliers removed."""
    # print(len(d0))
    # d0 = d0[~np.isnan(d0)]
    # print(len(d0))
    # d1 = d1[~np.isnan(d1)]
    if np.sum(d0) > 0:
        z0 = np.abs(stats.zscore(d0))
        # print(f"d0 shape = {d0.shape}")
        # d0 = np.where(z0 <= 4, d0, np.zeros(z0.shape)).nonzero()[0]
        # print(f"d0 shape = {d0.shape}")
    if np.sum(d1) > 0:
        z1 = np.abs(stats.zscore(d1))
        # print(f"d1 shape = {d1.shape}")
        # d1 = np.where(z1 <= 4, d1, np.zeros(z1.shape)).nonzero()[0]
        # print(f"d1 shape = {d1.shape}")
    return stats.ks_2samp(d0, d1)[0]


def pairwise_cluster(c: Config, load: bool):
    """Cluster pairwise maps from healthy and damaged scenarios."""
    features_path = c.get_data_path("features", "pairwise-cluster", bridge=False)
    if not load:
        normal_traffic_array, _ = load_normal_traffic_array(c=c, mins=24)
        normal_traffic_array = normal_traffic_array[
            int(len(normal_traffic_array) / 24) :
        ]
        response_type = ResponseType.YTranslation
        grid_points = [
            Point(x=x, y=0, z=-9.65)
            for x, _ in itertools.product(
                np.linspace(c.bridge.x_min, c.bridge.x_max, 50),
                # np.linspace(c.bridge.x_min, c.bridge.x_max, 4),
                [1],
            )
        ]

        # Collect a list of features per damage scenario.
        features = []
        for damage_scenario in healthy_and_cracked_scenarios[1:]:
            damage_c = damage_scenario.use(c)
            responses = responses_to_traffic_array(
                c=damage_c,
                traffic_array=normal_traffic_array,
                response_type=response_type,
                bridge_scenario=damage_scenario,
                points=grid_points,
                sim_runner=OSRunner,
            ).T
            ks_values = []
            for p0_i, point0 in enumerate(grid_points):
                print_i(f"Point {p0_i + 1} / {len(grid_points)}", end="\r")
                ks_values.append([])
                for p1_i, point1 in enumerate(grid_points):
                    ks = ks_no_outliers(responses[p0_i], responses[p1_i])
                    ks_values[-1].append(ks)
            features.append((ks_values, damage_scenario.name))

        # Save features to disk.
        features = np.array(features)
        np.save(features_path, features)

    features = np.load(features_path)
    # Reduce each pairwise map to a sum per sensor.
    for f_i, (feature, feature_name) in enumerate(features):
        features[f_i] = ([sum(sensor) for sensor in feature], feature_name)
        features[f_i] = ([sum(sensor) for sensor in features[f_i]], feature_name)

    # Cluster each pairwise map.
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(features)


def pairwise_sensors(c: Config, dist_measure=ks_no_outliers):
    """Compare distribution of pairs of sensors under HealthyScenario."""
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    response_type = ResponseType.YTranslation
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 50),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 4),
        )
    ]

    bridge_scenario = HealthyDamage()
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=normal_traffic_array,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        sim_runner=OSRunner,
    ).T
    assert len(responses) == len(points)

    ks_values_healthy = []
    for p0, point0 in enumerate(points):
        print_i(f"Point {p0 + 1} / {len(points)}")
        ks_values_healthy.append([])
        for p1, point1 in enumerate(points):
            ks = dist_measure(responses[p0], responses[p1])
            ks_values_healthy[-1].append(ks)

    plt.landscape()
    plt.imshow(ks_values_healthy)
    plt.savefig(c.get_image_path("joint-clustering", "healthy-bridge"))
    plt.close()

    bridge_scenario = each_pier_scenarios(c)[0]
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=normal_traffic_array,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        sim_runner=OSRunner,
    ).T
    assert len(responses) == len(points)

    ks_values_damage = []
    for p0, point0 in enumerate(points):
        print_i(f"Point {p0 + 1} / {len(points)}")
        ks_values_damage.append([])
        for p1, point1 in enumerate(points):
            ks = dist_measure(responses[p0], responses[p1])
            ks_values_damage[-1].append(ks)

    plt.imshow(ks_values_damage)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge"))
    plt.close()

    ks_values_comp = []
    for p0, point0 in enumerate(points):
        ks_values_comp.append([])
        for p1, point1 in enumerate(points):
            comp = abs(ks_values_healthy[p0][p1] - ks_values_damage[p0][p1])
            ks_values_comp[-1].append(comp)

    plt.landscape()
    plt.imshow(ks_values_comp)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge-comp"))
    plt.close()

    responses = Responses.from_responses(
        response_type=response_type,
        responses=[(sum(ks_values_comp[p]), point) for p, point in enumerate(points)],
    )
    top_view_bridge(c.bridge, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=responses)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge-comp-contour"))
    plt.close()
