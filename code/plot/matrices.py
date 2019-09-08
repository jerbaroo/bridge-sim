"""Plot responses from the response matrices."""
import numpy as np

from config import Config
from fem.responses.matrix.il import ResponsesMatrix
from fem.responses.matrix.il import ILMatrix
from plot import plt, plot_bridge_deck_side, sci_format_y_axis
from util import print_d, print_i, print_w

# Print debug information for this file.
D: bool = False


def plot_il(
        c: Config, resp_matrix: ILMatrix, expt_index: int,
        response_frac: float, num_x: int, interpolate_load: bool,
        interpolate_response: bool, save: str = None, show: bool = False):
    """Plot the IL for a response at some position."""
    x_fracs = np.linspace(0, 1, num_x)
    rs = [
        resp_matrix.response_to(
            x_frac=response_frac, load_x_frac=load_x_frac,
            load=c.il_unit_load_kn, interpolate_load=interpolate_load,
            interpolate_response=interpolate_response)
        for load_x_frac in x_fracs]
    xs = [c.bridge.x(x_frac=x_frac) for x_frac in x_fracs]
    response_ord = response_frac * c.bridge.length
    response_name = resp_matrix.response_type.name()
    response_units = resp_matrix.response_type.units()
    plt.title(f"{response_name.capitalize()} at {response_ord:.2f}m")
    plt.xlabel(f"{c.il_unit_load_kn}kN load position (m)")
    plt.ylabel(f"{response_name.capitalize()} at {response_ord:.2f}m"
               + f"({response_units})")
    sci_format_y_axis()
    plt.plot(xs, rs)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
    return rs


def plot_dc(
        c: Config, resp_matrix: ResponsesMatrix, expt_index: int,
        response_frac: float, num_x: int, interpolate_load: bool,
        interpolate_response: bool, save: str = None, show: bool = False):
    """Plot the IL for a response at some position.

    This function ignores the interpolate_load as it just return the response
    due to the displacement load which was placed in the simulation, and is
    determined by the expt_index parameter. The ignored parameters exist just
    so the function definition is consistent with plot_il and can be passed to
    the same functions.

    """
    print_w(f"plt.matrices.plot_dc: expt_index = {expt_index}")
    fem_responses = resp_matrix.expt_responses[expt_index]
    xs = fem_responses.xs
    rs = [
        resp_matrix.expt_responses[expt_index].at(
            x_frac=c.bridge.x_frac(x), interpolate=interpolate_load)
        for x in xs]
    response_name = resp_matrix.response_type.name()
    response_units = resp_matrix.response_type.units()
    plt.title(f"{response_name.capitalize()} at simulation {expt_index}")
    plt.xlabel(f"x-axis (m)")
    plt.ylabel(f"{response_name.capitalize()} ({response_units})")
    sci_format_y_axis()
    plt.plot(xs, rs)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
    return rs


def matrix_subplots(
        c: Config, resp_matrix: ResponsesMatrix, num_x: int, rows: int = 4,
        cols: int = None, save: str = None, show: bool = False, plot_func = None
        ):
    """For each subplot plot matrix responses using the given function."""
    print_w(f"num_expts = {resp_matrix.num_expts}")
    if cols is None:
        cols = int(resp_matrix.num_expts / rows)
        if cols != resp_matrix.num_expts / rows:
            print_w("Rows don't divide number of simulations")
            cols += 1
    y_min, y_max = 0, 0
    print_w(f"rows = {rows}")
    print_w(f"cols = {cols}")
    # Plot each IL and bridge deck side.
    for i, response_frac in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        rs = plot_func(c, resp_matrix, i, response_frac, num_x=num_x)
        plot_bridge_deck_side(c.bridge, show=False, equal_axis=False)
        plt.axvline(x=c.bridge.x(x_frac=response_frac), color="red")
        # Keep track of min and max on y axis (only when non-zero responses).
        if any(rs):
            _y_min, _y_max = plt.gca().get_ylim()
            y_min, y_max = min(y_min, _y_min), max(y_max, _y_max)
    # Ensure y_min == -y_max.
    y_min = min(y_min, -y_max)
    y_max = max(-y_min, y_max)
    for i, _ in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        plt.ylim(y_min, y_max)
    plt.gcf().set_size_inches(16, 10)
    plt.tight_layout()
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def imshow_il(
        c: Config, il_matrix: ILMatrix, num_ils: int, num_x: int,
        interpolate_load: bool, interpolate_response: bool, save: str = None,
        show: bool = False):
    """Plot a matrix of influence line for multiple response positions."""
    response_fracs = np.linspace(0, 1, num_ils)
    x_fracs = np.linspace(0, 1, num_x)
    matrix = []
    for response_frac in response_fracs:
        matrix.append([])
        for load_x_frac in x_fracs:
            print_d(D, f"response frac = {response_frac}, load_x_frac = {load_x_frac}")
            value = il_matrix.response_to(
                x_frac=response_frac, load_x_frac=load_x_frac,
                load=c.il_unit_load_kn, interpolate_load=interpolate_load,
                interpolate_response=interpolate_response)
            print_d(D, f"value = {value}, response_frac = {response_frac}, load_x_frac = {load_x_frac}")
            matrix[-1].append(value)
    # matrix = [
    #     [il_matrix.response_to(
    #         resp_x_frac=response_frac, load_x_frac=load_x_frac,
    #         load=c.il_unit_load_kn)
    #      for load_x_frac in x_fracs]
    #     for response_frac in response_fracs]
    print(np.amax(np.array(matrix)))
    print(np.amin(np.array(matrix)))
    plt.imshow(matrix, aspect="auto")
    plt.colorbar()
    plt.ylabel("load index")
    plt.xlabel("sensor index")
    plt.title(f"{il_matrix.fem_runner_name} influence lines")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
