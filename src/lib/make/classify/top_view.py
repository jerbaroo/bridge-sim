import matplotlib as mpl
import numpy as np
from datetime import datetime

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.data.traffic import load_traffic
from classify.scenario.bridge import PierDispDamage
from classify.scenario.traffic import normal_traffic
from classify import temperature
from fem.responses import Responses
from fem.responses.matrix.dc import DCMatrix
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.load import Vehicle
from model.response import ResponseType
from model.scenario import to_traffic, to_traffic_array
from plot import plt
from plot.geometry import top_view_bridge
from plot.load import top_view_vehicles
from plot.responses import plot_contour_deck
from bridge_sim.util import flatten, resize_units


def top_view_plot(c: Config, max_time: int, skip: int, damage_scenario):
    response_type = ResponseType.YTranslation
    # Create the traffic.
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, traffic, traffic_array = load_traffic(
        c=c, traffic_scenario=traffic_scenario, max_time=max_time,
    )
    assert len(traffic) == traffic_array.shape[0]
    # Points on the deck to collect fem.
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(
            c.bridge.x_min, c.bridge.x_max, num=int(c.bridge.length * 2)
        )
        for z in np.linspace(
            c.bridge.z_min, c.bridge.z_max, num=int(c.bridge.width * 2)
        )
        # for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=30)
        # for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=10)
    ]
    point = Point(x=21, y=0, z=-8.4)  # Point to plot
    deck_points.append(point)
    # Traffic array to fem array.
    responses_array = responses_to_traffic_array(
        c=c,
        traffic_array=traffic_array,
        damage_scenario=damage_scenario,
        points=deck_points,
        response_type=response_type,
    )
    # Temperature effect July 1st.
    temps_2019 = temperature.load("holly-springs")
    temps_2019["temp"] = temperature.resize(temps_2019["temp"])
    effect_2019 = temperature.effect(
        c=c,
        response_type=response_type,
        points=deck_points,
        temps=temps_2019["temp"],
        solar=temps_2019["solar"],
        len_per_hour=60,
    ).T
    # The effect is ordered by time series and then by points. (104910, 301)
    assert len(effect_2019) == len(temps_2019)
    july_2019_i, july_2019_j = temperature.from_to_indices(
        temps_2019,
        datetime.fromisoformat(f"2019-10-01T00:00"),
        datetime.fromisoformat(f"2019-10-01T23:59"),
    )
    temp_effect = []
    for i in range(len(deck_points)):
        temp_effect.append(
            temperature.apply(
                # Effect for July 1st, for the current point..
                effect=effect_2019.T[i][july_2019_i:july_2019_j],
                # ..for the length of the time series.
                responses=responses_array,
            )
        )
    temp_effect = np.array(temp_effect)
    plt.subplot(2, 1, 1)
    plt.plot(effect_2019.T[-1])
    plt.subplot(2, 1, 2)
    plt.plot(temp_effect[-1])
    plt.show()
    # Determine response due to pier settlement.
    pd_response_at_point = 0
    if isinstance(damage_scenario, PierDispDamage):
        pd_expt = list(
            DCMatrix.load(c=c, response_type=response_type, fem_runner=OSRunner(c))
        )
        for pier_displacement in damage_scenario.pier_disps:
            pd_sim_responses = pd_expt[pier_displacement.pier]
            pd_response_at_point += pd_sim_responses.at_deck(point, interp=False) * (
                pier_displacement.displacement / c.pd_unit_disp
            )
    # Resize fem if applicable to response type.
    resize_f, units = resize_units(response_type.units())
    if resize_f is not None:
        responses_array = resize_f(responses_array)
        temp_effect = resize_f(temp_effect.T).T
        print(np.mean(temp_effect[-1]))
        pd_response_at_point = resize_f(pd_response_at_point)
    responses_w_temp = responses_array + temp_effect.T
    # Determine levels of the colourbar.
    amin, amax = np.amin(responses_array), np.amax(responses_array)
    # amin, amax = min(amin, -amax), max(-amin, amax)
    levels = np.linspace(amin, amax, 25)
    # All vehicles, for colour reference.
    all_vehicles = flatten(traffic, Vehicle)
    # Iterate through each time index and plot results.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)
    # Plot for each time step.
    for t_ind in range(len(responses_array))[::skip]:
        plt.landscape()
        # Plot the bridge top view.
        plt.subplot2grid((3, 1), (0, 0), rowspan=2)
        top_view_bridge(c.bridge, compass=False, lane_fill=False, piers=True)
        top_view_vehicles(
            bridge=c.bridge,
            mv_vehicles=flatten(traffic[t_ind], Vehicle),
            time=warmed_up_at + t_ind * c.sensor_hz,
            all_vehicles=all_vehicles,
        )
        responses = Responses(
            response_type=response_type,
            responses=[
                (responses_array[t_ind][p_ind], deck_points[p_ind])
                for p_ind in range(len(deck_points))
            ],
            units=units,
        )
        plot_contour_deck(c=c, responses=responses, levels=levels, mm_legend=False)
        plt.scatter(
            [point.x],
            [point.z],
            label=f"Sensor in bottom plot",
            marker="o",
            color="red",
            zorder=10,
        )
        plt.legend(loc="upper right")
        plt.title(
            f"{response_type.name()} after {np.around(t_ind * c.sensor_hz, 4)} seconds"
        )
        # Plot the fem at a point.
        plt.subplot2grid((3, 1), (2, 0))
        time = t_ind * c.sensor_hz
        plt.axvline(
            x=time, color="black", label=f"Current time = {np.around(time, 4)} s"
        )
        plt.plot(
            np.arange(len(responses_array)) * c.sensor_hz,
            responses_w_temp.T[-1],
            color="red",
            label="Total effect",
        )
        if isinstance(damage_scenario, PierDispDamage):
            plt.plot(
                np.arange(len(responses_array)) * c.sensor_hz,
                np.ones(temp_effect[-1].shape) * pd_response_at_point,
                color="green",
                label="Pier settlement effect",
            )
        plt.plot(
            np.arange(len(responses_array)) * c.sensor_hz,
            temp_effect[-1],
            color="blue",
            label="Temperature effect",
        )
        plt.ylabel(f"{response_type.name()} ({responses.units})")
        plt.xlabel("Time (s)")
        plt.title(f"{response_type.name()} at sensor in top plot")
        plt.legend(loc="upper right", framealpha=1)
        # Finally save the image.
        name = f"{damage_scenario.name}-{response_type.name()}-{t_ind}"
        plt.tight_layout()
        plt.savefig(c.get_image_path("classify/top-view", f"{name}.pdf"))
        plt.savefig(c.get_image_path("classify/top-view/png", f"{name}.png"))
        plt.close()
