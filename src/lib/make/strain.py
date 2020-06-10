import matplotlib.pyplot as plt

from bridge_sim import plot, sim
from bridge_sim.model import PointLoad, ResponseType
from bridge_sim.sim.model import SimParams


def plot_strain(config):
    plt.portrait()
    plt.subplot(3, 1, 1)
    point_loads = [PointLoad(x=51, z=0, load=100)]
    responses = sim.responses.load(
        config=config, response_type=ResponseType.StrainXXB, point_loads=point_loads,
    )
    plot.contour_responses(config, responses)
    plt.title("Tricontourf")
    plt.subplot(3, 1, 2)
    plot.contour_responses(config, responses, interp=(200, 60))
    plt.title("Tricontourf: interpolated onto grid")
    plt.subplot(3, 1, 3)
    plot.contour_responses(config, responses, scatter=True)
    plot.shells(config, SimParams(ploads=point_loads))
    plt.title("Scatter plot with shells")
    plt.savefig(config.get_image_path("verification/jaggedness", "strain.pdf"))
