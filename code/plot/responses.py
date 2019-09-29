"""Plot responses on a bridge.

These function are characterized by taking FEMResponses as primary argument.

"""
from typing import Optional

from config import Config
from fem.responses import FEMResponses
from plot import plt


def plot_contour_deck(
        c: Config, fem_responses: FEMResponses, y: float,
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
    cs = plt.contourf(X, Z, H)
    plt.colorbar(cs)
    plt.title(
        f"{fem_responses.response_type.name()}"
        + f" {fem_responses.response_type.units()}")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    if save:
        print(save)
        plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()
