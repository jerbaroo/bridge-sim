from typing import List, Optional

import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from config import Config
from fem.params import ExptParams, SimParams
from fem.responses import FEMResponses
from fem.run.build.elements import ShellElement, shells_by_id
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.response import ResponseType
from plot import default_cmap, plt
from plot.geometry.angles import angles_3d


def contour_responses_3d(
        c: Config,
        sim_responses: FEMResponses,
        shells: Optional[List[ShellElement]] = None,
        deformation_amp: float = 0,
        cmap: matplotlib.colors.Colormap = default_cmap,
        center_norm: bool = False,
        new_fig: bool = True
):
    """3D contour plot of simulation responses over deformed shell elements.

    Args:
        c: Config, global configuration object.
        sim_responses: FEMResponses, simulation responses to plot.
        shells: Optional[List[ShellElement]], shells of the FEM used to generate
            the responses. If not given they will be generated.
        deformation_amp: float, the amplitude of deformation, in meters.
        cmap: matplotlib.colors.Colormap, the colormap to plot with.
        center_norm: bool, whether to center the color normalization at 0.
        new_fig: bool, whether to plot on a new figure and axis.

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
    # Maximum response per shell, for colour normalization.
    max_r_per_shell = []
    # Vertices of nodes for each shell.
    verts = []
    for shell in shells:
        verts.append([])
        max_r_per_shell.append(-np.inf)
        for node in shell.nodes():
            x = node.x
            y_response = sim_responses._at(x=node.x, y=node.y, z=node.z)
            y_deformation = np.interp(y_response, [min_r, max_r], [0, 1]) * deformation_amp
            y = node.y + y_deformation
            z = node.z
            xs.append(node.x)
            ys.append(node.y)
            zs.append(node.z)
            verts[-1].append([x, z, y])
            if y_response > max_r_per_shell[-1]:
                max_r_per_shell[-1] = y_response

    # Colors are normalized based on the maximum response per shell.
    vmin, vmax = min(max_r_per_shell), max(max_r_per_shell)
    if center_norm:
        vmin, vmax = min(vmin, -vmax), max(vmax, -vmin)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

    # Setup a new 3D landscape figure.
    if new_fig:
        _fig, ax, _ = next(angles_3d(xs, zs, ys))
    else:
        ax = plt.gca()

    for i, verts_ in enumerate(verts):
        collection = Poly3DCollection(
            [verts_],
            alpha=1,
            linewidths=0.001,
        )
        facenorm = norm(max_r_per_shell[i])
        facecolor = cmap(facenorm)
        collection.set_edgecolor("none")
        collection.set_facecolor(cmap(facenorm))
        ax.add_collection3d(collection)

    return shells
