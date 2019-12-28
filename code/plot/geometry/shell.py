from typing import List

import matplotlib
import numpy as np
from scipy.interpolate import interp2d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from fem.run.build.elements import ShellElement
from plot import default_cmap, plt
from plot.geometry.angles import angles_3d


def shell_properties_3d(
        shells: List[ShellElement],
        prop_units: str,
        prop_f,
        cmap = default_cmap,
        outline: bool = True,
        new_fig: bool = True,
):
    """3D plot of shell elements coloured by material property."""
    # Coordinates for rotating the plot perspective.
    xs, ys, zs = [], [], []
    # Vertices of nodes for each shell.
    verts = []
    # Min and max values for colour normalization.
    prop_min, prop_max = np.inf, -np.inf
    for shell in shells:
        verts.append([])
        for node in shell.nodes():
            xs.append(node.x)
            ys.append(node.y)
            zs.append(node.z)
            verts[-1].append([node.x, node.z, node.y])
        shell_prop = prop_f(shell.section)
        if shell_prop < prop_min:
            prop_min = shell_prop
        if shell_prop > prop_max:
            prop_max = shell_prop
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)

    norm = matplotlib.colors.Normalize(vmin=prop_min, vmax=prop_max)

    # Setup a new 3D landscape figure.
    if new_fig:
        fig, ax, _ = next(angles_3d(xs, zs, ys))
    else:
        fig = plt.gcf()
        ax = plt.gca()

    for i, verts_ in enumerate(verts):
        ax.add_collection3d(
            Poly3DCollection(
                [verts_],
                facecolors=cmap(norm(prop_f(shells[i].section))),
                edgecolors="black" if outline else "none",
                linewidths=0.1 if outline else 0,
            )
        )

    # Let's add a colorbar.
    mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    clb = fig.colorbar(mappable, shrink=0.7)
    clb.ax.set_title(prop_units)
