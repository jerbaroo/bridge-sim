"""Plot responses from the IL matrices."""
import matplotlib.pyplot as plt

from config import Config, bridge_705_config
from fem.responses.il import ILMatrix
from fem.run.opensees import os_runner
from model import *
from plot import *


def plot_il(c: Config, il_matrix: ILMatrix, response_frac: float, num_x: int,
            save: str=None, show: bool=False):
    """Plot the IL for a response at some position."""
    x_fracs = np.linspace(0, 1, num_x)
    rs = [il_matrix.response(response_frac, x_frac, c.il_unit_load_kn)
          for x_frac in x_fracs]
    xs = [c.bridge.x(x_frac) for x_frac in x_fracs]
    response_ord = response_frac * c.bridge.length
    response_name = response_type_name(il_matrix.response_type)
    response_units = response_type_units(il_matrix.response_type)
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


def plot_ils(c: Config, il_matrix: ILMatrix, rows: int=4, cols:int=3,
             num_x: int=100, save: str=None, show: bool=False):
    """Plot the influence line for a number of response positions."""
    response_name = response_type_name(il_matrix.response_type).capitalize()
    response_units = response_type_units(il_matrix.response_type)
    ymin, ymax = 0, 0
    # Plot each IL and bridge deck side.
    for i, response_frac in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        rs = plot_il(c, il_matrix, response_frac, num_x=num_x)
        plot_bridge_deck_side(c.bridge, show=False, equal_axis=False)
        # Keep track of min and max on y axis (only when non-zero responses).
        if any(rs):
            _ymin, _ymax = plt.gca().get_ylim()
            ymin, ymax = min(ymin, _ymin), max(ymax, _ymax)
    # Ensure ymin == -ymax.
    ymin = min(ymin, -ymax)
    ymax = max(-ymin, ymax)
    for i, _ in enumerate(np.linspace(0, 1, rows * cols)):
        plt.subplot(rows, cols, i + 1)
        plt.ylim(ymin, ymax)
    plt.gcf().set_size_inches(16, 10)
    plt.tight_layout()
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def imshow_il(c: Config, il_matrix: ILMatrix, num_ils: int=10, num_x: int=100,
              save: str=None, show: bool=False):
    """Plot a matrix of influence line for multiple response positions."""
    response_fracs = np.linspace(0, 1, num_ils)
    x_fracs = np.linspace(0, 1, num_x)
    matrix = [
        [il_matrix.response(response_frac, x_frac, c.il_unit_load_kn)
         for x_frac in x_fracs]
        for response_frac in response_fracs]
    plt.imshow(matrix, aspect="auto")
    plt.colorbar()
    plt.ylabel("load index")
    plt.xlabel("sensor index")
    name = response_type_name(il_matrix.response_type)
    plt.title(f"{il_matrix.fem_runner_name} influence lines")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
