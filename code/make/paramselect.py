import numpy as np
from scipy.signal import savgol_filter

from classify.vehicle import wagen1, wagen1_x_pos
from config import Config
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.load import PointLoad
from model.response import ResponseType
from plot import plt
from util import clean_generated, flatten, print_i, safe_str
from validate.campaign import displa_sensor_xz


def number_of_uls_plot(c: Config):
    """Plot error as a function of number of unit load simulations."""
    if not c.shorten_paths:
        raise ValueError("This plot requires --shorten-paths true")
    response_type = ResponseType.YTranslation
    num_ulss = np.arange(100, 1500, 10)
    chosen_uls = 100
    point = Point(x=c.bridge.x_max - (c.bridge.length / 2), y=0, z=-8.4)
    wagen1_time = wagen1.time_at(x=point.x, bridge=c.bridge)
    print_i(f"Wagen 1 time at x = {point.x:.3f} is t = {wagen1_time:.3f}")

    # Collect the data.
    total_load = []
    num_loads = []
    responses = []
    for num_uls in num_ulss:
        c.il_num_loads = num_uls
        print_i(f"Number of ULS = {num_uls}")
        # Nested in here because it depends on the setting of 'il_num_loads'.
        truck_loads = flatten(wagen1.to_wheel_track_loads(c=c, time=wagen1_time), PointLoad)
        print_i(f"Truck loads = {truck_loads}")
        num_loads.append(len(truck_loads))
        total_load.append(sum(map(lambda l: l.kn, truck_loads)))
        sim_responses = load_fem_responses(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            sim_params=SimParams(ploads=truck_loads, response_types=[response_type])
        )
        responses.append(sim_responses.at_deck(point, interp=True) * 1000)

    # Plot the data.
    plt.landscape()
    # Determine the min and max after chosen number of ULS.
    min_after_chosen, max_after_chosen = np.inf, -np.inf
    for i, (num_uls, response) in enumerate(zip(num_ulss, responses)):
        if num_uls >= chosen_uls:
            if responses[i] < min_after_chosen:
                min_after_chosen = responses[i]
            if responses[i] > max_after_chosen:
                max_after_chosen = responses[i]
    difference = np.around(max_after_chosen - min_after_chosen, 3)
    print_i(f"Difference in responses = {difference}")
    plt.plot(num_ulss, responses)
    plt.title(f"Displacement to Truck 1 as a function of ULS")
    plt.ylabel("Displacement (m)")
    plt.xlabel("ULS")
    plt.tight_layout()
    plt.savefig(c.get_image_path("paramselection", "uls.pdf"))
    plt.close()
    plt.plot(num_ulss, total_load)
    plt.savefig(c.get_image_path("paramselection", "uls-verify-total-load.pdf"))
    plt.close()
    plt.plot(num_ulss, num_loads)
    plt.savefig(c.get_image_path("paramselection", "uls-verify-num-loads.pdf"))
    plt.close()
    #         plt.axvline(
    #             chosen_uls,
    #             label=f"Max. difference after {chosen_uls} ULS = {difference} {units_str}",
    #             color="black",
    #         )
    #         plt.axhline(min_after_chosen, color="black")
    #         plt.axhline(max_after_chosen, color="black")
    #         plt.legend()
    #         plt.plot(num_ulss, responses)
    #         plt.xlabel("Unit load simulations (ULS) per wheel track")
    #         plt.ylabel(f"{response_type.name()} ({units_str})")
    #         plt.title(
    #             f"{response_type.name()} at x = {np.around(point.x, 2)} m, z = {np.around(point.z, 2)} m."
    #             f"\nTruck 1's front axle at x = {np.around(truck_x_pos, 2)} m, on the south lane of Bridge 705."
    #         )


def experiment_noise(c: Config):
    """Plot noise from dynamic test 1"""
    plt.portrait()
    # Find points of each sensor.
    displa_labels = ["U13", "U26", "U29"]
    displa_points = []
    for displa_label in displa_labels:
        sensor_x, sensor_z = displa_sensor_xz(displa_label)
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
        smooth = savgol_filter(data, 21, 3)
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
    plt.savefig(c.get_image_path("params", "noise.pdf"))
    plt.close()
