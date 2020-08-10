"""Plot fem on a bridge.

Functions characterized by receiving 'FEMResponses' and 'PointLoad'.

"""
from typing import Callable, List, Optional, Tuple

import numpy as np
from scipy.stats import chisquare

from bridge_sim.internal.plot import plt
from bridge_sim.model import ResponseType, Point, Config
from bridge_sim.sim.build import get_bridge_nodes, det_nodes
from bridge_sim.plot.util import legend_marker_size
from bridge_sim.util import print_w


def plot_deck_sensors(c: Config, without: Callable[[Point], bool], label: bool = False):
    """Scatter plot of deck sensors."""
    deck_nodes, _ = get_bridge_nodes(c.bridge)
    deck_nodes = det_nodes(deck_nodes)
    unavail_nodes = []
    avail_nodes = []
    for node in deck_nodes:
        if without(Point(x=node.x, y=node.y, z=node.z)):
            unavail_nodes.append(node)
        else:
            avail_nodes.append(node)
    X, Z, H = [], [], []  # 2D arrays, x and z coordinates, and height.
    for node in deck_nodes:
        X.append(node.x)
        Z.append(node.z)
        if without(Point(x=node.x, y=node.y, z=node.z)):
            H.append(1)
        else:
            H.append(0)
    plt.scatter(
        [node.x for node in avail_nodes],
        [node.z for node in avail_nodes],
        s=5,
        color="#1f77b4",
    )
    plt.scatter(
        [node.x for node in unavail_nodes],
        [node.z for node in unavail_nodes],
        color="#ff7f0e",
        s=5,
    )
    if label:
        plt.scatter(
            [avail_nodes[0].x],
            [avail_nodes[0].z],
            color="#1f77b4",
            label="Available",
            s=5,
        )
        plt.scatter(
            [unavail_nodes[0].x],
            [unavail_nodes[0].z],
            color="#ff7f0e",
            label="Unavailable",
            s=5,
        )
        legend = plt.legend()
        legend_marker_size(legend, 50)


def plot_distributions(
    response_array: List[float],
    response_type: ResponseType,
    titles: List[str],
    save: str,
    cols: int = 5,
    expected: List[List[float]] = None,
    xlim: Optional[Tuple[float, float]] = None,
):
    # Transpose so points are indexed first.
    response_array = response_array.T
    # response_array, unit_str = resize_and_units(response_array, response_type)
    num_points = response_array.shape[0]
    amax, amin = np.amax(response_array), np.amin(response_array)

    # Determine the number of rows.
    rows = int(num_points / cols)
    if rows != num_points / cols:
        print_w(f"Cols don't divide number of points {num_points}, cols = {cols}")
        rows += 1

    # Plot fem.
    for i in range(num_points):
        plt.subplot(rows, cols, i + 1)
        plt.xlim((amin, amax))
        plt.title(titles[i])
        label = None
        if expected is not None:
            if response_array.shape != expected.shape:
                expected = expected.T
                expected, _ = resize_and_units(expected, response_type)
            assert response_array.shape == expected.shape
            label = chisquare(response_array[i], expected[i])
        plt.hist(response_array[i], label=label)
        if label is not None:
            plt.legend()
        if xlim is not None:
            plt.xlim(xlim)

    plt.savefig(save)
    plt.close()
