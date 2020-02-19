import matplotlib as mpl
import numpy as np

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.scenario.traffic import normal_traffic
from classify.temperature import get_temperature_effect, load_temperature_month
from fem.responses import Responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.load import Vehicle
from model.response import ResponseType
from model.scenario import to_traffic, to_traffic_array
from plot import plt
from plot.geometry import top_view_bridge
from plot.load import top_view_vehicles
from plot.responses import plot_contour_deck
from util import flatten, resize_units


def top_view_plot(c: Config, max_time: int, skip: int, damage_scenario):
    response_type = ResponseType.YTranslation
    # Create the 'TrafficSequence' and 'TrafficArray'.
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence = traffic_scenario.traffic_sequence(bridge=c.bridge, max_time=max_time)
    traffic = to_traffic(c=c, traffic_sequence=traffic_sequence, max_time=max_time)
    traffic_array = to_traffic_array(c=c, traffic_sequence=traffic_sequence, max_time=max_time)
    assert len(traffic) == traffic_array.shape[0]
    # Points on the deck to collect responses.
    deck_points = [
        Point(x=x, y=0, z=z)
        # for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=int(c.bridge.length * 2))
        # for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=int(c.bridge.width * 2))
        for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=30)
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=10)
    ]
    point = Point(x=21, y=0, z=-8.4)  # Point to plot
    deck_points.append(point)
    # Traffic array to responses array.
    responses_array = responses_to_traffic_array(
        c=c,
        traffic_array=traffic_array,
        damage_scenario=damage_scenario,
        points=deck_points,
        response_type=response_type,
        sim_runner=OSRunner(c),
    )
    # Temperature effect.
    temps = load_temperature_month("may", offset=10)["temp"]
    # print(f"Temps = {temps}")
    temp_effect = get_temperature_effect(
        c=c,
        response_type=response_type,
        points=deck_points,
        temps=temps,
        responses=responses_array.T,
        speed_up=60,
    )
    print(temp_effect.shape)
    print(responses_array.shape)
    responses_array = responses_array + temp_effect.T
    # Resize responses if applicable to response type.
    resize_f, units = resize_units(response_type.units())
    if resize_f is not None:
        responses_array = resize_f(responses_array)
        temp_effect = resize_f(temp_effect)
    # Determine levels of the colourbar.
    amin, amax = np.amin(responses_array), np.amax(responses_array)
    # amin, amax = min(amin, -amax), max(-amin, amax)
    levels = np.linspace(amin, amax, 25)
    # All vehicles, for colour reference.
    all_vehicles = flatten(traffic, Vehicle)
    # Iterate through each time index and plot results.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)
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
            f"{response_type.name()} at time {np.around(t_ind * c.sensor_hz, 4)} s"
        )
        # Plot the responses at a point.
        plt.subplot2grid((3, 1), (2, 0))
        time = t_ind * c.sensor_hz
        plt.axvline(x=time, color="black", label=f"Current time = {np.around(time, 4)} s")
        plt.plot(
            np.arange(len(responses_array)) * c.sensor_hz,
            temp_effect[-1],
            color="blue",
            label="Temperature effect",
        )
        plt.plot(
            np.arange(len(responses_array)) * c.sensor_hz,
            responses_array.T[-1],
            color="red",
            label="Temp. + traffic effect"
        )
        plt.ylabel(f"{response_type.name()} ({responses.units})")
        plt.xlabel("Time (s)")
        plt.title(f"{response_type.name()} at sensor in top plot")
        plt.legend(loc="upper right", framealpha=1)
        # Finally save the image.
        plt.tight_layout()
        plt.savefig(c.get_image_path("classify/top-view", f"{t_ind}.pdf"))
        plt.savefig(c.get_image_path("classify/top-view/png", f"{t_ind}.png"))
        plt.close()
