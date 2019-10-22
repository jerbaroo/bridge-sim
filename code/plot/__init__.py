"""General plotting functions.

More specific plotting functions are found in other modules.

"""
import copy
from collections import OrderedDict
from typing import Callable, List, Optional

import matplotlib.patches as patches
import matplotlib.pyplot as _plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.ticker import ScalarFormatter
from scipy import stats

from classify.data.responses import responses_to_mv_vehicles, times_on_bridge
from config import Config
from fem.run import FEMRunner
from model.bridge import Bridge, Dimensions, Point, Section
from model.load import MvVehicle, PointLoad, Vehicle
from model.response import Event, ResponseType
from util import print_d, print_w, kde_sampler

# Print debug information for this file.
D: bool = False

###### Apply modifications to matplotlib.pyplot. ##############################


_og_savefig = _plt.savefig


def _savefig(*args, **kwargs):
    _plt.gcf().set_size_inches(16, 10)
    _plt.tight_layout()
    _og_savefig(*args, **kwargs)


_og_show = _plt.show


def _show(*args, **kwargs):
    _plt.gcf().set_size_inches(16, 10)
    _plt.tight_layout()
    _og_show(*args, **kwargs)


plt = _plt
plt.savefig = _savefig
plt.show = _show


###############################################################################

class Color:
    bridge = "limegreen"
    lane = "gold"
    load = "crimson"
    pier = "limegreen"
    rebar = "crimson"
    response = "mediumorchid"
    response_axle = "cornflowerblue"


def sci_format_y_axis(points: int = 1):
    """Format y-axis ticks in scientific style."""

    class ScalarFormatterForceFormat(ScalarFormatter):
        def _set_format(self):
            self.format = f"%1.{points}f"

    plt.gca().yaxis.set_major_formatter(ScalarFormatterForceFormat())
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))


def animate_plot(frames: int, plot_f: Callable[[int], None], time_step: float, save: str):
    """Generate an animation with given plotting function.

    Args:
        frames: int, amount of frames to animate.
        plot_f: Callable[[float], None], plot at current time step.
        time_step: float, time step between each frame.
        save: str, filepath where to save the animation.

    """

    def animate_frame(t):
        """Plot at the given time index."""
        plt.cla()
        plot_f(t)

    plot_f(0)
    anim = FuncAnimation(
        plt.gcf(), animate_frame, frames, interval=time_step)
    writer = FFMpegWriter()
    anim.save(save, writer=writer)


def _plot_vehicle_deck_side(
        bridge: Bridge, mv_vehicle: MvVehicle,
        normalize_vehicle_height: bool = False):
    """Plot a vehicle on the side of the deck (but don't plot the deck)."""
    xl = bridge.x(x_frac=mv_vehicle.init_x_frac)
    # Width and height on the plot.
    width = mv_vehicle.length
    height = width / 2
    if normalize_vehicle_height:
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
        bridge: Bridge, mv_vehicles: List[MvVehicle] = [], equal_axis: bool = True,
        normalize_vehicle_height: bool = False, save: str = None,
        show: bool = False):
    """Plot the deck of a bridge from the side with optional vehicles.

    Args:
        equal_axis: bool, if true set both axes to have the same scale.
        normalize_vehicle_height: bool, plot the height of a vehicle relative
            to the height of the y-axis.

    """
    # A horizontal line that is the top of the bridge deck.
    plt.hlines(0, 0, bridge.length, color=bridge_color)
    pier_x_positions = [
        (bridge.x(pier.x_frac)
         if bridge.dimensions == Dimensions.D2
         else pier.x)
        for pier in bridge.supports]
    plt.plot(
        pier_x_positions, [0 for _ in bridge.supports], "o", color=pier_color)
    if equal_axis: plt.axis("equal")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    for mv_vehicle in mv_vehicles:
        _plot_vehicle_deck_side(
            bridge=bridge, mv_vehicle=mv_vehicle,
            normalize_vehicle_height=normalize_vehicle_height)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def plot_bridge_first_section(
        bridge: Bridge, save: str = None, show: bool = False):
    """Plot the first cross section of a bridge."""
    plot_section(bridge.sections[0], save=save, show=show)


def plot_section(section: Section, save: str = None, show: bool = False):
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
    plt.xlabel("z position (m)")
    plt.ylabel("y position (m)")
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


