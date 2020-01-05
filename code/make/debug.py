from copy import deepcopy

from config import Config
from fem.build import BuildContext
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.load import PointLoad
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import safe_str


def mesh_refinement(c: Config, build: bool, plot: bool):
    """Generate TCL files for debugging mesh refinement."""
    response_type = ResponseType.YTranslation
    min_config = deepcopy(c)
    min_config.bridge.type = "debugging"
    # min_config.bridge.base_mesh_deck_max_x = 100
    # min_config.bridge.base_mesh_deck_max_z = 100
    # min_config.bridge.base_mesh_pier_max_long = 10
    pload = PointLoad(x_frac=0.5, z_frac=0.5, kn=100)

    def build_with_refinement(refinement_radii):
        sim_params = SimParams(
            response_types=[response_type],
            ploads=[pload],
            refinement_radii=refinement_radii,
        )
        # Build and save the model file.
        if build:
            build_model_3d(
                c=min_config,
                expt_params=ExptParams([sim_params]),
                os_runner=OSRunner(min_config),
            )
        # Load and plot responses.
        if plot:
            sim_responses = load_fem_responses(
                c=min_config,
                sim_runner=OSRunner(min_config),
                response_type=response_type,
                sim_params=sim_params,
                run=True,
            )
            for scatter in [True, False]:
                top_view_bridge(min_config.bridge, abutments=True, piers=True, lanes=True)
                plot_contour_deck(
                    c=min_config,
                    responses=sim_responses,
                    scatter=scatter,
                    levels=100,
                )
                plt.title(f"{refinement_radii}")
                plt.savefig(min_config.get_image_path(
                    "debugging",
                    safe_str(f"{response_type.name()}-{refinement_radii}-scatter-{scatter}") + ".pdf"
                ))
                plt.close()

    build_with_refinement([0])
    build_with_refinement([])
