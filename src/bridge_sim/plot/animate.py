"""Animate a traffic scenario."""
from typing import Callable, List, Tuple, Optional

import bridge_sim.plot
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
from bridge_sim.crack import CrackDeck
from bridge_sim.shrinkage import CementClass
from bridge_sim.sim.responses import without
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.spatial import distance

from bridge_sim import sim, plot
from bridge_sim.plot.util import legend_marker_size
from bridge_sim.sim.model import Responses
from bridge_sim.sim.run import ulm_xzs
from bridge_sim.model import Config, Point, ResponseType, Vehicle, PierSettlement
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
    config: Config,
    traffic_sequence: TrafficSequence,
    response_type: ResponseType,
    units: str,
    save: str,
    with_creep: bool,
    xz: Tuple[float, float] = (18, -8.4),
    pier_settlement: List[Tuple[PierSettlement, PierSettlement]] = [],
    weather: Optional[pd.DataFrame] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    install_day: Optional[int] = None,
    start_day: Optional[int] = None,
    end_day: Optional[int] = None,
    cement_class: CementClass = CementClass.Normal,
    crack: Optional[Tuple[CrackDeck, int]] = None,
    psi: Tuple[float, float, float] = [1, 1, 1],
    cmap=cm.get_cmap("RdBu"),
    without_edges: int = 0,
):
    x, z = xz
    mul = 1e6 if response_type.is_strain() else 1e3
    traffic = traffic_sequence.traffic()
    traffic_array = traffic_sequence.traffic_array()
    # Determine points at which to collect responses.
    without_edges = (
        (lambda _: False)
        if without_edges == 0
        else without.edges(config, without_edges)
    )
    deck_points = [
        p
        for p in [
            Point(x=x, y=0, z=z)
            for x in np.linspace(config.bridge.x_min, config.bridge.x_max, num=100)
            for z in np.linspace(config.bridge.z_min, config.bridge.z_max, num=60)
        ]
        if not without_edges(p)
    ]
    # Find the closest point to these coordinates.
    point_index = 0
    for _index in range(len(deck_points)):
        p = deck_points[point_index]
        i = deck_points[_index]
        if distance.euclidean([x, z], [i.x, i.z]) < distance.euclidean(
            [x, z], [p.x, p.z]
        ):
            point_index = _index
    point = deck_points[point_index]
    # Collect all the different kinds of responses.
    (
        ll_responses,
        ps_responses,
        temp_responses,
        shrinkage_responses,
        creep_responses,
    ) = sim.responses.to(
        config=config,
        points=deck_points,
        traffic_array=traffic_array,
        response_type=ResponseType.YTrans,
        with_creep=with_creep,
        pier_settlement=pier_settlement,
        weather=weather,
        start_date=start_date,
        end_date=end_date,
        install_day=install_day,
        start_day=start_day,
        end_day=end_day,
        ret_all=True,
        cement_class=cement_class,
        crack=crack,
        psi=psi,
    )
    # Resize responses for plotting.
    ll_responses *= mul
    ps_responses *= mul
    temp_responses *= mul
    shrinkage_responses *= mul
    creep_responses *= mul
    total_responses = (
        ll_responses
        + ps_responses
        + temp_responses
        + shrinkage_responses
        + creep_responses
    )
    # Calculate Matplotlib norm.
    min_response, max_response = np.amin(ll_responses), np.amax(ll_responses)
    vmin, vmax = min(min_response, -max_response), max(max_response, -min_response)
    response_norm = colors.Normalize(vmin=vmin, vmax=vmax)
    # Determine vehicles.
    vehicles_at_time = [flatten(t, Vehicle) for t in traffic]
    all_vehicles = flatten(traffic, Vehicle)

    def plot_f(time_index):
        # Top plot of the moving vehicles.
        plt.landscape()
        plt.subplot2grid((3, 1), (0, 0), 2, 1)
        plt.title(
            f"{response_type.name()} on {config.bridge.name.title().replace('-', ' ')}"
        )
        bridge_sim.plot.top_view_bridge(
            config.bridge, edges=True, piers=True, units="m"
        )
        plot.contour_responses(
            config=config,
            responses=Responses(
                response_type=response_type,
                responses=list(zip(ll_responses.T[time_index], deck_points)),
            ),
            cmap=cmap,
            norm=response_norm,
            mm_legend=False,
            cbar=False,
            levels=50,
        )
        plt.xlim((config.bridge.x_min, config.bridge.x_max))
        plt.scatter(
            [point.x],
            [point.z],
            c="red",
            s=30,
            label="sensor in bottom plot",
            zorder=100,
        )
        plot.top_view_vehicles(
            config=config,
            vehicles=vehicles_at_time[time_index],
            all_vehicles=all_vehicles,
            time=traffic_sequence.times[time_index],
            wheels=True,
        )
        legend_marker_size(
            plt.legend(
                facecolor="white",
                loc="upper right",
                framealpha=1,
                fancybox=False,
                borderaxespad=0,
                labelspacing=0.1,
            ),
            30,
        )

        # Bottom plot of the total load on the bridge.
        plt.subplot2grid((3, 1), (2, 0), 1, 1)
        lw = 2
        plt.plot(
            traffic_sequence.times,
            ll_responses[point_index],
            c="xkcd:purple",
            label="traffic",
            lw=lw,
        )
        plt.plot(
            traffic_sequence.times,
            ps_responses[point_index],
            c="tab:blue",
            label="pier settlement",
            lw=lw,
        )
        plt.plot(
            traffic_sequence.times,
            temp_responses[point_index],
            c="tab:orange",
            label="temperature",
            lw=lw,
        )
        plt.plot(
            traffic_sequence.times,
            shrinkage_responses[point_index],
            c="tab:green",
            label="shrinkage",
            lw=lw,
        )
        plt.plot(
            traffic_sequence.times,
            creep_responses[point_index],
            c="magenta",
            label="creep",
            lw=lw,
        )
        plt.plot(
            traffic_sequence.times,
            total_responses[point_index],
            c="red",
            label="total",
            lw=lw,
        )
        plt.xlabel("Time (s)")
        plt.ylabel(units)
        plt.axvline(
            x=traffic_sequence.start_time + time_index * time_step,
            c="black",
            label="current time",
            lw=lw,
        )
        y_min, y_max = plt.ylim()
        plt.ylim(min(y_min, -y_max), max(y_max, -y_min))
        plt.legend(
            facecolor="white",
            loc="upper right",
            framealpha=1,
            fancybox=False,
            borderaxespad=0,
            labelspacing=0.1,
        )
        plt.tight_layout()

        # Add a color bar.
        plt.gcf().subplots_adjust(right=0.75)
        cbar_ax = plt.gcf().add_axes([0.8, 0.1, 0.01, 0.8])
        cbar = plt.gcf().colorbar(
            cm.ScalarMappable(norm=response_norm, cmap=cmap), cax=cbar_ax,
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
        bridge_sim.plot.top_view_bridge(config.bridge, edges=True, piers=True)
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
        bridge_sim.plot.top_view_bridge(config.bridge, edges=True, piers=True)
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
