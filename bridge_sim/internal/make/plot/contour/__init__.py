"""Make contour for validation of "unit" loads."""
from itertools import chain

from matplotlib.cm import get_cmap

from bridge_sim.internal.plot import parula_cmap, plt
from bridge_sim.internal.plot.contour import contour_responses_3d
from bridge_sim.model import Config, ResponseType
from bridge_sim.vehicles import truck1
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.responses import load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def cover_photo(c: Config, x: float, deformation_amp: float):
    """

    TODO: Not validation.
    TODO: SimParams takes any loads iterable, to be flattened.
    TODO: Wrap SimRunner into Config.
    TODO: Ignore response type in SimParams (fill in by load_sim_responses).

    """
    response_type = ResponseType.YTranslation
    sim_responses = load_fem_responses(
        c=c,
        sim_runner=OSRunner(c),
        response_type=response_type,
        sim_params=SimParams(
            response_types=[response_type],
            ploads=list(
                chain.from_iterable(
                    truck1.to_point_loads(
                        bridge=c.bridge, time=truck1.time_at(x=x, bridge=c.bridge),
                    )
                )
            ),
        ),
    )
    shells = contour_responses_3d(c=c, sim_responses=sim_responses)
    for cmap in [
        parula_cmap,
        get_cmap("jet"),
        get_cmap("coolwarm"),
        get_cmap("viridis"),
    ]:
        contour_responses_3d(
            c=c,
            sim_responses=sim_responses,
            deformation_amp=deformation_amp,
            shells=shells,
            cmap=cmap,
        )
        plt.axis("off")
        plt.grid(False)
        plt.savefig(
            c.get_image_path(
                "cover-photo",
                f"cover-photo-deform-{deformation_amp}" f"-cmap-{cmap.name}.pdf",
            )
        )
        plt.close()
