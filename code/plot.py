""""Plot a Bridge."""
from collections import OrderedDict

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from model import *

bridge_color = "green"
lane_color = "red"
pier_color = "green"


def plot_bridge_deck_side(b: Bridge, bridge_color=bridge_color,
                          pier_color=pier_color, show=True):
    """Plot the deck of a bridge from the side."""
    plt.hlines(0, 0, b.length, color=bridge_color)
    plt.plot(
        np.linspace(0, b.length, len(b.fixed_nodes)),
        [0 for _ in range(len(b.fixed_nodes))],
        "o", color=pier_color)
    if show:
        plt.show()


def plot_bridge_deck_top(b: Bridge, bridge_color=bridge_color,
                         lane_color=lane_color, show=True):
    """Plot the deck of a bridge from the top."""
    plt.hlines([0, b.width], 0, b.length, color=bridge_color)
    plt.vlines([0, b.length], 0, b.width, color=bridge_color)
    for lane in b.lanes:
        plt.gca().add_patch(
            patches.Rectangle((0, lane.z0), b.length, lane.z1 - lane.z0,
                              facecolor=lane_color))
    if show:
        plt.show()


def plot_bridge_first_section(b: Bridge, show=True):
    """Plot the first cross section of a bridge."""
    plot_section(b.sections[0], show=show)


def plot_section(s: Section, color=bridge_color, point_color="r", show=True):
    """Plot the cross section of a bridge."""
    for p in s.patches:
        plt.plot([p.p0.z, p.p1.z], [p.p0.y, p.p0.y], color=color)  # Bottom.
        plt.plot([p.p0.z, p.p0.z], [p.p0.y, p.p1.y], color=color)  # Left.
        plt.plot([p.p0.z, p.p1.z], [p.p1.y, p.p1.y], color=color)  # Top.
        plt.plot([p.p1.z, p.p1.z], [p.p1.y, p.p0.y], color=color,  # Right.
                 label=p.material.name)
    for l in s.layers:
        for point in l.points():
            plt.plot([point.z], [point.y], "o", color=point_color,
                     label=l.material.name)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    if show:
        plt.show()


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
        plot_bridge(bridge)
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


if __name__ == "__main__":
    plot_bridge_deck_side(bridge_705)
    plot_bridge_deck_top(bridge_705)
    plot_bridge_first_section(bridge_705)
