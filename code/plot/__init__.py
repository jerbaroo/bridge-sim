"""General plotting functions.

More specific plotting functions are found in other modules.

"""
import copy
from collections import OrderedDict
from typing import Callable, List, Optional

import matplotlib
import matplotlib.colors as colors
import matplotlib.patches as patches
import matplotlib.pyplot as _plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.ticker import ScalarFormatter
from scipy import stats

# from classify.data.responses import responses_to_mv_vehicles, times_on_bridge
from config import Config
from fem.run import FEMRunner
from model.bridge import Bridge, Dimensions, Point, Section
from model.load import MvVehicle
from model.response import ResponseType
from util import print_d, print_i, print_w, kde_sampler

# Print debug information for this file.
D: bool = False

###### Apply modifications to matplotlib.pyplot. ##############################


def _portrait():
    matplotlib.rcParams["figure.figsize"] = (10, 16)


def _landspace():
    matplotlib.rcParams["figure.figsize"] = (16, 10)


_og_savefig = _plt.savefig
_og_show = _plt.show


def _savefig(s):
    print_i(f"Saving image to {s}")
    plt.tight_layout()
    _og_savefig(s)


def _show(*args, **kwargs):
    plt.tight_layout()
    _og_show(*args, **kwargs)


def _equal_ax_lims(plt):
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    amin, amax = min(xmin, ymin), max(xmax, ymax)
    plt.xlim((amin, amax))
    plt.ylim((amin, amax))


plt = _plt
plt.equal_ax_lims = lambda: _equal_ax_lims(plt)
plt.savefig = _savefig
plt.show = _show
plt.portrait = _portrait
plt.landscape = _landspace

SMALL_SIZE = 18
MEDIUM_SIZE = 22
BIGGER_SIZE = 26

plt.rc("font", size=SMALL_SIZE)  # Default text sizes.
plt.rc("axes", titlesize=BIGGER_SIZE)  # Axes titles.
plt.rc("axes", labelsize=MEDIUM_SIZE)  # Axes titles.
plt.rc("xtick", labelsize=SMALL_SIZE)  # X tick labels.
plt.rc("ytick", labelsize=SMALL_SIZE)  # Y tick labels.
plt.rc("legend", fontsize=SMALL_SIZE)  # Legend.
plt.rc("figure", titlesize=BIGGER_SIZE)  # Figure title


###############################################################################


