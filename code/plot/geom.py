"""Plot 3D geometry of a bridge."""
from typing import Callable, Optional

import numpy as np
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from config import Config
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.common import Node
from fem.run.opensees.build.d3 import build_model_3d, nodes_by_id
from model.load import PointLoad
from plot import plt
from util import print_d

# Print debug information for this file.
D: str = "plot.bridge"
# D: bool = False


def plot_cloud_of_nodes(
        c: Config, equal_axis: bool = False,
        node_prop: Optional[Callable[[Node], float]] = None,
        save: Optional[str] = None, show: bool = False):
    """Plot the 'Node's of a 3D FEM."""
    build_model_3d(c=c, expt_params=ExptParams([FEMParams(
        [PointLoad(0.1, 0.1, 100)], [])]), os_runner=OSRunner(c))
    nodes = list(nodes_by_id.values())
    print(len(nodes))

    # Split into separate arrays of x, y and z position, and colors.
    xs = np.array([n.x for n in nodes])
    ys = np.array([n.y for n in nodes])
    zs = np.array([n.z for n in nodes])
    cs = None if node_prop is None else np.array([node_prop(n) for n in nodes])

    # Axis to be referenced by function f in plot_and_save.
    ax = None

    # Determine values for scaling axes.
    max_range = np.array(
        [xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()]
    ).max() / 2.0
    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5

    def plot_and_save(f: Callable[[], None], append: str = ""):
        """Plot the cloud of points with optional additional operation.

        Args:
            f: Callable[[], None], additional operation called before plotting.
            append: str, string to append to the file name.

        """
        fig = plt.figure()
        nonlocal ax
        ax = fig.add_subplot(111, projection="3d", proj_type="ortho")
        f()
        p = ax.scatter(xs, zs, ys, c=cs, s=1)
        if equal_axis:
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        if cs is not None:
            fig.colorbar(p)
        if save: plt.savefig(f"{save}{append}")
        if show: plt.show()
        if save or show: plt.close()

    # Plot without angle change.
    plot_and_save(lambda: None, append="no-rotation")

    # Plot for different angles.
    for ii in range(0, 360, 90):
        plot_and_save(f=lambda: ax.view_init(elev=0, azim=ii), append=f"-{ii}")
