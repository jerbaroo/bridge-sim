from typing import List, Optional

import matplotlib
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from config import Config
from fem.params import ExptParams, SimParams
from fem.responses import FEMResponses
from fem.run.build.elements import ShellElement, shells_by_id
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.response import ResponseType
from plot import plt
from plot.geometry.angles import angles_3d


def contour_plot_3d(
        c: Config, sim_responses: FEMResponses, max_translate: float = 3,
        shells: Optional[List[ShellElement]] = None
):
    """3D contour plot of given responses.

    Args:
        c: Config, global configuration object.
        sim_responses: FEMResponses, simulation responses to plot.
        max_translate: float, the maximum amount of translation, in meters.
        shells: Optional[List[ShellElement]], shells of the FEM used to generate
            the responses. If not given they will be generated.

    """
    # For now we only support displacement.
    assert sim_responses.response_type == ResponseType.YTranslation

    # Calculate the shells if necessary.
    # TODO: Add default expt_params to build_model_3d.
    if shells is None:
        build_model_3d(
            c=c, expt_params=ExptParams([SimParams([], [])]),
            os_runner=OSRunner(c)
        )
        shells = shells_by_id.values()
        deck_shells = [s for s in shells if not s.pier]
        pier_shells = [s for s in shells if s.pier]
        shells = pier_shells + deck_shells

    max_r, min_r = max(sim_responses.values()), min(sim_responses.values())
    # Coordinates for rotating the plot perspective.
    xs, ys, zs = [], [], []
    # Maximum response per shell, for colour calculation.
    max_r_per_shell = []
    # Vertices of nodes for each shell.
    verts = []
    for shell in shells:
        verts.append([])
        max_r_per_shell.append(-np.inf)
        for node in shell.nodes():
            x = node.x
            y_response = sim_responses._at(x=node.x, y=node.y, z=node.z)
            y_translate = np.interp(y_response, [min_r, max_r], [0, 1]) * max_translate
            y = node.y + y_translate
            z = node.z
            xs.append(node.x)
            ys.append(node.y)
            zs.append(node.z)
            verts[-1].append([x, z, y])
            if y_response > max_r_per_shell[-1]:
                max_r_per_shell[-1] = y_response
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)

    norm = matplotlib.colors.Normalize(vmin=min(max_r_per_shell), vmax=max(max_r_per_shell))
    cmap = matplotlib.cm.get_cmap("coolwarm")

    def plot_shells(fig, ax, append):
        """Plot the cloud of points with optional additional operation."""
        for i, verts_ in enumerate(verts):
            ax.add_collection3d(
                Poly3DCollection(
                    [verts_],
                    facecolors=cmap(norm(max_r_per_shell[i])),
                )
            )
        plt.savefig(c.get_image_path("cover-photo", "cover-photo.pdf"))
        plt.close()

    for fig, ax, angle in angles_3d(xs=xs, ys=zs, zs=ys):
        plot_shells(fig, ax, angle)
