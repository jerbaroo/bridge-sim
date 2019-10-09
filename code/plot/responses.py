"""Plot responses on a bridge.

These function are characterized by taking FEMResponses as primary argument.

"""
from typing import List, Optional

import numpy as np

from config import Config
from fem.responses import FEMResponses
from model.load import Load
from plot import plt


def plot_contour_deck(
        c: Config, fem_responses: FEMResponses, y: float, loads: List[Load],
        save: Optional[str] = None, show: bool = False):
    """Contour plot of responses on the deck of the bridge.

    This function will iterate over x and z for a fixed y (given).

    """
    # Structure data.
    amax = np.inf
    amax_x, amax_z = None, None
    X, Z, H = [], [], []  # 2D arrays, x and z coordinates, and height.
    for x in fem_responses.xs:
        X.append([])
        Z.append([])
        H.append([])
        for z in fem_responses.zs[x][y]:
            X[-1].append(x)
            Z[-1].append(z)
            H[-1].append(fem_responses.responses[0][x][y][z].value)
            if H[-1][-1] < amax:
                amax = H[-1][-1]
                amax_x, amax_z = X[-1][-1], Z[-1][-1]
    # Plot contour and colorbar.
    cs = plt.contourf(X, Z, H, levels=50)
    plt.colorbar(cs)
    # Plot loads.
    for load in loads:
        x = load.x_frac * c.bridge.length
        z = (load.z_frac * c.bridge.width) - (c.bridge.width / 2)
        plt.plot([x], [z], marker="o", markersize=5, color="red")
    # Titles and labels.
    amin = np.amax(np.array(H))
    plt.title(
        f"{fem_responses.response_type.name()}"
        + f" ({fem_responses.response_type.units(False)})"
        + f", min = {(amax - amin):.10f} at ({amax_x}, {amax_z})")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.axis("equal")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()

