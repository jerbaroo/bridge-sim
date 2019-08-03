"""General plotting functions.

More specific plotting functions are found in other modules.

"""
import copy
from collections import OrderedDict
from typing import Callable, List

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.ticker import ScalarFormatter
from scipy import stats

from classify.data.responses import responses_to_mv_load, times_on_bridge_
from config import Config
from fem.run import FEMRunner
from model import *
from util import *

bridge_color = "limegreen"
lane_color = "gold"
load_color = "crimson"
pier_color = "limegreen"
rebar_color = "crimson"
response_color = "mediumorchid"
response_axle_color = "cornflowerblue"


def sci_format_y_axis(points: int=1):
    """Format y-axis ticks in scientific style."""

    class ScalarFormatterForceFormat(ScalarFormatter):
        def _set_format(self):
            self.format = f"%1.{points}f"

    plt.gca().yaxis.set_major_formatter(ScalarFormatterForceFormat())
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))


def _plot_load_deck_side(
        bridge: Bridge, load: Load, normalize_vehicle_height: bool=False):
    """Plot a load on the side of the deck (but don't plot the deck)."""
    xl = load.x_frac * bridge.length
    if load.is_point_load():
        plt.plot(xl, 0, "o", color=load_color)
    # A vehicle load.
    else:
        width = sum(load.axle_distances)
        height = width / 2
        if normalize_vehicle_height and not load.is_point_load():
            y_min, y_max = plt.ylim()
            y_length = np.abs(y_min - y_max)
            x_min, x_max = plt.xlim()
            x_length = np.abs(x_min - x_max)
            width_frac = width / x_length
            height_frac = (height / width) * width_frac
            height = height_frac * y_length
        plt.gca().add_patch(patches.Rectangle(
            (xl, 0), width, height, facecolor=load_color))


def plot_bridge_deck_side(
        bridge: Bridge, loads: List[Load]=[], save: str=None, show: bool=False,
        equal_axis: bool=True, normalize_vehicle_height: bool=False):
    """Plot the deck of a bridge from the side with optional loads.

    Args:
        equal_axis: bool, if true set both axes to have the same scale.
        normalize_vehicle_height: bool, plot the height of a vehicle relative
            to the height of the y-axis.

    """
    plt.hlines(0, 0, bridge.length, color=bridge_color)
    plt.plot(
        [f.x_frac * bridge.length for f in bridge.fixed_nodes],
        [0 for _ in range(len(bridge.fixed_nodes))],
        "o", color=pier_color)
    if equal_axis: plt.axis("equal")
    for load in loads:
        _plot_load_deck_side(
            bridge, load, normalize_vehicle_height=normalize_vehicle_height)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def _plot_load_deck_top(bridge: Bridge, load: Load):
    xl = load.x_frac * bridge.length
    z_center = bridge.lanes[load.lane].z_center()
    if load.is_point_load():
        plt.plot(xl, z_center, "o", color=load_color)
    # A vehicle load.
    else:
        z_center = bridge.lanes[load.lane].z_center()
        zb = z_center - (load.axle_width / 2)
        plt.gca().add_patch(patches.Rectangle(
            (xl, zb), sum(load.axle_distances), load.axle_width,
            facecolor=load_color))


def plot_bridge_deck_top(bridge: Bridge, loads: List[Load]=[], save: str=None,
                         show: bool=False):
    """Plot the deck of a bridge from the top."""
    plt.hlines([0, bridge.width], 0, bridge.length, color=bridge_color)
    plt.vlines([0, bridge.length], 0, bridge.width, color=bridge_color)
    for lane in bridge.lanes:
        plt.gca().add_patch(
            patches.Rectangle(
                (0, lane.z0), bridge.length, lane.z1 - lane.z0,
                facecolor=lane_color))
    for load in loads:
        _plot_load_deck_top(bridge, load)
    plt.axis("equal")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def plot_bridge_first_section(
        bridge: Bridge, save: str=None, show: bool=False):
    """Plot the first cross section of a bridge."""
    plot_section(bridge.sections[0], save=save, show=show)


def plot_section(section: Section, save: str=None, show: bool=False):
    """Plot the cross section of a bridge."""
    for p in section.patches:
        plt.plot([p.p0.z, p.p1.z], [p.p0.y, p.p0.y], color=bridge_color)  # Bottom.
        plt.plot([p.p0.z, p.p0.z], [p.p0.y, p.p1.y], color=bridge_color)  # Left.
        plt.plot([p.p0.z, p.p1.z], [p.p1.y, p.p1.y], color=bridge_color)  # Top.
        plt.plot([p.p1.z, p.p1.z], [p.p1.y, p.p0.y], color=bridge_color,  # Right.
                 label=p.material.name)
    for l in section.layers:
        for point in l.points():
            plt.plot([point.z], [point.y], "o", color=rebar_color,
                     label=l.material.name)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.axis("equal")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def animate_translation(x, y, num_elems=300, node_step=0.2, spans=7):
    """Show an animation of translation of the nodes."""

    def plot_translation(t):
        """Return a plot of model translation at given time index."""
        p = np.arange(0, num_elems * node_step + node_step, node_step)
        plt.ylim(top=np.amax(y), bottom=np.amin(y))
        plot_bridge(num_elems=num_elems, node_step=node_step, spans=spans)
        plt.plot([p[i] + x[t][i] for i in range(len(p))], y[t], color="blue")

    animate_plot(len(x), plot_translation)