parula_cmap = colors.LinearSegmentedColormap.from_list(
    "parula",
    [
        [0.2081, 0.1663, 0.5292],
        [0.2116238095, 0.1897809524, 0.5776761905],
        [0.212252381, 0.2137714286, 0.6269714286],
        [0.2081, 0.2386, 0.6770857143],
        [0.1959047619, 0.2644571429, 0.7279],
        [0.1707285714, 0.2919380952, 0.779247619],
        [0.1252714286, 0.3242428571, 0.8302714286],
        [0.0591333333, 0.3598333333, 0.8683333333],
        [0.0116952381, 0.3875095238, 0.8819571429],
        [0.0059571429, 0.4086142857, 0.8828428571],
        [0.0165142857, 0.4266, 0.8786333333],
        [0.032852381, 0.4430428571, 0.8719571429],
        [0.0498142857, 0.4585714286, 0.8640571429],
        [0.0629333333, 0.4736904762, 0.8554380952],
        [0.0722666667, 0.4886666667, 0.8467],
        [0.0779428571, 0.5039857143, 0.8383714286],
        [0.079347619, 0.5200238095, 0.8311809524],
        [0.0749428571, 0.5375428571, 0.8262714286],
        [0.0640571429, 0.5569857143, 0.8239571429],
        [0.0487714286, 0.5772238095, 0.8228285714],
        [0.0343428571, 0.5965809524, 0.819852381],
        [0.0265, 0.6137, 0.8135],
        [0.0238904762, 0.6286619048, 0.8037619048],
        [0.0230904762, 0.6417857143, 0.7912666667],
        [0.0227714286, 0.6534857143, 0.7767571429],
        [0.0266619048, 0.6641952381, 0.7607190476],
        [0.0383714286, 0.6742714286, 0.743552381],
        [0.0589714286, 0.6837571429, 0.7253857143],
        [0.0843, 0.6928333333, 0.7061666667],
        [0.1132952381, 0.7015, 0.6858571429],
        [0.1452714286, 0.7097571429, 0.6646285714],
        [0.1801333333, 0.7176571429, 0.6424333333],
        [0.2178285714, 0.7250428571, 0.6192619048],
        [0.2586428571, 0.7317142857, 0.5954285714],
        [0.3021714286, 0.7376047619, 0.5711857143],
        [0.3481666667, 0.7424333333, 0.5472666667],
        [0.3952571429, 0.7459, 0.5244428571],
        [0.4420095238, 0.7480809524, 0.5033142857],
        [0.4871238095, 0.7490619048, 0.4839761905],
        [0.5300285714, 0.7491142857, 0.4661142857],
        [0.5708571429, 0.7485190476, 0.4493904762],
        [0.609852381, 0.7473142857, 0.4336857143],
        [0.6473, 0.7456, 0.4188],
        [0.6834190476, 0.7434761905, 0.4044333333],
        [0.7184095238, 0.7411333333, 0.3904761905],
        [0.7524857143, 0.7384, 0.3768142857],
        [0.7858428571, 0.7355666667, 0.3632714286],
        [0.8185047619, 0.7327333333, 0.3497904762],
        [0.8506571429, 0.7299, 0.3360285714],
        [0.8824333333, 0.7274333333, 0.3217],
        [0.9139333333, 0.7257857143, 0.3062761905],
        [0.9449571429, 0.7261142857, 0.2886428571],
        [0.9738952381, 0.7313952381, 0.266647619],
        [0.9937714286, 0.7454571429, 0.240347619],
        [0.9990428571, 0.7653142857, 0.2164142857],
        [0.9955333333, 0.7860571429, 0.196652381],
        [0.988, 0.8066, 0.1793666667],
        [0.9788571429, 0.8271428571, 0.1633142857],
        [0.9697, 0.8481380952, 0.147452381],
        [0.9625857143, 0.8705142857, 0.1309],
        [0.9588714286, 0.8949, 0.1132428571],
        [0.9598238095, 0.9218333333, 0.0948380952],
        [0.9661, 0.9514428571, 0.0755333333],
        [0.9763, 0.9831, 0.0538],
    ],
)

default_cmap = matplotlib.cm.get_cmap("viridis")


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


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def animate_plot(
    frames: int, plot_f: Callable[[int], None], time_step: float, save: str
):
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
    anim = FuncAnimation(plt.gcf(), animate_frame, frames, interval=time_step)
    writer = FFMpegWriter()
    anim.save(save, writer=writer)


def _plot_vehicle_deck_side(
    bridge: Bridge, mv_vehicle: MvVehicle, normalize_vehicle_height: bool = False,
):
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
    plt.gca().add_patch(patches.Rectangle((xl, 0), width, height, facecolor=load_color))


def plot_bridge_deck_side(
    bridge: Bridge,
    mv_vehicles: List[MvVehicle] = [],
    equal_axis: bool = True,
    normalize_vehicle_height: bool = False,
    save: str = None,
    show: bool = False,
):
    """Plot the deck of a bridge from the side with optional vehicles.

    Args:
        equal_axis: bool, if true set both axes to have the same scale.
        normalize_vehicle_height: bool, plot the height of a vehicle relative
            to the height of the y-axis.

    """
    # A horizontal line that is the top of the bridge deck.
    plt.hlines(0, 0, bridge.length, color=Color.bridge)
    pier_x_positions = [
        (bridge.x(pier.x_frac) if bridge.dimensions == Dimensions.D2 else pier.x)
        for pier in bridge.supports
    ]
    plt.plot(pier_x_positions, [0 for _ in bridge.supports], "o", color=Color.pier)
    if equal_axis:
        plt.axis("equal")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    for mv_vehicle in mv_vehicles:
        _plot_vehicle_deck_side(
            bridge=bridge,
            mv_vehicle=mv_vehicle,
            normalize_vehicle_height=normalize_vehicle_height,
        )
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    if save or show:
        plt.close()


def plot_bridge_first_section(bridge: Bridge, save: str = None, show: bool = False):
    """Plot the first cross section of a bridge."""
    plot_section(bridge.sections[0], save=save, show=show)


