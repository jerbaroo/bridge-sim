"""Plot responses on a bridge.

These function are characterized by taking FEMResponses as primary argument.

"""
from typing import List, Optional

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
    X, Z, H = [], [], []  # 2D arrays, of x and y coordinates, and height.
    for x in fem_responses.xs:
        X.append([])
        Z.append([])
        H.append([])
        for z in fem_responses.zs[x][y]:
            X[-1].append(x)
            Z[-1].append(z)
            H[-1].append(fem_responses.responses[0][x][y][z].value)
    cs = plt.contourf(X, Z, H, levels=40)
    plt.colorbar(cs)
    for load in loads:
        x = load.x_frac * c.bridge.length
        z = (load.z_frac * c.bridge.width) - (c.bridge.width / 2)
        plt.plot([x], [z], marker="o", markersize=5, color="red")
    plt.title(
        f"{fem_responses.response_type.name()}"
        + f" {fem_responses.response_type.units()}")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.axis("equal")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()

