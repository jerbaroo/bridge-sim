import matplotlib.pyplot as plt

from bridge_sim import plot, sim
from bridge_sim.model import Config, ResponseType, PointLoad
from bridge_sim.util import safe_str


def plot_self_weight(config: Config):
    response_type = ResponseType.StrainXXB
    responses = sim.responses.load(
        config=config,
        response_type=response_type,
        self_weight=True,
    ).map(lambda r: r * (1 if response_type.is_strain() else 1E3))
    if not response_type.is_strain():
        responses.units = "mm"
    plot.top_view_bridge(config.bridge, piers=True, units="m")
    plot.contour_responses(config, responses, scatter=True)
    plt.legend()

    rt_name = "Microstrain XXB" if response_type.is_strain() else response_type.name()
    plt.title(f"{rt_name} to self-weight")
    plt.tight_layout()
    plt.savefig(config.get_image_path(
        "verification/self_weight",
        safe_str(response_type.name()) + ".pdf"
    ))
    plt.close()
