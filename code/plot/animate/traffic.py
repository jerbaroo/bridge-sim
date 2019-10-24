"""Animate a traffic scenario."""
from itertools import chain
from typing import Callable, List

import numpy as np
import matplotlib.cm as cm

from classify.data.scenarios import normal_traffic
from model.bridge import Bridge
from model.load import MvVehicle
from model.scenario import Traffic
from plot import animate_plot, plt
from plot.geom import top_view_bridge
from plot.load import top_view_vehicles
from util import print_i


def animate_traffic_top_view(
        bridge: Bridge, title: str, traffic: Traffic, time_step: float,
        start_index: int, save: str):
    """Animate traffic from a top view.

    Args:
        bridge: Bridge, the bridge on which the vehicles move.
        title: str, title of the plot.
        traffic: Traffic, vehicles on the bridge at each time step.
        time_step, float, time step between each frame.
        start_index: int, time index when to start the animation.
        save: str, filepath where to save the animation.

    """
    all_vehicles = list(chain.from_iterable(traffic))
    cmap, norm = all_vehicles[0].cmap_norm(all_vehicles)
    total_kn = [sum(v.total_kn() for v in t) for t in traffic]
    times = np.array(range(len(traffic))) * time_step

    def plot_f(time_index):
        time_index += start_index

        # Plot of the moving vehicles.
        plt.subplot2grid((3, 1), (0, 0), 2, 1)
        plt.title(title)
        top_view_bridge(bridge)
        top_view_vehicles(
            bridge=bridge, mv_vehicles=traffic[time_index],
            all_vehicles=all_vehicles, time=time_index * time_step)

        # Plot of the total load on the bridge.
        plt.subplot2grid((3, 1), (2, 0), 1, 1)
        plt.plot(times, total_kn)
        plt.xlabel("time")
        plt.ylabel("kilo Newton")
        plt.axvline(x=time_index * time_step, color="red")

        plt.tight_layout()

        # Add a color bar.
        plt.gcf().subplots_adjust(right=0.8)
        cbar_ax = plt.gcf().add_axes([0.85, 0.1, 0.02, 0.8])
        cbar = plt.gcf().colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
        cbar.set_label("kilo Newton")


    animate_traffic(
        traffic=traffic[start_index:], time_step=time_step, plot_f=plot_f,
        save=save)


def animate_traffic(
        traffic: Traffic, time_step: float,
        plot_f: Callable[[List[MvVehicle]], None], save: str):
    """Animate traffic with given plotting function."""
    frames = len(traffic)

    def _plot_f(time_index):
        print_i(f"Animating time step = {time_index * time_step:.3f}", end="\r")
        plot_f(time_index)

    animate_plot(frames=frames, plot_f=_plot_f, time_step=time_step, save=save)
