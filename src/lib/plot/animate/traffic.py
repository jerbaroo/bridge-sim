"""Animate a traffic scenario."""
from itertools import chain
from typing import Callable, List

import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors

from config import Config
from classify.data.responses import responses_to_traffic
from fem.run import FEMRunner
from model.bridge import Bridge, Point
from model.load import MvVehicle
from model.response import ResponseType
from model.scenario import DamageScenario, Traffic
from plot import animate_plot, plt
from plot.geom import top_view_bridge
from plot.load import top_view_vehicles
from plot.responses import plot_contour_deck
from bridge_sim.util import print_i


def animate_traffic_top_view(
    c: Config,
    bridge: Bridge,
    traffic: Traffic,
    start_time: float,
    time_step: float,
    fem_runner: FEMRunner,
    response_type: ResponseType,
    traffic_name: str,
    bridge_scenario: DamageScenario,
    save: str,
):
    """Animate traffic from a top view with contour and total weight.

    Args:
        bridge: Bridge, the bridge on which the vehicles move.
        traffic: Traffic, vehicles on the bridge at each time step.
        start_time: float, time at which the traffic simulation starts.
        time_step, float, time step between each frame.
        fem_runner: FEMRunner, FE program used to run the simulations.
        response_type: ResponseType, type of sensor response to record.
        traffic_name: str, name of the traffic scenario.
        bridge_scenario: DamageScenario, scenarios scenario of the bridge.
        save: str, filepath where to save the animation.

    """
    # First convert the inner list of lanes into a flat list of vehicles.
    # traffic = list(map(lambda l: list(chain.from_iterable(l)), traffic))
    print(np.array(traffic).shape)

    all_vehicles = list(chain.from_iterable(traffic))
    total_kn = [sum(v.total_kn() for v in t) for t in traffic]
    times = np.array(range(len(traffic))) * time_step + start_time
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=10)
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=10)
    ]
    traffic_responses, min_response, max_response = responses_to_traffic(
        c=c,
        traffic=traffic,
        bridge_scenario=bridge_scenario,
        start_time=start_time,
        time_step=time_step,
        points=deck_points,
        response_type=response_type,
        fem_runner=fem_runner,
        min_max=True,
    )
    min_response = min(min_response, -max_response)
    max_response = max(max_response, -min_response)
    response_norm = colors.Normalize(vmin=min_response, vmax=max_response)

    def plot_f(time_index):
        # Top plot of the moving vehicles.
        plt.subplot2grid((3, 1), (0, 0), 2, 1)
        plt.title(f"{response_type.name()} on {bridge.name} {traffic_name}")
        top_view_bridge(bridge, lane_fill=False)
        top_view_vehicles(
            bridge=bridge,
            mv_vehicles=traffic[time_index],
            all_vehicles=all_vehicles,
            time=time_index * time_step + start_time,
        )
        contour_cmap = plot_contour_deck(
            c=c, responses=traffic_responses[time_index], y=0, norm=response_norm,
        )
        plt.xlim((bridge.x_min, bridge.x_max))

        # Bottom plot of the total load on the bridge.
        plt.subplot2grid((3, 1), (2, 0), 1, 1)
        plt.plot(times, total_kn)
        plt.xlabel("time")
        plt.ylabel("kilo Newton")
        plt.axvline(x=start_time + time_index * time_step, color="red")
        plt.tight_layout()

        # Add a color bar.
        plt.gcf().subplots_adjust(right=0.75)
        cbar_ax = plt.gcf().add_axes([0.80, 0.1, 0.01, 0.8])
        cbar = plt.gcf().colorbar(
            cm.ScalarMappable(norm=response_norm, cmap=contour_cmap), cax=cbar_ax,
        )
        cbar.set_label(response_type.units(short=False))

    animate_traffic(traffic=traffic, time_step=time_step, plot_f=plot_f, save=save)


def animate_traffic(
    traffic: Traffic,
    time_step: float,
    plot_f: Callable[[int], None],
    save: str,
):
    """Animate traffic with given plotting function."""
    frames = len(traffic)

    def _plot_f(time_index):
        print_i(f"Animating time = {time_index * time_step:.3f}", end="\r")
        plot_f(time_index)

    animate_plot(frames=frames, plot_f=_plot_f, time_step=time_step, save=save)

