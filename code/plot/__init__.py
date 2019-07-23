"""General plotting functions.

More specific plotting functions are found in other modules.

"""
from collections import OrderedDict
from typing import List

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import ScalarFormatter
from scipy import stats

from config import Config
from model import *
from util import *


bridge_color = "green"
lane_color = "yellow"
load_color = "red"
pier_color = "green"
rebar_color = "red"


def sci_format_y_axis(points=1):
    """Format an axis' ticks in scientific style."""
    class ScalarFormatterForceFormat(ScalarFormatter):
        def _set_format(self):
            self.format = f"%1.{points}f"
    plt.gca().yaxis.set_major_formatter(ScalarFormatterForceFormat())
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))


def _plot_load_deck_side(bridge: Bridge, load: Load):
    xl = load.x_frac * bridge.length
    if load.is_point_load():
        plt.plot(xl, 0, "o", color=load_color)
    # A vehicle load.
    else:
        plt.gca().add_patch(patches.Rectangle(
            (xl, 0), sum(load.axle_distances), load.axle_width,
            facecolor=load_color))


def plot_bridge_deck_side(bridge: Bridge, loads: List[Load]=[], save: str=None,
                          show: bool=False, equal_axis: bool=True):
    """Plot the deck of a bridge from the side with optional loads."""
    plt.hlines(0, 0, bridge.length, color=bridge_color)
    plt.plot(
        [f.x_frac * bridge.length for f in bridge.fixed_nodes],
        [0 for _ in range(len(bridge.fixed_nodes))],
        "o", color=pier_color)
    for load in loads:
        _plot_load_deck_side(bridge, load)
    if equal_axis: plt.axis("equal")
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
            patches.Rectangle((0, lane.z0), bridge.length, lane.z1 - lane.z0,
                              facecolor=lane_color))
    for load in loads:
        _plot_load_deck_top(bridge, load)
    plt.axis("equal")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def plot_bridge_first_section(bridge: Bridge, save: str=None,
                              show: bool=False):
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


def plot_responses_to_mv_load_bridge_side(
        c: Config, responses: np.ndarray, mv_load: MovingLoad,
        time_step: float, at: List[Point], response_type: ResponseType
    ):
    """Plot responses to a moving load from the bridge side."""

    pass


def animate_translation(x, y, num_elems=300, node_step=0.2, spans=7):
    """Show an animation of translation of the nodes."""

    def plot_translation(t):
        """Return a plot of model translation at given time index."""
        p = np.arange(0, num_elems * node_step + node_step, node_step)
        plt.ylim(top=np.amax(y), bottom=np.amin(y))
        plot_bridge(num_elems=num_elems, node_step=node_step, spans=spans)
        plt.plot([p[i] + x[t][i] for i in range(len(p))], y[t], color="blue")

    animate_plot(len(x), plot_translation)


def animate_bridge_response(bridge: Bridge, data):
    """Show an animation of a bridge response over time."""

    def plot_bridge_response(t):
        plt.ylim(top=np.amax(data), bottom=np.amin(data))
        plt.plot(np.linspace(0, bridge.length, len(data[t])), data[t],
                 color="b")
        plot_bridge_deck_side(bridge)

    animate_plot(len(data), plot_bridge_response)


def animate_plot(frames, f):
    """Show an animation with the function f plotting data."""
    def animate(t):
        """Plot at the given time index."""
        plt.cla()
        plt.title(f"time = {t}")
        f(t)
    f(0)
    ani = FuncAnimation(plt.gcf(), animate, frames, interval=1)
    plt.show()


def plot_hist(data, bins: int=None, density: bool=True, kde: bool=False,
              title: str=None, ylabel: str=None, xlabel: str=None,
              save: str=None, show: bool=False):
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


def plot_kde_and_kde_samples_hist(data, samples=5000, title=None, ylabel=None,
                                  xlabel=None, save=None, show=None):
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
