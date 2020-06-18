import os

import matplotlib.pyplot as plt
import numpy as np
from bridge_sim import sim, plot, temperature
from bridge_sim.crack import transverse_crack

from bridge_sim.model import Config, PointLoad, Point, ResponseType, PierSettlement
from bridge_sim.plot import top_view_bridge
from bridge_sim.plot.util import equal_lims
from bridge_sim.sim.model import Responses
from bridge_sim.sim.responses import to_traffic_array, without
from bridge_sim.traffic import Traffic, TrafficSequence
from bridge_sim.util import print_i, flatten, project_dir
from bridge_sim.vehicles import truck1
from lib.validate import _displa_sensor_xz, _strain_sensor_xz


def truck_1_time_series(c: Config):
    """Time series of 3 sensors to Truck 1's movement."""
    side_s = 7
    side = int(side_s * (1 / c.sensor_hz))
    assert truck1.x_at(time=0, bridge=c.bridge) == 0
    # Get times and loads for Truck 1.
    end_time = truck1.time_left_bridge(c.bridge)
    traffic_array = TrafficSequence(
        config=c, vehicles_per_lane=[[truck1], []], warmed_up_at=0, final_time=end_time,
    ).traffic_array()

    # Find points of each sensor.
    displa_labels = ["U13", "U26", "U29"]
    displa_points = [
        Point(x=sensor_x, y=0, z=sensor_z)
        for sensor_x, sensor_z in [
            _displa_sensor_xz(displa_label) for displa_label in displa_labels
        ]
    ]
    strain_labels = ["T1", "T10", "T11"]
    strain_points = [
        Point(x=sensor_x, y=0, z=sensor_z)
        for sensor_x, sensor_z in [
            _strain_sensor_xz(strain_label) for strain_label in strain_labels
        ]
    ]
    for strain_point in strain_points:
        print(f"Strain point = {strain_point}")
    for displa_point in displa_points:
        print(f"Displa point = {displa_point}")

    ################
    # Vert. trans. #
    ################

    plt.portrait()
    # Ensure points and truck are on the same lane.
    assert all(p.z < 0 for p in displa_points)

    # Results from simulation.
    responses_truck1 = to_traffic_array(
        config=c,
        traffic_array=traffic_array,
        response_type=ResponseType.YTrans,
        points=displa_points,
    )
    for s_i, sensor_responses in enumerate(responses_truck1):
        plt.subplot(len(displa_points), 1, s_i + 1)
        # Find the center of the plot, minimum point in the data.
        data_center = 10
        for i in range(len(sensor_responses)):
            if sensor_responses[i] < sensor_responses[data_center]:
                data_center = i
        left, right = (
            max(0, data_center - side),
            min(len(sensor_responses), data_center + side),
        )
        plot_data = sensor_responses[left:right]
        x = np.arange(len(plot_data)) / 700
        if data_center - side < 0:
            x += abs(data_center - side) / 700
        plt.plot(x, plot_data, c="b", label="Simulation")

    # Results from experiment.
    center = 13500
    plot_offsets = [-1350, -825, 0]
    for s_i, displa_label in enumerate(displa_labels):
        plt.subplot(len(displa_points), 1, s_i + 1)
        with open(
            os.path.join(
                project_dir(), f"data/validation/experiment/D1a-{displa_label}.txt"
            )
        ) as f:
            data = list(map(float, f.readlines()))
        print_i(f"Total Y translation data length = {len(data)}")
        new_center = center + plot_offsets[s_i]
        plot_data = data[new_center - side : new_center + side]
        x = np.arange(len(plot_data)) / 700
        plt.plot(x, plot_data, c="r", label="Experiment")

        # Labels/titles.
        plt.legend()
        plt.ylabel(f"{ResponseType.YTrans.name()} (mm)")
        plt.xlabel("Time (s)")
        point = displa_points[s_i]
        plt.title(f"{displa_labels[s_i]} at X = {point.x} m, Z = {point.z} m")
        if s_i < len(displa_labels) - 1:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)

    plt.tight_layout()
    plt.savefig(c.get_image_path("validation/dynamic", "y-trans.pdf"))
    plt.close()

    ##########
    # Strain #
    ##########

    plt.portrait()
    # Results from simulation.
    responses_truck1 = (
        to_traffic_array(
            config=c,
            traffic_array=traffic_array,
            response_type=ResponseType.StrainXXB,
            points=strain_points,
        )
        * 1e-3
    )
    for s_i, sensor_responses in enumerate(responses_truck1):
        plt.subplot(len(strain_points), 1, s_i + 1)
        data_center = 0
        for i in range(len(sensor_responses)):
            if sensor_responses[i] > sensor_responses[data_center]:
                data_center = i
        plt.plot(
            sensor_responses[data_center - side : data_center + side],
            c="b",
            label="Simulation",
        )

    # Results from experiment.
    center = 13000
    plot_offsets = [-370, -290, -160]
    for s_i, strain_label in enumerate(strain_labels):
        plt.subplot(len(strain_points), 1, s_i + 1)
        with open(
            os.path.join(
                project_dir(), f"data/validation/experiment/D1a-{strain_label}.txt"
            )
        ) as f:
            data = list(map(float, f.readlines()))
        print_i(f"Total strain data length = {len(data)}")
        new_center = center + plot_offsets[s_i]
        plt.plot(data[new_center - side : new_center + side], c="r", label="Experiment")

        # Labels/titles.
        plt.legend()
        plt.ylabel("Microstrain XXB")
        plt.xlabel("Time (s)")
        point = strain_points[s_i]
        plt.title(f"{strain_labels[s_i]} at X = {point.x} m, Z = {point.z} m")
        if s_i < len(strain_labels) - 1:
            plt.tick_params(axis="x", bottom=False, labelbottom=False)

    # set_labels(ResponseType.StrainXXB.name(), "Time")
    plt.tight_layout()
    plt.savefig(c.get_image_path("validation/dynamic", "strain.pdf"))
    plt.close()


