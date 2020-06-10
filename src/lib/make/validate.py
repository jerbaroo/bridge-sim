import os

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim.model import Config, PointLoad, Point, ResponseType
from bridge_sim.sim.responses import responses_to_traffic_array
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
    wagen1_times = np.linspace(
        -end_time, end_time * 2, int((end_time * 3) / c.sensor_hz)
    )
    wagen1_loads = [
        flatten(truck1.wheel_track_loads(c=c, time=time), PointLoad)
        for time in wagen1_times
    ]

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
    responses_truck1 = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=wagen1_loads),
        response_type=ResponseType.YTrans,
        points=displa_points,
    ).T * 1E-3
    for s_i, sensor_responses in enumerate(responses_truck1):
        plt.subplot(len(displa_points), 1, s_i + 1)
        # Find the center of the plot, minimum point in the data.
        data_center = 0
        for i in range(len(sensor_responses)):
            if sensor_responses[i] < sensor_responses[data_center]:
                data_center = i
        sensor_responses = sensor_responses * 1000
        plot_data = sensor_responses[data_center - side:data_center + side]
        x = np.arange(len(plot_data)) / 700
        plt.plot(x, plot_data, c="b", label="simulation")

    # Results from experiment.
    center = 13500
    plot_offsets = [-1350, -850, 0]
    for s_i, displa_label in enumerate(displa_labels):
        plt.subplot(len(displa_points), 1, s_i + 1)
        with open(os.path.join(project_dir(), f"data/validation/experiment/D1a-{displa_label}.txt")) as f:
            data = list(map(float, f.readlines()))
        print_i(f"Total Y translation data length = {len(data)}")
        new_center = center + plot_offsets[s_i]
        plot_data = data[new_center - side:new_center + side]
        x = np.arange(len(plot_data)) / 700
        plt.plot(x, plot_data, c="r", label="experiment")

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
    responses_truck1 = responses_to_traffic_array(
        c=c,
        traffic_array=loads_to_traffic_array(c=c, loads=wagen1_loads),
        response_type=ResponseType.StrainXXB,
        points=strain_points,
    ).T * 1E-3
    for s_i, sensor_responses in enumerate(responses_truck1):
        plt.subplot(len(strain_points), 1, s_i + 1)
        data_center = 0
        for i in range(len(sensor_responses)):
            if sensor_responses[i] > sensor_responses[data_center]:
                data_center = i
        plt.plot(sensor_responses[data_center - side:data_center + side], c="b", label="simulation")

    # Results from experiment.
    center = 13000
    plot_offsets = [-400, -290, -170]
    for s_i, strain_label in enumerate(strain_labels):
        plt.subplot(len(strain_points), 1, s_i + 1)
        with open(os.path.join(project_dir(), f"data/validation/experiment/D1a-{strain_label}.txt")) as f:
            data = list(map(float, f.readlines()))
        print_i(f"Total strain data length = {len(data)}")
        new_center = center + plot_offsets[s_i]
        plt.plot(data[new_center - side:new_center + side], c="r", label="experiment")

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


def stress_strength_plot(c: Config, top: bool):
    """Plot the difference of tensile strength and stress under load."""
    original_c = c
    plt.portrait()
    response_type = ResponseType.StrainT if top else ResponseType.Strain
    settlement = 3
    temp_bottom, temp_top = 21, 30
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(
            # c.bridge.x_min, c.bridge.x_max, num=10
            c.bridge.x_min,
            c.bridge.x_max,
            num=int(c.bridge.length * 3),
        )
        for z in np.linspace(
            # c.bridge.z_min, c.bridge.z_max, num=10
            c.bridge.z_min,
            c.bridge.z_max,
            num=int(c.bridge.width * 3),
        )
    ]

    # Pier settlement.
    plt.subplot(3, 1, 1)
    c, sim_params = pier_disp_damage([(9, settlement / 1000)]).use(original_c)
    responses = (
        load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=sim_params,
        )
        .resize()
        .to_stress(c.bridge)
    )
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=responses, decimals=2)
    plt.legend(loc="upper right", borderaxespad=0)
    plt.title(f"{settlement} mm pier settlement")
    print("Calculated stress from pier settlement")

    # Temperature effect.
    plt.subplot(3, 1, 2)
    c = original_c
    print(f"deck_points.shape = {np.array(deck_points).shape}")
    temp_effect = temperature.effect(
        c=c,
        response_type=response_type,
        points=deck_points,
        temps_bt=([temp_bottom], [temp_top]),
    ).T[0]
    print(f"temp_effect.shape = {np.array(temp_effect).shape}")
    responses = (
        Responses(
            response_type=response_type,
            responses=[
                (temp_effect[p_ind], deck_points[p_ind])
                for p_ind in range(len(deck_points))
                if not np.isnan(temp_effect[p_ind])
            ],
        )
        .without(remove=without.edges(c=c, radius=2))
        .to_stress(c.bridge)
    )
    top_view_bridge(c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=responses, decimals=2)
    plt.legend(loc="upper right", borderaxespad=0)
    plt.title(f"T_bot, T_top = {temp_bottom}°C, {temp_top}°C")
    # plt.title(f"{top_str} stress\nbottom, top = {temp_bottom}, {temp_top}")
    print("Calculated stress from temperature")

    # Cracked concrete.
    plt.subplot(3, 1, 3)
    time = wagen1.time_at(x=52, bridge=c.bridge)
    print(f"wagen1.total_kn() = {wagen1.kn}")
    wagen1.kn = 400
    loads = wagen1.to_wheel_track_loads(c=c, time=time, flat=True)
    c, sim_params = transverse_crack().use(original_c)

    c, sim_params = HealthyDamage().use(original_c)
    sim_params.ploads = loads
    responses = (
        load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=sim_params,
        )
        .resize()
        .to_stress(c.bridge)
    )
    top_view_bridge(bridge=c.bridge, compass=False, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=responses, decimals=2)
    plt.legend(loc="upper right", borderaxespad=0)
    # plt.title(f"Top stress: cracked concrete\nunder a {int(wagen1.kn)} kN vehicles")
    plt.title(f"{int(wagen1.total_kn())} kN vehicle")

    plt.suptitle(f"Stress {response_type.ss_direction()} for 3 scenarios")
    equal_lims("x", 3, 1)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(
        original_c.get_image_path(
            "validation", f"stress-strength-{response_type.name()}.pdf"
        )
    )
    plt.close()
