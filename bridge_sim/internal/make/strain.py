from copy import deepcopy

import matplotlib.pyplot as plt

from bridge_sim import plot, sim
from bridge_sim.model import Config, PointLoad, ResponseType, PierSettlement
from bridge_sim.sim.model import SimParams


def plot_strain(config: Config):
    plt.portrait()
    plt.subplot(3, 1, 1)
    point_loads = [PointLoad(x=51, z=0, load=100 * 1e3)]
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


def plot_linear_youngs(config: Config):
    response_type = ResponseType.StrainXXB
    point_loads = [PointLoad(x=80, z=+9.65, load=100 * 1e3)]
    pier_settlement = [PierSettlement(pier=4, settlement=1)]
    pier_settlement = []

    config_copy = deepcopy(config)
    config_copy.bridge.data_id = "modified-youngs"
    # Multiply young's modulus of piers.
    for support in config_copy.bridge.supports:
        existing_f = support._sections

        def new_f(*args):
            material = existing_f(*args)
            og_youngs = material.youngs
            material.youngs = og_youngs * 2
            material._youngs_x = material.youngs
            return material

        support._sections = new_f
    # Multiply young's modulus of bridge deck.
    for material in config_copy.bridge.sections:
        og_youngs = material.youngs
        material.youngs = og_youngs * 2
        material._youngs_x = material.youngs
    responses1 = sim.responses.load(
        config=config,
        response_type=response_type,
        point_loads=point_loads,
        pier_settlement=pier_settlement,
    ).map(lambda r: r * 1e3)
    responses2 = sim.responses.load(
        config=config_copy,
        response_type=response_type,
        point_loads=point_loads,
        pier_settlement=pier_settlement,
    ).map(lambda r: r * 1e3)
    plt.landscape()
    plt.subplot(1, 2, 1)
    plot.contour_responses(config, responses1)
    plot.top_view_bridge(config.bridge, piers=True)
    plt.legend()
    plt.subplot(1, 2, 2)
    plot.contour_responses(config_copy, responses2)
    plot.top_view_bridge(config_copy.bridge, piers=True)
    plt.legend()
    plt.savefig(config.get_image_path("verification/creep", "linear-youngs.pdf"))