def stress_strength_plot(config: Config, top: bool):
    """Plot the difference of tensile strength and stress under load."""
    plt.portrait()
    response_type = ResponseType.StrainXXT if top else ResponseType.StrainXXB
    settlement_mm = 3
    temp_bottom, temp_top = 21, 30
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, 200)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 60)
    ]

    # Pier settlement.
    plt.subplot(3, 1, 1)
    responses = (
        sim.responses.load(
            config=config,
            response_type=response_type,
            pier_settlement=[PierSettlement(pier=9, settlement=settlement_mm / 1000)],
        )
        .map(lambda r: r * 1e-6)
        .to_stress(config.bridge)
    )
    responses.units = "N/mm²"
    plot.top_view_bridge(bridge=config.bridge, abutments=True, piers=True)
    plot.contour_responses(config, responses=responses, decimals=2, interp=(200, 60))
    plt.legend(loc="upper right", borderaxespad=0)
    plt.title(f"{settlement_mm} mm pier settlement")
    print("Calculated stress from pier settlement")

    # Temperature effect.
    plt.subplot(3, 1, 2)
    print(f"deck_points.shape = {np.array(deck_points).shape}")
    temp_effect = temperature.effect(
        config=config,
        response_type=response_type,
        points=deck_points,
        temps_bt=([temp_bottom], [temp_top]),
    ).T[0]
    print(f"temp_effect.shape = {np.array(temp_effect).shape}")
    responses = (
        Responses(
            response_type=response_type, responses=list(zip(temp_effect, deck_points))
        )
        .without_nan_inf()
        .without(without.edges(c=config, radius=2))
        .to_stress(config.bridge)
    )
    responses.units = "N/mm²"
    plot.top_view_bridge(config.bridge, abutments=True, piers=True)
    plot.contour_responses(config, responses=responses, decimals=2, interp=(200, 60))
    plt.legend(loc="upper right", borderaxespad=0)
    plt.title(f"T_bot, T_top = {temp_bottom}°C, {temp_top}°C")
    # plt.title(f"{top_str} stress\nbottom, top = {temp_bottom}, {temp_top}")
    print("Calculated stress from temperature")

    # Cracked concrete.
    plt.subplot(3, 1, 3)
    time = truck1.time_at(x=53, bridge=config.bridge)
    truck1.load = 400
    assert truck1.total_load() == 400
    cracked_config = transverse_crack().crack(config)
    responses = (
        sim.responses.load(
            config=cracked_config,
            response_type=response_type,
            point_loads=truck1.wheel_track_loads(config, [time])[0],
        )
        .map(lambda r: r * 1e-6)
        .to_stress(config.bridge)
    )
    responses.units = "N/mm²"
    plot.top_view_bridge(bridge=config.bridge, abutments=True, piers=True)
    plot.contour_responses(
        config=config, responses=responses, decimals=2, interp=(200, 60)
    )
    plt.legend(loc="upper right", borderaxespad=0)
    plot.top_view_vehicles(config, vehicles=[truck1], time=time, wheels=True)
    plt.title(f"{int(truck1.load)} kN vehicle over a 0.5 m crack zone")

    plt.suptitle(f"Stress {response_type.ss_direction()} for 3 scenarios")
    equal_lims("x", 3, 1)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(
        config.get_image_path(
            "validation", f"stress-strength-{response_type.value}.pdf"
        )
    )
    plt.close()
