"""Plot responses from simulation."""
import numpy as np
from lib.plot import plt

from lib.plot.responses import plot_contour_deck as contour_responses
from lib.plot.geometry import top_view_bridge

__all__ = ["contour_responses", "top_view_bridge"]


def equal_lims(axis, rows, cols, subplots=None):
    """Set equal x or y limits on subplots."""
    amin, amax = np.inf, -np.inf
    lim_f = plt.ylim if axis == "y" else plt.xlim
    subplots = range(1, rows * cols + 1) if subplots is None else subplots
    for p in subplots:
        plt.subplot(rows, cols, p)
        if lim_f()[0] < amin:
            amin = lim_f()[0]
        if lim_f()[1] > amax:
            amax = lim_f()[1]
    for p in subplots:
        plt.subplot(rows, cols, p)
        lim_f((amin, amax))