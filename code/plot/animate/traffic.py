"""Animate a traffic scenario."""
from itertools import chain
from typing import Callable, List

from classify.data.scenarios import normal_traffic
from model.bridge import Bridge
from model.load import MvVehicle
from model.scenario import Traffic
from plot import animate_plot, plt
from plot.geom import top_view_bridge
from plot.load import top_view_vehicles


def animate_traffic_top_view(
        bridge: Bridge, title: str, traffic: Traffic, time_step: float, save: str):
    """Animate traffic from a top view.

    Args:
        bridge: Bridge, the bridge on which the vehicles move.
        title: str, title of the plot.
        traffic: Traffic, vehicles on the bridge at each time step.
        time_step, float, time step between each frame.
        save: str, filepath where to save the animation.

    """
    all_vehicles = list(chain.from_iterable(traffic))

    def plot_f(time_index):
        plt.title(title)
        top_view_bridge(bridge)
        top_view_vehicles(
            bridge=bridge, mv_vehicles=traffic[time_index],
            all_vehicles=all_vehicles, time=time_index * time_step)

    animate_traffic(
        traffic=traffic, time_step=time_step, plot_f=plot_f, save=save)


def animate_traffic(
        traffic: Traffic, time_step: float,
        plot_f: Callable[[List[MvVehicle]], None], save: str):
    """Animate traffic with given plotting function."""
    frames = len(traffic)
    animate_plot(frames=frames, plot_f=plot_f, time_step=time_step, save=save)
