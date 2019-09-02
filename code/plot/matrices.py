"""Plot responses from the response matrices."""
import numpy as np

from config import Config
from fem.responses.matrix.il import ResponsesMatrix
from fem.responses.matrix.il import ILMatrix
from plot import plt, plot_bridge_deck_side, sci_format_y_axis
from util import print_i, print_w


def plot_il(
        c: Config, il_matrix: ILMatrix, _i: int, response_frac: float,
        num_x: int, save: str = None, show: bool = False):
    """Plot the IL for a response at some position."""
    x_fracs = np.linspace(0, 1, num_x)
    rs = [il_matrix.response_to(response_frac, load_x_frac, c.il_unit_load_kn)
          for load_x_frac in x_fracs]
    xs = [c.bridge.x(x_frac) for x_frac in x_fracs]
    response_ord = response_frac * c.bridge.length
    response_name = il_matrix.response_type.name()
    response_units = il_matrix.response_type.units()
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
        c: Config, resp_matrix: ResponsesMatrix, i: int, _response_frac: float,
        num_x: int, save: str = None, show: bool = False):
    """Plot the IL for a response at some position."""
    fem_responses = resp_matrix.expt_responses[i]
    xs = fem_responses.xs
    rs = [resp_matrix.expt_responses[i].at(x_frac=c.bridge.x_frac(x))
          for x in xs]
    response_name = resp_matrix.response_type.name()
    response_units = resp_matrix.response_type.units()
    plt.title(f"{response_name.capitalize()} at simulation {i}")
    plt.xlabel(f"x-axis (m)")
    plt.ylabel(f"{response_name.capitalize()} ({response_units})")
    sci_format_y_axis()
    plt.plot(xs, rs)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
    return rs


def matrix_subplots(
        c: Config, resp_matrix: ResponsesMatrix, rows: int = 4, cols: int = None,
        num_x: int = 100, save: str = None, show: bool = False, plot_func=None):
    """For each subplot plot matrix responses using the given function."""
    if cols is None:
        cols = int(resp_matrix.num_expts / rows)
        if cols != resp_matrix.num_expts / rows:
            print_w("Rows don't divide number of simulations")
            cols += 1
    y_min, y_max = 0, 0
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
        c: Config, il_matrix: ILMatrix, num_ils: int = 10, num_x: int = 100,
        save: str = None, show: bool = False):
    """Plot a matrix of influence line for multiple response positions."""
    response_fracs = np.linspace(0, 1, num_ils)
    x_fracs = np.linspace(0, 1, num_x)
    matrix = []
    for response_frac in response_fracs:
        matrix.append([])
        for load_x_frac in x_fracs:
            print_w(f"response frac = {response_frac}, load_x_frac = {load_x_frac}")
            value = il_matrix.response_to(
                x_frac=response_frac, load_x_frac=load_x_frac,
                load=c.il_unit_load_kn)
            print_i(f"value = {value}, response_frac = {response_frac}, load_x_frac = {load_x_frac}")
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