# TODO: Plot multiple response lines.
def animate_bridge_response(
        bridge: Bridge, responses, time_step: float,
        response_type: ResponseType, mv_loads: List[MovingLoad]=[],
        save: str=None, show: bool=False):
    """Animate a bridge's response to moving loads.

    Args:
        responses: a 3 or 4 dimensional list. The first index is the load,
            followed by time, then x position. Then there is either a float
            representing the response to the load, or a list of responses
            for each vehicle axle.

    """
    per_axle = not isinstance(responses[0][0][0], float)
    responses_per_load = (
        np.apply_along_axis(sum, axis=3, arr=responses) if per_axle
        else responses)
    # Find max and min of all responses.
    top, bottom = np.amax(responses_per_load), np.amin(responses_per_load)
    # Ensure top == -bottom, so bridge is vertically centered.
    top, bottom = max(top, -bottom), min(bottom, -top)
    # Non-moving loads, updated and plotted every timestep.
    loads = [copy.deepcopy(mv_load.load) for mv_load in mv_loads]

    def update_loads(t):
        for i, mv_load in enumerate(mv_loads):
            loads[i].x_frac = mv_load.x_frac_at(t * time_step, bridge)
            assert 0 <= loads[i].x_frac and loads[i].x_frac <= 1

    # TODO: This should be a global function.
    def plot_bridge_response(t):
        update_loads(t)
        plt.ylim(top=top, bottom=bottom)

        # Plot responses for each moving load.
        for i in range(len(mv_loads)):
            t_load_responses = responses[i][t]
            x_axis = bridge.x_axis_equi(len(t_load_responses))

            # Plot responses per axle and one sum of responses.
            if per_axle:
                for axle in range(mv_loads[i].load.num_axles):
                    print_d(f"axle_num = {axle}")
                    plt.plot(
                        x_axis, list(map(lambda x: x[axle], t_load_responses)),
                        color=response_axle_color, linewidth=1)
                print_d(f"Response per axle")
                plt.plot(
                    x_axis, responses_per_load[i][t], color=response_color,
                    linewidth=1)

            # Plot one response for the moving load. 
            else:
                print(type(t_load_responses[0]))
                plt.plot(x_axis, t_load_responses)

        # Plot the bridge and loads.
        plot_bridge_deck_side(
            bridge, loads=loads, equal_axis=False,
            normalize_vehicle_height=True)
        sci_format_y_axis()
        response_name = response_type_name(response_type).capitalize()
        plt.title(f"{response_name} at {t * time_step:.1f}s")
        plt.xlabel("x-axis (m)")
        plt.ylabel(f"{response_name} ({response_type_units(response_type)})")
        plt.gcf().set_size_inches(16, 10)

    print_w(f"num time steps = {len(responses[0])}")
    print_w(f"interval = {time_step}")
    print_w(f"total time = {len(responses[0]) * time_step}")
    animate_plot(
        len(responses[0]), plot_bridge_response, time_step, save, show)


def animate_plot(
        frames: int, plot: Callable[[int], None], time_step: float,
        save: str=None, show: bool=True):
    """Generate an animation with given plotting function."""

    def animate(t):
        """Plot at the given time index."""
        plt.cla()
        plot(t)

    plot(0)
    anim = FuncAnimation(plt.gcf(), animate, frames, interval=time_step * 1000)
    if save:
        writer = FFMpegWriter()
        anim.save(save, writer=writer)
    if show: plt.show()
    if save or show:
        plt.close()


def animate_mv_load(
        c: Config, mv_load: MovingLoad, response_type: ResponseType,
        fem_runner: FEMRunner, time_step: float=0.1, time_end: float=20,
        num_x_fracs: int=100, per_axle: bool=False, save: str=None,
        show: bool=False):
    """Animate the bridge's response to a moving load."""
    times = times_on_bridge_(
        c, mv_load, time_step=time_step, time_end=time_end)
    at = [Point(x=c.bridge.x(x_frac))
          for x_frac in np.linspace(0, 1, num_x_fracs)]
    responses = responses_to_mv_load(
        c, mv_load, response_type, fem_runner, times, at, per_axle=per_axle)
    animate_bridge_response(
        c.bridge, [responses], time_step, response_type, mv_loads=[mv_load],
        save=save, show=show)


def plot_hist(
        data, bins: int=None, density: bool=True, kde: bool=False,
        title: str=None, ylabel: str=None, xlabel: str=None, save: str=None,
        show: bool=False):
    """Plot a histogram and optionally a KDE of given data."""
    _, x, _ = plt.hist(data, bins=bins, density=density)
    data_kde = stats.gaussian_kde(data)
    if kde: plt.plot(x, data_kde(x))
    if title: plt.title(title)
    if ylabel: plt.ylabel(ylabel)
    if xlabel: plt.xlabel(xlabel)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def plot_kde_and_kde_samples_hist(
        data, samples=5000, title=None, ylabel=None, xlabel=None, save=None,
        show=None):
    """Plot the KDE of given data and a histogram of samples from the KDE."""
    kde = stats.gaussian_kde(data)
    x = np.linspace(data.min(), data.max(), 100)
    sampler = kde_sampler(data)
    plt.hist([next(sampler) for _ in range(samples)], bins=25, density=True)
    plt.plot(x, kde(x))
    if title: plt.title(title)
    if ylabel: plt.ylabel(ylabel)
    if xlabel: plt.xlabel(xlabel)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
