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
    # response_type = ResponseType.YTranslation
    # num_ulss = np.arange(50, 600, 1)
    # chosen_uls = 400

    # # Point load for each wheel of truck 1 in the experimental campaign.
    # # wagen1_times = [wagen1.time_at(x=x, bridge=c.bridge) for x in wagen1_x_pos()]

    # wagen1_time = wagen1.time_at(x=c.bridge.x_max - (c.bridge.length / 2), bridge=c.bridge)

    # # For each amount of unit load simulations, collect a function. The function
    # # will calculate the response at a given point based on the amount of unit
    # # load simulations/bins.
    # response_to_trucks = []
    # for num_uls in num_ulss:
    #     c.il_num_loads = num_uls
    #     print_i(f"Number of ULS = {num_uls}")
    #     # A list of loads. This is nested in here because it depends on the
    #     # setting of 'il_num_loads'.
    #     truck_loads = flatten(wagen1.to_wheel_track_loads(c=c, time=time), PointLoad)
    #     print_i(f"Truck loads = {truck_loads}")
    #     responses = []
    #     for wheel_track_load in truck_loads:
    #         sim_responses = load_fem_responses(
    #             c=c,
    #             response_type=response_type,
    #             sim_runner=OSRunner(c),
    #             sim_params=SimParams(
    #                 ploads=[wheel_bin_load], response_types=[response_type],
    #             ),
    #         )
    #         responses.append(sim_responses)

    #     def response_to_truck(_responses):
    #         def _response_to_truck(point: Point):
    #             response = 0
    #             for sim_responses, frac in _responses:
    #                     response += sim_responses.at_deck(point, interp=True)
    #             return response

    #         return _response_to_truck

    #     response_to_trucks[-1].append(response_to_truck(responses))

    # # Create a plot for each truck position.
    # plt.landscape()
    # point = [
    #         Point(x=x, y=0, z=c.bridge.z(wheel_load.z_frac))
    #         for x in np.linspace(
    #             max(truck_x_pos, c.bridge.x_min),
    #             min(truck_x_pos, c.bridge.x_max),
    #             num_points,
    #         )
    #     ]
    #     # for p_i, point in enumerate(points):
    #         plt.subplot(num_points, 1, p_i + 1)
    #         responses = []
    #         min_after_chosen, max_after_chosen = np.inf, -np.inf
    #         for num_uls, response_func in zip(num_ulss, response_funcs):
    #             responses.append(response_func(point))
    #             if num_uls >= chosen_uls:
    #                 if responses[-1] < min_after_chosen:
    #                     min_after_chosen = responses[-1]
    #                 if responses[-1] > max_after_chosen:
    #                     max_after_chosen = responses[-1]
    #         units_str = response_type.units()
    #         if response_type == ResponseType.YTranslation:
    #             responses = np.array(responses) * 1000
    #             min_after_chosen *= 1000
    #             max_after_chosen *= 1000
    #             units_str = "mm"
    #         difference = np.around(max_after_chosen - min_after_chosen, 3)[0]
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
    #     plt.tight_layout()
    #     plt.savefig(
    #         c.get_image_path(
    #             "paramselection", safe_str(f"uls-truck-x-{truck_x_pos:.2f}") + ".pdf"
    #         )
    #     )
    #     plt.close()


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
