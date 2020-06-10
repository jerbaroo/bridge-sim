"""Animate a traffic scenario."""
from itertools import chain
from typing import Callable, List

import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from bridge_sim.sim.model import Responses
from bridge_sim.sim.run import ulm_xzs
from lib.plot import axis_cmap_r
from matplotlib.animation import FuncAnimation, FFMpegWriter

from bridge_sim import sim, plot
from bridge_sim.model import Config, Point, ResponseType, Vehicle
from bridge_sim.traffic import Traffic, TrafficSequence, TrafficArray
from bridge_sim.util import print_i, flatten


def _animate_plot(
    frames: int, plot_f: Callable[[int], None], time_step: float, save: str
):
    """Generate an animation with given plotting function.

    Args:
        frames: amount of frames to animate.
        plot_f: function to plot at a time index.
        time_step: time step between each frame.
        save: path where to save the animation.

    """

    def animate_frame(t):
        """Plot at the given time index."""
        plt.cla()
        plot_f(t)

    plot_f(0)
    anim = FuncAnimation(plt.gcf(), animate_frame, frames, interval=time_step)
    writer = FFMpegWriter()
    anim.save(save, writer=writer)
    print_i(f"Saved animation to {save}")


def _animate_traffic(
    traffic: List, time_step: float, plot_f: Callable[[int], None], save: str,
):
    """Animate traffic with given plotting function."""
    frames = len(traffic)

    def _plot_f(time_index):
        print_i(f"Animating time = {time_index * time_step:.3f} s", end="\r")
        plot_f(time_index)

    _animate_plot(frames=frames, plot_f=_plot_f, time_step=time_step, save=save)


def animate_responses(
    config: Config, traffic_sequence: TrafficSequence,
    response_type: ResponseType, units: str, save: str,
):
    traffic = traffic_sequence.traffic()
    traffic_array = traffic_sequence.traffic_array()
    deck_points = [
        Point(x=x, y=0, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, num=10)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, num=10)
    ]
    point_index = 27
    point = deck_points[point_index]
    responses = sim.responses.responses_to_traffic_array(
        c=config,
        traffic_array=traffic_array,
        response_type=ResponseType.YTrans,
        points=deck_points,
    )
    min_response, max_response = np.amin(responses), np.amax(responses)
    min_response = min(min_response, -max_response)
    max_response = max(max_response, -min_response)
    response_norm = colors.Normalize(vmin=min_response, vmax=max_response)
    vehicles_at_time = [flatten(t, Vehicle) for t in traffic]
    all_vehicles = flatten(traffic, Vehicle)

    def plot_f(time_index):
        # Top plot of the moving vehicles.
        plt.landscape()
        plt.subplot2grid((3, 1), (0, 0), 2, 1)
        plt.title(f"{response_type.name()} on {config.bridge.name}")
        plot.top_view_bridge(config.bridge, edges=True, piers=True)
        plot.top_view_vehicles(
            config=config,
            vehicles=vehicles_at_time[time_index],
            all_vehicles=all_vehicles,
            time=traffic_sequence.times[time_index],
            wheels=True,
        )
        plot.contour_responses(
            config=config,
            responses=Responses(
                response_type=response_type,
                responses=list(zip(responses.T[time_index], deck_points)),
            ),
            cmap=axis_cmap_r,
            norm=response_norm,
            mm_legend=False,
            cbar=False,
        )
        plt.xlim((config.bridge.x_min, config.bridge.x_max))
        plt.scatter([point.x], [point.z], c="r", s=10, label="sensor in bottom plot", zorder=100)
        plt.legend(loc="upper right")

        # Bottom plot of the total load on the bridge.
        plt.subplot2grid((3, 1), (2, 0), 1, 1)
        plt.plot(traffic_sequence.times, responses[point_index], c="r", label="traffic")
        plt.xlabel("time")
        plt.ylabel(units)
        plt.axvline(x=traffic_sequence.start_time + time_index * time_step, c="black", label="current time")
        plt.legend(loc="upper right")
        plt.tight_layout()

        # Add a color bar.
        plt.gcf().subplots_adjust(right=0.75)
        cbar_ax = plt.gcf().add_axes([0.80, 0.1, 0.01, 0.8])
        cbar = plt.gcf().colorbar(
            cm.ScalarMappable(norm=response_norm, cmap=axis_cmap_r),
            cax=cbar_ax,
        )
        cbar.set_label(units)

    time_step = traffic_sequence.times[1] - traffic_sequence.times[0]
    _animate_traffic(traffic=traffic, time_step=time_step, plot_f=plot_f, save=save)


