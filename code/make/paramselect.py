import numpy as np

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


def number_of_uls_plot(c: Config):
    """Plot error as a function of number of unit load simulations."""
    num_truck_positions = 1
    response_type = ResponseType.YTranslation
    num_ulss = np.arange(50, 600, 1)
    chosen_uls = 400

    # Point load for each wheel of truck 1 in the experimental campaign.
    wagen1_times = [wagen1.time_at(x=x, bridge=c.bridge) for x in wagen1_x_pos()]

    # For each amount of unit load simulations, collect a function for each
    # truck position. The function will calculate the response at a given
    # point based on the amount of unit load simulations/bins.
    response_to_trucks = []
    for num_uls in num_ulss:
        c.il_num_loads = num_uls
        response_to_trucks.append([])
        print_i(f"Number of ULS = {num_uls}")
        # A list of loads per truck position. This is nested in here because it
        # depends on the setting of 'il_num_loads'. Because a load is calculated
        # based on where the bins are positioned.
        truck_loads = [
            flatten(wagen1.to_point_loads_binned(c=c, time=time), PointLoad)
            for time in times
        ][:num_truck_positions]
        print_i(f"Truck loads = {truck_loads[0]}")
        # For each truck position, get a list of SimResponses per wheel bin.
        for truck_i, wheel_bin_loads in enumerate(truck_loads):
            print_i(f"Truck position index = {truck_i}")
            responses = []
            for wheel_bin_load in wheel_bin_loads:
                sim_responses = load_fem_responses(
                    c=c,
                    response_type=response_type,
                    sim_runner=OSRunner(c),
                    sim_params=SimParams(
                        ploads=[wheel_bin_load],
                        response_types=[response_type],
                    ),
                )
                responses[-1].append((sim_responses, bin_frac))

            def response_to_truck(_responses):
                def _response_to_truck(point: Point):
                    response = 0
                    for wheel_responses in _responses:
                        for sim_responses, frac in wheel_responses:
                            response += sim_responses.at_deck(point, interp=True) * frac
                    return response

                return _response_to_truck

            response_to_trucks[-1].append(response_to_truck(responses))

    # Response functions ordered by truck then number of ULS.
    response_to_trucks = np.array(response_to_trucks).T
    # Create a plot for each truck position.
    plt.landscape()
    for response_funcs, truck_x_pos in zip(response_to_trucks, wagen1_x_pos()):
        num_points = 1
        points = [
            Point(x=x, y=0, z=c.bridge.z(wheel_load.z_frac))
            for x in np.linspace(
                max(truck_x_pos, c.bridge.x_min),
                min(truck_x_pos, c.bridge.x_max),
                num_points,
            )
        ]
        for p_i, point in enumerate(points):
            plt.subplot(num_points, 1, p_i + 1)
            responses = []
            min_after_chosen, max_after_chosen = np.inf, -np.inf
            for num_uls, response_func in zip(num_ulss, response_funcs):
                responses.append(response_func(point))
                if num_uls >= chosen_uls:
                    if responses[-1] < min_after_chosen:
                        min_after_chosen = responses[-1]
                    if responses[-1] > max_after_chosen:
                        max_after_chosen = responses[-1]
            units_str = response_type.units()
            if response_type == ResponseType.YTranslation:
                responses = np.array(responses) * 1000
                min_after_chosen *= 1000
                max_after_chosen *= 1000
                units_str = "mm"
            difference = np.around(max_after_chosen - min_after_chosen, 3)[0]
            plt.axvline(
                chosen_uls,
                label=f"Max. difference after {chosen_uls} ULS = {difference} {units_str}",
                color="black",
            )
            plt.axhline(min_after_chosen, color="black")
            plt.axhline(max_after_chosen, color="black")
            plt.legend()
            plt.plot(num_ulss, responses)
            plt.xlabel("Unit load simulations (ULS) per wheel track")
            plt.ylabel(f"{response_type.name()} ({units_str})")
            plt.title(
                f"{response_type.name()} at x = {np.around(point.x, 2)} m, z = {np.around(point.z, 2)} m."
                f"\nTruck 1's front axle at x = {np.around(truck_x_pos, 2)} m, on the south lane of Bridge 705."
            )
        plt.tight_layout()
        plt.savefig(
            c.get_image_path(
                "paramselection", safe_str(f"uls-truck-x-{truck_x_pos:.2f}") + ".pdf"
            )
        )
        plt.close()
