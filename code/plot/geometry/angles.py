from typing import Optional, List

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from plot import plt


def angles_3d(
    xs: List[float],
    ys: List[float],
    zs: List[float],
    angles: Optional[List[float]] = None,
    elev: Optional[float] = None,
):
    """Rotate a plot in 3D, yielding the axis and angle.

    Args:
        angles: Optional[List[float]], angles to plot at, if None use default
            angle.
        elev: Optional[float], elevation used if 'angles' is given.

    """
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)

    # Determine values for scaling axes.
    max_range = (
        np.array([xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()]).max()
        / 2.0
    )
    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5

    # Ensure at least one angle in default case.
    if angles is None:
        angles = [None]

    # Plot for different angles.
    for ii in angles:
        plt.landscape()
        fig = plt.figure()
        # ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
        ax = Axes3D(fig)
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        if ii is not None:
            ax.view_init(elev=elev, azim=ii)
        yield fig, ax, ii
