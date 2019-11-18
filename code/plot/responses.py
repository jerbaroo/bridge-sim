"""Plot responses on a bridge.

Functions characterized by receiving 'FEMResponses' and 'PointLoad'.

"""
from typing import List, Optional, Tuple

import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np

from config import Config
from fem.responses import Responses
from fem.run import FEMRunner
from model import Response
from model.load import PointLoad
from model.response import ResponseArray, ResponseType, resize_units
from plot import plt
from util import print_w


def plot_distributions(
        response_array: ResponseArray, response_type: ResponseType,
        titles: List[str], save: str, cols: int = 5,
        xlim: Optional[Tuple[float, float]] = None):
    # Transpose so points are indexed first.
    response_array = response_array.T
    response_array, unit_str = resize_units(response_array, response_type)
    num_points = response_array.shape[0]
    amax, amin = np.amax(response_array), np.amin(response_array)

    # Determine the number of rows.
    rows = int(num_points / cols)
    if rows != num_points / cols:
        print_w(
            f"Cols don't divide number of points {num_points}, cols = {cols}")
        rows += 1

    # Plot responses.
    for i in range(num_points):
        plt.subplot(rows, cols, i + 1)
        plt.xlim((amin, amax))
        plt.title(titles[i])
        plt.hist(response_array[i])
        if xlim is not None:
            plt.xlim(xlim)

    plt.savefig(save)
    plt.close()


def plot_contour_deck(
    c: Config,
    responses: Responses,
    y: float=0,
    ploads: List[PointLoad] = [],
    norm=None,
    save: Optional[str] = None,
):
    """Contour plot of given responses. Iterate over x and z for a fixed y."""
    # Structure data.
    amax, amax_x, amax_z = -np.inf, None, None
    amin, amin_x, amin_z = np.inf, None, None
    X, Z, H = [], [], []  # 2D arrays, x and z coordinates, and height.
    for x in responses.xs:
        # There is a chance that no sensors exist at given y position for every
        # x position, thus we must check.
        if y in responses.zs[x]:
            X.append([])
            Z.append([])
            H.append([])
            for z in responses.zs[x][y]:
                X[-1].append(x)
                Z[-1].append(z)
                H[-1].append(responses.responses[0][x][y][z])
                if isinstance(H[-1][-1], Response):
                    H[-1][-1] = H[-1][-1].value
                if H[-1][-1] > amax:
                    amax = H[-1][-1]
                    amax_x, amax_z = X[-1][-1], Z[-1][-1]
                if H[-1][-1] < amin:
                    amin = H[-1][-1]
                    amin_x, amin_z = X[-1][-1], Z[-1][-1]
    if len(X) == 0:
        raise ValueError(f"No responses for contour plot")

    # Plot contour and colorbar.
    cmap = cm.get_cmap("bwr")
    if norm is None:
        vmin = min(amin, -amax)
        vmax = max(amax, -amin)
        print(amin, amax)
        print(vmin, vmax)
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
    cs = plt.contourf(X, Z, H, levels=50, cmap=cmap, norm=norm)

    if save is None:
        return cs, cmap, norm

    clb = plt.colorbar(cs, norm=norm)
    clb.ax.set_title(responses.response_type.units())
    plt.axis("equal")

    # Plot point loads.
    for pload in ploads:
        x = pload.x_frac * c.bridge.length
        z = (pload.z_frac * c.bridge.width) - (c.bridge.width / 2)
        plt.plot([x], [z], marker="o", markersize=5, color="red")
    # Titles and labels.
    plt.title(
        f"{responses.response_type.name()}"
        + f", min = {amin:.4f} at ({amin_x:.3f}, {amin_z:.3f})"
        + f", max = {amax:.4f} at ({amax_x:.3f}, {amax_z:.3f})"
    )
    plt.xlabel("x position (m)")
    plt.ylabel("z position (m)")
    if save:
        plt.savefig(save)
        plt.close()