def animate_traffic(
    config: Config, traffic_sequence: TrafficSequence, traffic: Traffic, save: str,
):
    """Simple animation of "Traffic" over a bridge."""
    vehicles_at_time = [flatten(t, Vehicle) for t in traffic]
    all_vehicles = flatten(traffic, Vehicle)

    def plot_f(time_index):
        plt.title(config.bridge.name)
        plot.top_view_bridge(config.bridge, edges=True, piers=True)
        plot.top_view_vehicles(
            config=config,
            vehicles=vehicles_at_time[time_index],
            all_vehicles=all_vehicles,
            time=traffic_sequence.times[time_index],
            wheels=True,
        )
        plt.xlim((config.bridge.x_min, config.bridge.x_max))
        plt.tight_layout()

    time_step = traffic_sequence.times[1] - traffic_sequence.times[0]
    _animate_traffic(traffic=traffic, time_step=time_step, plot_f=plot_f, save=save)


def animate_traffic_array(
    config: Config,
    traffic_sequence: TrafficSequence,
    traffic_array: TrafficArray,
    save: str,
):
    """Simple animation of "TrafficArray" over a bridge."""
    cmin, cmax = np.amin(traffic_array), np.amax(traffic_array)
    response_norm = colors.Normalize(vmin=cmin, vmax=cmax)

    def plot_f(time_index):
        plt.title(config.bridge.name)
        plot.top_view_bridge(config.bridge, edges=True, piers=True)
        plt.xlim((config.bridge.x_min, config.bridge.x_max))
        slice = traffic_array[time_index]
        for (x, z), v in zip(ulm_xzs(config), slice):
            if v != 0:
                plt.scatter([x], [z], c=v, s=1, norm=response_norm)
        plt.tight_layout()

    time_step = traffic_sequence.times[1] - traffic_sequence.times[0]
    _animate_traffic(
        traffic=traffic_array, time_step=time_step, plot_f=plot_f, save=save
    )


# def animate_traffic_top_view(
#         c: Config,
#         bridge: Bridge,
#         traffic: Traffic,
#         start_time: float,
#         time_step: float,
#         response_type: ResponseType,
#         traffic_name: str,
#         save: str,
# ):
#     """Animate traffic from a top view with contour and total weight.
#
#     Args:
#         bridge: the bridge on which the vehicles move.
#         traffic: vehicles on the bridge at each time step.
#         start_time: time at which the traffic simulation starts.
#         time_step: time step between each frame.
#         response_type: type of sensor response to record.
#         traffic_name: name of the traffic scenario.
#         save: filepath where to save the animation.
#
#     """
#     traffic = [flatten(t, Vehicle) for t in traffic]
#     total_load = [sum(v.total_load() for v in t) for t in traffic]
#     times = np.array(range(len(traffic))) * time_step + start_time
#     deck_points = [
#         Point(x=x, y=0, z=z)
#         for x in np.linspace(c.bridge.x_min, c.bridge.x_max, num=10)
#         for z in np.linspace(c.bridge.z_min, c.bridge.z_max, num=10)
#     ]
#     traffic_responses, min_response, max_response = responses_to_traffic(
#         c=c,
#         traffic=traffic,
#         bridge_scenario=bridge_scenario,
#         start_time=start_time,
#         time_step=time_step,
#         points=deck_points,
#         response_type=response_type,
#         fem_runner=fem_runner,
#         min_max=True,
#     )
#     min_response = min(min_response, -max_response)
#     max_response = max(max_response, -min_response)
#     response_norm = colors.Normalize(vmin=min_response, vmax=max_response)
#
#     def plot_f(time_index):
#         # Top plot of the moving vehicles.
#         plt.subplot2grid((3, 1), (0, 0), 2, 1)
#         plt.title(f"{response_type.name()} on {bridge.name} {traffic_name}")
#         top_view_bridge(bridge, lane_fill=False)
#         top_view_vehicles(
#             bridge=bridge,
#             mv_vehicles=traffic[time_index],
#             all_vehicles=all_vehicles,
#             time=time_index * time_step + start_time,
#         )
#         contour_cmap = plot_contour_deck(
#             c=c, responses=traffic_responses[time_index], y=0, norm=response_norm,
#         )
#         plt.xlim((bridge.x_min, bridge.x_max))
#
#         # Bottom plot of the total load on the bridge.
#         plt.subplot2grid((3, 1), (2, 0), 1, 1)
#         plt.plot(times, total_kn)
#         plt.xlabel("time")
#         plt.ylabel("kilo Newton")
#         plt.axvline(x=start_time + time_index * time_step, color="red")
#         plt.tight_layout()
#
#         # Add a color bar.
#         plt.gcf().subplots_adjust(right=0.75)
#         cbar_ax = plt.gcf().add_axes([0.80, 0.1, 0.01, 0.8])
#         cbar = plt.gcf().colorbar(
#             cm.ScalarMappable(norm=response_norm, cmap=contour_cmap), cax=cbar_ax,
#         )
#         cbar.set_label(response_type.units(short=False))
#
#     animate_traffic(traffic=traffic, time_step=time_step, plot_f=plot_f, save=save)
