import matplotlib as mpl
import numpy as np

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import HealthyDamage
from classify.scenario.traffic import normal_traffic
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
from util import flatten


def top_view_plot(c: Config, max_time: int, skip: int):
    response_type = ResponseType.YTranslation
    # Create the 'TrafficSequence' and 'TrafficArray'.
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence = traffic_scenario.traffic_sequence(
        bridge=c.bridge, max_time=max_time
    )
    traffic = to_traffic(
        c=c, traffic_sequence=traffic_sequence, max_time=max_time)
    traffic_array = to_traffic_array(
        c=c, traffic_sequence=traffic_sequence, max_time=max_time
    )
    assert len(traffic) == traffic_array.shape[0]
    # Points on the deck to collect responses.
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=10)
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=10)
    ]
    # Traffic array to responses array.
    responses_array = responses_to_traffic_array(
        c=c,
        traffic_array=traffic_array,
        damage_scenario=HealthyDamage(),
        points=deck_points,
        response_type=response_type,
        sim_runner=OSRunner(c),
    )
    amin, amax = np.amin(responses_array), np.amax(responses_array)
    amin = min(amin, -amax), max(-amin, amax)
    levels = np.linspace(amin, amax, 50)
    # All vehicles, for colour reference.
    all_vehicles = flatten(traffic, Vehicle)
    # Iterate through each time index and plot results.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)
    for t_ind in range(len(responses_array))[::skip]:
        top_view_bridge(c.bridge, lane_fill=False, piers=True)
        top_view_vehicles(
            bridge=c.bridge,
            mv_vehicles=flatten(traffic[t_ind], Vehicle),
            time=warmed_up_at + t_ind * c.sensor_hz,
            all_vehicles=all_vehicles,
        )
        responses = Responses(
            response_type=response_type,
            responses=[
                (responses_array[t_ind][i], deck_points[i])
                for i in range(len(deck_points))
            ],
        )
        plot_contour_deck(c=c, responses=responses, levels=levels)
        plt.title(f"{response_type.name()} at time {np.around(t_ind * c.sensor_hz, 4)} s")
        plt.tight_layout()
        plt.savefig(c.get_image_path("classify/top-view", f"{t_ind}.pdf"))
        plt.close()