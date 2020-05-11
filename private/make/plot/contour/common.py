import itertools
from typing import Callable, List, Optional, Tuple

import numpy as np

from classify.data.responses import responses_to_traffic_array
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses, Responses
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array
from model.bridge import Point
from model.response import ResponseType
from model.scenario import DamageScenario
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck


def damage_scenario_traffic_plot(
    c: Config,
    response_types: List[ResponseType],
    damage_scenario: DamageScenario,
    titles: List[str],
    saves: List[str],
    times: int = 3,
):
    """Save a contour plot of a damage scenario under normal traffic."""
    # Grid of points where to record responses.
    grid_points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 4),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 4),
        )
    ]
    c, sim_params = damage_scenario.use(
        c=c, sim_params=SimParams(response_types=response_types)
    )

    # Generate a plot for each response type.
    for t, response_type, title, save in zip(
        range(times), response_types, titles, saves
    ):
        time_index = -1 + abs(t)
        response_array = responses_to_traffic_array(
            c=c,
            traffic_array=load_normal_traffic_array(c, mins=1)[0],
            response_type=response_type,
            bridge_scenario=damage_scenario,
            points=grid_points,
            sim_runner=OSRunner,
        )
        print(f"grid.shape = {np.array(grid).shape}")
        mean_response_array = np.mean(response_array, axis=0).T
        print(f"response_array.shape = {np.array(response_array).shape}")
        print(f"mean_response_array.shape = {np.array(mean_response_array).shape}")
        top_view_bridge(c.bridge, abutments=True, piers=True)
        responses = Responses.from_responses(
            response_type=response_type,
            responses=[
                (response_array[time_index][p], point)
                for p, point in enumerate(grid_points)
            ],
        )
        plot_contour_deck(c=c, responses=responses, center_norm=True, levels=100)
        plt.title(title)
        plt.save(save)
        plt.close()
