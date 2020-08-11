import numpy as np
from scipy.signal import savgol_filter

from bridge_sim.internal.plot import plt
from bridge_sim.internal.validate import _displa_sensor_xz, _strain_sensor_xz
from bridge_sim.model import Config, Point, PointLoad, ResponseType
from bridge_sim.vehicles import truck1
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.responses import load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from bridge_sim.util import flatten, print_i


def number_of_uls_plot(c: Config):
    """Plot error as a function of number of unit load simulations."""
    if not c.shorten_paths:
        raise ValueError("This plot requires --shorten-paths true")
    response_type = ResponseType.YTranslation
    num_ulss = np.arange(100, 2000, 10)
    chosen_uls = 600
    point = Point(x=c.bridge.x_max - (c.bridge.length / 2), y=0, z=-8.4)
    wagen1_time = truck1.time_at(x=point.x, bridge=c.bridge)
    print_i(f"Wagen 1 time at x = {point.x:.3f} is t = {wagen1_time:.3f}")

    # Determine the reference value.
    truck_loads = flatten(
        truck1.to_point_load_pw(time=wagen1_time, bridge=c.bridge), PointLoad
    )
    print_i(f"Truck loads = {truck_loads}")
    sim_responses = load_fem_responses(
        c=c,
        response_type=response_type,
        sim_runner=OSRunner(c),
        sim_params=SimParams(ploads=truck_loads, response_types=[response_type]),
    )
    ref_value = sim_responses.at_deck(point, interp=True) * 1000
    print_i(f"Reference value = {ref_value}")

    # Collect the data.
    total_load = []
    num_loads = []
    responses = []
    for num_uls in num_ulss:
        c.il_num_loads = num_uls
        # Nested in here because it depends on the setting of 'il_num_loads'.
        truck_loads = flatten(
            truck1.to_wheel_track_loads(c=c, time=wagen1_time), PointLoad
        )
        num_loads.append(len(truck_loads))
        total_load.append(sum(map(lambda l: l.kn, truck_loads)))
        sim_responses = load_fem_responses(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            sim_params=SimParams(ploads=truck_loads, response_types=[response_type]),
        )
        responses.append(sim_responses.at_deck(point, interp=True) * 1000)

    # Plot the raw fem, then error on the second axis.
    plt.landscape()
    # plt.plot(num_ulss, fem)
    # plt.ylabel(f"{response_type.name().lower()} (mm)")
    plt.xlabel("ULS")
    error = np.abs(np.array(responses) - ref_value).flatten() * 100
    # ax2 = plt.twinx()
    plt.plot(num_ulss, error)
    plt.ylabel("Error (%)")
    plt.title(f"Error in {response_type.name()} to Truck 1 as a function of ULS")
    # Plot the chosen number of ULS.
    chosen_error = np.interp([chosen_uls], num_ulss, error)[0]
    plt.axhline(
        chosen_error,
        label=f"At {chosen_uls} ULS, error = {np.around(chosen_error, 2)} %",
        color="black",
    )
    plt.axhline(
        0, color="red", label="Response from direct simulation (no wheel tracks)"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(c.get_image_path("paramselection", "uls.pdf"))
    plt.close()
    # Additional verification plots.
    plt.plot(num_ulss, total_load)
    plt.savefig(c.get_image_path("paramselection", "uls-verify-total-load.pdf"))
    plt.close()
    plt.plot(num_ulss, num_loads)
    plt.savefig(c.get_image_path("paramselection", "uls-verify-num-loads.pdf"))
    plt.close()
    #         plt.axhline(min_after_chosen, color="black")
    #         plt.axhline(max_after_chosen, color="black")
    #         plt.legend()
    #         plt.plot(num_ulss, fem)
    #         plt.xlabel("Unit load simulations (ULS) per wheel track")
    #         plt.ylabel(f"{response_type.name()} ({units_str})")
    #         plt.title(
    #             f"{response_type.name()} at x = {np.around(point.x, 2)} m, z = {np.around(point.z, 2)} m."
    #             f"\nTruck 1's front axle at x = {np.around(truck_x_pos, 2)} m, on the south lane of Bridge 705."
    #         )


def experiment_noise(c: Config):
    """Plot displacement and strain noise from dynamic test 1"""
    ################
    # Displacement #
    ################
    plt.portrait()
    # Find points of each sensor.
    displa_labels = ["U13", "U26", "U29"]
    displa_points = []
    for displa_label in displa_labels:
        sensor_x, sensor_z = _displa_sensor_xz(displa_label)
        displa_points.append(Point(x=sensor_x, y=0, z=sensor_z))
    # For each sensor plot and estimate noise.
    side = 700
    for s_i, displa_label in enumerate(displa_labels):
        # First plot the signal, and smoothed signal.
        plt.subplot(len(displa_points), 2, (s_i * 2) + 1)
        with open(f"validation/experiment/D1a-{displa_label}.txt") as f:
            data = list(map(float, f.readlines()))
        # Find the center of the plot, minimum point in first 15000 points.
        data_center = 0
        for i in range(15000):
            if data[i] < data[data_center]:
                data_center = i
        data = data[data_center - side : data_center + side]
        smooth = savgol_filter(data, 31, 3)
        plt.plot(data, linewidth=1)
        plt.plot(smooth, linewidth=1)
        plt.ylim(-0.8, 0.3)
        plt.title(f"{displa_label} in dynamic test")
        # Then plot subtraction of smoothed from noisey.
        plt.subplot(len(displa_points), 2, (s_i * 2) + 2)
        noise = data - smooth
        plt.plot(noise, label=f"σ = {np.around(np.std(noise), 4)}")
        plt.legend()
        plt.title(f"Noise from {displa_label}")
    plt.tight_layout()
    plt.savefig(c.get_image_path("params", "noise-displa.pdf"))
    plt.close()

    ##########
    # Strain #
    ##########

    plt.portrait()
    # Find points of each sensor.
    strain_labels = ["T1", "T10", "T11"]
    strain_points = []
    for strain_label in strain_labels:
        sensor_x, sensor_z = _strain_sensor_xz(strain_label)
        strain_points.append(Point(x=sensor_x, y=0, z=sensor_z))
    # For each sensor plot and estimate noise.
    side = 700
    xmin, xmax = np.inf, -np.inf
    for s_i, strain_label in enumerate(strain_labels):
        # First plot the signal, and smoothed signal.
        plt.subplot(len(strain_points), 2, (s_i * 2) + 1)
        with open(f"validation/experiment/D1a-{strain_label}.txt") as f:
            data = list(map(float, f.readlines()))
        # Find the center of the plot, minimum point in first 15000 points.
        data_center = 0
        for i in range(15000):
            if data[i] < data[data_center]:
                data_center = i
        data = data[data_center - side : data_center + side]
        smooth = savgol_filter(data, 31, 3)
        plt.plot(data, linewidth=1)
        plt.plot(smooth, linewidth=1)
        plt.title(f"{strain_label} in dynamic test")
        # Then plot subtraction of smoothed from noisey.
        plt.subplot(len(strain_points), 2, (s_i * 2) + 2)
        noise = data - smooth
        plt.plot(noise, label=f"σ = {np.around(np.std(noise), 4)}")
        plt.legend()
        plt.title(f"Noise from {strain_label}")
    plt.tight_layout()
    plt.savefig(c.get_image_path("params", "noise-strain.pdf"))
    plt.close()
