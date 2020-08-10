"""Utilities when plotting."""

import numpy as np
from matplotlib import pyplot as plt, colors


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


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    """A truncated version of the given Matplotlib colormap."""
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


def legend_marker_size(legend, size):
    """Set the marker size for all legend markers."""
    for legend_handle in legend.legendHandles:
        legend_handle._sizes = [size]
