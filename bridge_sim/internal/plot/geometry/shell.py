from typing import Callable, List, Optional

import matplotlib
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from bridge_sim.internal.plot import default_cmap, plt
from bridge_sim.internal.plot.geometry.angles import ax_3d
from bridge_sim.model import Material
from bridge_sim.sim.model import Shell


def shell_properties_3d(
    shells: List[Shell],
    prop_f: Callable[[Material], float],
    prop_units: str,
    cmap: matplotlib.colors.Colormap = default_cmap,
    colorbar: bool = False,
    label: bool = False,
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
        fig, ax = ax_3d(xs=xs, ys=zs, zs=ys)
    else:
        fig = plt.gcf()
        ax = plt.gca()

    # Keep track of all values used for colours.
    # This is so we don't add duplicate labels.
    values = set()

    for i, verts_ in enumerate(verts):
        value = prop_f(shells[i].section)
        colour = cmap(norm(value))
        label_str = None
        if label and value not in values:
            values.add(value)
            label_str = f"{value}{prop_units}"
        poly = Poly3DCollection(
            [verts_],
            facecolors=colour,
            edgecolors="black" if outline else "none",
            linewidths=0.01 if outline else 0,
            label=label_str,
        )
        poly._facecolors2d = poly._facecolors3d
        poly._edgecolors2d = poly._edgecolors3d
        ax.add_collection3d(poly)

    if label:
        plt.legend()

    # Add a colorbar if requested.
    if colorbar:
        mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        clb = fig.colorbar(mappable, shrink=0.7)
        clb.ax.set_title(prop_units)


def shell_properties_top_view(
    shells: List[Shell],
    prop_f: Optional[Callable[[Material], float]] = None,
    prop_units: Optional[str] = None,
    cmap: matplotlib.colors.Colormap = default_cmap,
    colorbar: bool = False,
    label: bool = False,
    outline: bool = True,
):
    """Top view of shell elements optionally coloured by material property."""
    # Vertices of nodes for each shell.
    verts = []
    # Min and max values for colour normalization.
    prop_min, prop_max = np.inf, -np.inf
    for shell in shells:
        verts.append([])
        for node in shell.nodes():
            verts[-1].append([node.x, node.z])
        shell_prop = prop_f(shell.section) if prop_f is not None else 0
        if shell_prop < prop_min:
            prop_min = shell_prop
        if shell_prop > prop_max:
            prop_max = shell_prop
    if prop_f is not None:
        norm = matplotlib.colors.Normalize(vmin=prop_min, vmax=prop_max)

    # Keep track of all values used for colours.
    # This is so we don't add duplicate labels.
    values = set()

    ax = plt.gca()
    for shell, shell_verts in zip(shells, verts):
        colour, label_str = "none", None
        if prop_f is not None:
            value = prop_f(shell.section)
            colour = cmap(norm(value))
            if label and value not in values:
                values.add(value)
                label_str = f"{value} {prop_units}"
        ax.add_collection(
            matplotlib.collections.PolyCollection(
                [shell_verts],
                facecolors=colour,
                edgecolors="black" if outline else "none",
                linewidths=0.01 if outline else 0,
                label=label_str,
            )
        )

    if prop_f is not None:
        if label:
            plt.legend()
        if colorbar:
            mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
            clb = plt.gcf().colorbar(mappable, shrink=0.7)
            clb.ax.set_title(prop_units)