def plot_section(section: Section, save: str = None, show: bool = False):
    """Plot the cross section of a bridge."""
    for p in section.patches:
        plt.plot([p.p0.z, p.p1.z], [p.p0.y, p.p0.y], color=bridge_color)  # Bottom.
        plt.plot([p.p0.z, p.p0.z], [p.p0.y, p.p1.y], color=bridge_color)  # Left.
        plt.plot([p.p0.z, p.p1.z], [p.p1.y, p.p1.y], color=bridge_color)  # Top.
        plt.plot(
            [p.p1.z, p.p1.z],
            [p.p1.y, p.p0.y],
            color=bridge_color,  # Right.
            label=p.material.name,
        )
    for l in section.layers:
        for point in l.points():
            plt.plot(
                [point.z], [point.y], "o", color=rebar_color, label=l.material.name,
            )
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.axis("equal")
    plt.xlabel("z position (m)")
    plt.ylabel("y position (m)")
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    if save or show:
        plt.close()


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
    c: Config,
    responses,
    response_type: ResponseType,
    mv_vehicles: List[MvVehicle] = [],
    save: str = None,
    show: bool = False,
):
    """Animate a bridge's response, of one response type, to moving vehicles.

    Args:
        responses: a 3 or 4 dimensional list. The first index is the vehicle,
            followed by time, then x position. Then there is either a float
            representing the response to the vehicle, or a list of responses for
            each vehicle axle.

    """
    per_axle = not isinstance(responses[0][0][0], float)
    responses_per_vehicle = (
        np.apply_along_axis(sum, axis=3, arr=responses) if per_axle else responses
    )
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
                        x_axis,
                        list(map(lambda x: x[axle], t_vehicle_responses)),
                        color=response_axle_color,
                        linewidth=1,
                    )
                print_d(D, f"Response per axle")
                plt.plot(
                    x_axis,
                    responses_per_vehicle[i][t],
                    color=response_color,
                    linewidth=1,
                )

            # Plot one response for the moving vehicle.
            else:
                plt.plot(x_axis, t_vehicle_responses)

        # Plot the bridge and vehicles.
        plot_bridge_deck_side(
            c.bridge,
            vehicles=vehicles,
            equal_axis=False,
            normalize_vehicle_height=True,
        )
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
        frames=len(responses[0]),
        plot=plot_bridge_response,
        time_step=c.time_step,
        save=save,
        show=show,
    )


def animate_mv_vehicle(
    c: Config,
    mv_vehicle: MvVehicle,
    response_type: ResponseType,
    fem_runner: FEMRunner,
    num_x_fracs: int = 100,
    per_axle: bool = False,
    save: str = None,
    show: bool = False,
):
    """Animate the bridge's response to a moving vehicle."""
    times = list(times_on_bridge(c=c, mv_vehicles=[mv_vehicles]))
    at = [Point(x=c.bridge.x(x_frac)) for x_frac in np.linspace(0, 1, num_x_fracs)]
    responses = responses_to_mv_vehicles(
        c=c,
        mv_vehicles=[mv_vehicles],
        response_types=[response_type],
        fem_runner=fem_runner,
        times=times,
        at=at,
        per_axle=per_axle,
    )
    # Reshape to have only a single response type and moving vehicle.
    new_shape = [d for d in responses.shape if d != 1]
    responses = responses.reshape(new_shape)
    animate_bridge_response(
        c=c,
        responses=[responses],
        response_type=response_type,
        mv_vehicles=[mv_vehicles],
        save=save,
        show=show,
    )


def plot_hist(
    data,
    bins: int = None,
    density: bool = True,
    kde: bool = False,
    title: str = None,
    ylabel: str = None,
    xlabel: str = None,
    save: str = None,
    show: bool = False,
):
    """Plot a histogram and optionally a KDE of given data."""
    _, x, _ = plt.hist(data, bins=bins, density=density)
    data_kde = stats.gaussian_kde(data)
    if kde:
        plt.plot(x, data_kde(x))
    if title:
        plt.title(title)
    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    if save or show:
        plt.close()


def plot_kde_and_kde_samples_hist(
    data,
    samples: int = 5000,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
    xlabel: Optional[str] = None,
    save: Optional[str] = None,
    show: bool = False,
):
    """Plot the KDE of given data and a histogram of samples from the KDE."""
    kde = stats.gaussian_kde(data)
    x = np.linspace(data.min(), data.max(), 100)
    sampler = kde_sampler(data)
    plt.hist([next(sampler) for _ in range(samples)], bins=25, density=True)
    plt.plot(x, kde(x))
    if title:
        plt.title(title)
    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    if save or show:
        plt.close()
