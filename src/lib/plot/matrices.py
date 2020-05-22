"""Plot fem from the response matrices."""
import numpy as np

from config import Config
from fem.responses.matrix.il import ResponsesMatrix
from fem.responses.matrix.il import ILMatrix
from plot import plt, plot_bridge_deck_side, sci_format_y_axis
from bridge_sim.util import print_w

# Print debug information for this file.
D: bool = False


def plot_il(
    c: Config,
    resp_matrix: ILMatrix,
    expt_index: int,
    response_frac: float,
    z_frac: float,
    num_x: int,
    save: str = None,
):
    """Plot the IL for a response at some position."""
    x_fracs = np.linspace(0, 1, num_x)
    rs = [
        resp_matrix.response_to(
            x_frac=response_frac,
            z_frac=z_frac,
            load_x_frac=load_x_frac,
            load=c.il_unit_load_kn,
        )
        for load_x_frac in x_fracs
    ]
    xs = [c.bridge.x(x_frac=x_frac) for x_frac in x_fracs]

    units = resp_matrix.response_type.units()
    if units == "m":
        rs = np.array(rs) * 1000
        units = "mm"
    else:
        sci_format_y_axis()

    plt.plot(xs, rs)

    x, z = c.bridge.x(response_frac), c.bridge.z(resp_matrix.load_z_frac)
    name = resp_matrix.response_type.name()
    plt.title(
        f"{name.capitalize()} at x = {x:.2f}m, z = {z:.2f}m"
        + f"\n to {c.il_unit_load_kn}kN load moving along"
        + f" z = {c.bridge.z(resp_matrix.load_z_frac):.2f}m"
    )
    plt.xlabel(f"X position of {c.il_unit_load_kn}kN load")
    plt.ylabel(f"{name.capitalize()} ({units})")

    if save:
        plt.savefig(save)
        plt.close()
    return rs


def plot_dc(
    c: Config,
    resp_matrix: ResponsesMatrix,
    expt_index: int,
    response_frac: float,
    num_x: int,
    interp_sim: bool,
    interp_response: bool,
    save: str = None,
    show: bool = False,
):
    """Plot the IL for a response at some position.

    This function ignores the interp_sim as it just return the response due to
    the displacement load which was placed in the simulation, and is determined
    by the expt_index parameter. The ignored parameters exist just so the
    function definition is consistent with plot_il and can be passed to the
    same functions.

    """
    print_w(f"plt.matrices.plot_dc: expt_index = {expt_index}")
    fem_responses = resp_matrix.expt_responses[expt_index]
    xs = fem_responses.xs
    rs = [
        resp_matrix.expt_responses[expt_index].at(
            x_frac=c.bridge.x_frac(x), interpolate=interp_sim
        )
        for x in xs
    ]
    response_name = resp_matrix.response_type.name()
    response_units = resp_matrix.response_type.units()
    plt.title(f"{response_name.capitalize()} at simulation {expt_index}")
    plt.xlabel(f"x-axis (m)")
    plt.ylabel(f"{response_name.capitalize()} ({response_units})")
    sci_format_y_axis()
    plt.plot(xs, rs)
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    if save or show:
        plt.close()
    return rs


def matrix_subplots(
    c: Config,
    resp_matrix: ResponsesMatrix,
    num_subplots: int,
    num_x: int,
    z_frac: float,
    rows: int = 4,
    save: str = None,
    plot_func=None,
):
    """For each subplot plot matrix fem using the given function."""
    cols = int(num_subplots / rows)
    if cols != num_subplots / rows:
        print_w(
            f"Rows don't divide number of simulations, cols = {cols}"
            + f", sims = {num_subplots / rows}"
            + f", num_subplots = {num_subplots}, rows = {rows}"
        )
        cols += 1
    y_min, y_max = 0, 0
    # Plot each IL and bridge deck side.
    for i, response_frac in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        plot_bridge_deck_side(c.bridge, show=False, equal_axis=False)
        rs = plot_func(c, resp_matrix, i, response_frac, z_frac=z_frac, num_x=num_x)
        plt.axvline(x=c.bridge.x(x_frac=response_frac), color="red")
        # Keep track of min and max on y axis (only when non-zero fem).
        if any(rs):
            _y_min, _y_max = plt.gca().get_ylim()
            y_min, y_max = min(y_min, _y_min), max(y_max, _y_max)
    # Ensure y_min == -y_max.
    y_min = min(y_min, -y_max)
    y_max = max(-y_min, y_max)
    for i, _ in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        plt.ylim(y_min, y_max)
    plt.tight_layout()
    if save:
        plt.savefig(save)
        plt.close()


def imshow_il(
    c: Config, il_matrix: ILMatrix, num_loads: int, num_sensors: int, save: str
):
    """Plot a matrix of influence line for multiple response positions.

    Args:
        c: Config, global configuration object.
        il_matrix: ILExpt, fem for a number of unit load simulations.
        num_loads: int, number of loading positions/influence lines to plot.
        num_sensors: int, number of sensor positions in x direction to plot.

    """
    load_fracs = np.linspace(0, 1, num_loads)
    sensor_fracs = np.linspace(0, 1, num_sensors)

    matrix = []
    for load_frac in load_fracs:
        matrix.append([])
        for sensor_frac in sensor_fracs:
            value = il_matrix.response_to(
                x_frac=sensor_frac,
                z_frac=il_matrix.load_z_frac,
                load_x_frac=load_frac,
                load=c.il_unit_load_kn,
            )
            # print_d(D, f"value = {value}, il_frac = {il_frac}, load_x_frac = {load_x_frac}")
            matrix[-1].append(value)

    units = il_matrix.response_type.units()
    if il_matrix.response_type.units() == "m":
        matrix = np.array(matrix) * 1000
        units = "mm"
    print(np.amax(np.array(matrix)))
    print(np.amin(np.array(matrix)))

    plt.imshow(matrix, aspect="auto")
    clb = plt.colorbar()
    clb.ax.set_title(units)
    plt.title(
        f"Influence lines for {num_sensors} response positions along z ="
        + f" {c.bridge.z(il_matrix.load_z_frac):.2f}"
        + f" {il_matrix.response_type.units()}"
    )
    plt.xlabel("Response x position (m)")
    locs = [int(i) for i in np.linspace(0, num_sensors - 1, 5)]
    labels = [f"{c.bridge.x(sensor_fracs[i]):.2f}" for i in locs]
    plt.xticks(locs, labels)
    locs = [int(i) for i in np.linspace(0, num_loads - 1, 5)]
    labels = [f"{c.bridge.x(load_fracs[i]):.2f}" for i in locs]
    plt.yticks(locs, labels)
    plt.ylabel("Load x position (m)")
    if save:
        plt.savefig(save)
        plt.close()
