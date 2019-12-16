import matplotlib
import numpy as np
from scipy.interpolate import interp2d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from plot import plt
from plot.geometry.angles import angles_3d


def shell_plots_3d(shells, prop_units, prop_f, outline, cb):
    """Plot the given shells from multiple angles."""

    # Coordinates for the purpose of rotating the plot perspective.
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
        shell_prop = prop_f(shell)
        if shell_prop < prop_min:
            prop_min = shell_prop
        if shell_prop > prop_max:
            prop_max = shell_prop
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)

    norm = matplotlib.colors.Normalize(vmin=prop_min, vmax=prop_max)
    cmap = matplotlib.cm.get_cmap("coolwarm")

    def plot_shells(fig, ax, append):
        """Plot the cloud of points with optional additional operation."""

        for i, verts_ in enumerate(verts):
            ax.add_collection3d(
                Poly3DCollection(
                    [verts_],
                    facecolors=cmap(norm(prop_f(shells[i]))),
                    edgecolors="black" if outline else "none",
                    linewidths=0.1 if outline else 0,
                )
            )
        mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        clb = fig.colorbar(mappable, shrink=0.7)
        clb.ax.set_title(prop_units)
        cb(angle)

    for fig, ax, angle in angles_3d(xs=xs, ys=zs, zs=ys):
        plot_shells(fig, ax, angle)
    # for fig, ax, angle in angles_3d(
    #         angles=range(0, 360, 90), elev=0, xs=xs, ys=ys, zs=zs):
    #     plot_shells(fig, ax, angle)