def animate_bridge_response(
        c: Config, responses, response_type: ResponseType,
        mv_vehicles: List[MvVehicle] = [], save: str = None, show: bool = False):
    """Animate a bridge's response, of one response type, to moving vehicles.

    Args:
        responses: a 3 or 4 dimensional list. The first index is the vehicle,
            followed by time, then x position. Then there is either a float
            representing the response to the vehicle, or a list of responses for
            each vehicle axle.

    """
    per_axle = not isinstance(responses[0][0][0], float)
    responses_per_vehicle = (
        np.apply_along_axis(sum, axis=3, arr=responses) if per_axle
        else responses)
    # Find max and min of all responses.
    top, bottom = np.amax(responses_per_vehicle), np.amin(responses_per_vehicle)
    # Ensure top == -bottom, so bridge is vertically centered.
    top, bottom = max(top, -bottom), min(bottom, -top)
    # Non-moving vehicles, updated and plotted every timestep.
    vehicles = [copy.deepcopy(mv_vehicle) for mv_vehicle in mv_vehicles]

    def update_vehicles(t):
        for i, mv_vehicle in enumerate(mv_vehicles):
            vehicles[i].x_frac = mv_vehicle.x_frac_at(t * c.time_step, c.bridge)
            assert 0 <= vehicles[i].x_frac and vehicles[i].x_frac <= 1

    # TODO: This should be a global function.
    def plot_bridge_response(t):
        update_vehicles(t)
        plt.ylim(top=top, bottom=bottom)

        # Plot responses for each moving vehicle.
        for i in range(len(mv_vehicles)):
            t_vehicle_responses = responses[i][t]
            x_axis = c.bridge.x_axis_equi(len(t_vehicle_responses))

            # Plot responses per axle and one sum of responses.
            if per_axle:
                for axle in range(mv_vehicles[i].num_axles):
                    print_d(D, f"axle_num = {axle}")
                    plt.plot(
                        x_axis, list(map(lambda x: x[axle], t_vehicle_responses)),
                        color=response_axle_color, linewidth=1)
                print_d(D, f"Response per axle")
                plt.plot(
                    x_axis, responses_per_vehicle[i][t], color=response_color,
                    linewidth=1)

            # Plot one response for the moving vehicle.
            else:
                plt.plot(x_axis, t_vehicle_responses)

        # Plot the bridge and vehicles.
        plot_bridge_deck_side(
            c.bridge, vehicles=vehicles, equal_axis=False,
            normalize_vehicle_height=True)
        sci_format_y_axis()
        response_name = response_type.name().capitalize()
        plt.title(f"{response_name} at {t * c.time_step:.1f}s")
        plt.xlabel("x-axis (m)")
        plt.ylabel(f"{response_name} ({response_type.units()})")
        plt.gcf().set_size_inches(16, 10)

    print_w(f"num time steps = {len(responses[0])}")
    print_w(f"interval = {c.time_step}")
    print_w(f"total time = {len(responses[0]) * c.time_step}")
    animate_plot(
        frames=len(responses[0]), plot=plot_bridge_response,
        time_step=c.time_step, save=save, show=show)


def animate_mv_vehicle(
        c: Config, mv_vehicle: MvVehicle, response_type: ResponseType,
        fem_runner: FEMRunner, num_x_fracs: int = 100, per_axle: bool = False,
        save: str = None, show: bool = False):
    """Animate the bridge's response to a moving vehicle."""
    times = list(times_on_bridge(c=c, mv_vehicles=[mv_vehicles]))
    at = [Point(x=c.bridge.x(x_frac))
          for x_frac in np.linspace(0, 1, num_x_fracs)]
    responses = responses_to_mv_vehicles(
        c=c, mv_vehicles=[mv_vehicles], response_types=[response_type],
        fem_runner=fem_runner, times=times, at=at, per_axle=per_axle)
    # Reshape to have only a single response type and moving vehicle.
    new_shape = [d for d in responses.shape if d != 1]
    responses = responses.reshape(new_shape)
    animate_bridge_response(
        c=c, responses=[responses], response_type=response_type,
        mv_vehicles=[mv_vehicles], save=save, show=show)


def plot_hist(
        data, bins: int = None, density: bool = True, kde: bool = False,
        title: str = None, ylabel: str = None, xlabel: str = None,
        save: str = None, show: bool = False):
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
        data, samples: int = 5000, title: Optional[str] = None,
        ylabel: Optional[str] = None, xlabel: Optional[str] = None,
        save: Optional[str] = None, show: bool = False):
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
