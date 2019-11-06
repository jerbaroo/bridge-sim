"""Plot responses on a bridge.

Functions characterized by receiving 'FEMResponses' and 'PointLoad'.

"""
from typing import List, Optional

import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np

from config import Config
from fem.responses import Responses
from fem.run import FEMRunner
from model import Response
from model.load import PointLoad
from plot import plt


def plot_contour_deck(
        c: Config, responses: Responses, y: float, ploads: List[PointLoad] = [],
        norm = None, save: Optional[str] = None):
    """Contour plot of given responses. Iterate over x and z for a fixed y."""
    # Structure data.
    amax = np.inf
    amax_x, amax_z = None, None
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
                if H[-1][-1] < amax:
                    amax = H[-1][-1]
                    amax_x, amax_z = X[-1][-1], Z[-1][-1]
    amin = np.amax(np.array(H))
    if len(X) == 0:
        raise ValueError(f"No responses for contour plot")

    # Plot contour and colorbar.
    cmap = cm.get_cmap("bwr")
    if norm is None:
        vmin = min(amax, -amin)
        vmax = max(amin, -amax)
        print(amin, amax)
        print(vmin, vmax)
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
    cs = plt.contourf(X, Z, H, levels=50, cmap=cmap, norm=norm)

    if not save:
        return cmap

    plt.colorbar(cs, norm=norm)
    plt.axis("equal")

    # Plot point loads.
    for pload in ploads:
        x = pload.x_frac * c.bridge.length
        z = (pload.z_frac * c.bridge.width) - (c.bridge.width / 2)
        plt.plot([x], [z], marker="o", markersize=5, color="red")
    # Titles and labels.
    plt.title(
        f"{responses.response_type.name()}"
        + f" ({responses.response_type.units(False)})"
        + f", min = {(amax - amin):.10f} at ({amax_x}, {amax_z})")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    if save:
        plt.savefig(save)
        plt.close()
