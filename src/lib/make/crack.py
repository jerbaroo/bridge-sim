from typing import Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import crack, temperature, plot
from bridge_sim.model import Config, ResponseType, Point
from bridge_sim.sim.model import Responses, Shell


def plot_crack_E(config: Config):
    """Verification plot of Young's modulus before and after cracking"""
    plt.portrait()
    plt.subplot(3, 1, 2)
    transverse_crack = crack.transverse_crack(length=2, at_x=config.bridge.x_center)
    crack_config = transverse_crack.crack(config)
    cmap, norm = plot.shells(
        crack_config, color_f=lambda shell: shell.section.youngs_x(), ret_cmap_norm=True
    )
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Cracked bridge")
    plt.subplot(3, 1, 1)
    plot.shells(
        config, color_f=lambda shell: shell.section.youngs_x(), cmap=cmap, norm=norm
    )
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Uncracked bridge")
    plt.subplot(3, 1, 3)

    def difference(shell: Shell) -> float:
        center = shell.center()
        uncracked_shell = config.bridge.deck_section_at(x=center.x, z=center.z)
        return uncracked_shell.youngs_x() - shell.section.youngs_x()

    cmap, norm = plot.shells(crack_config, color_f=difference, ret_cmap_norm=True)
    plot.top_view_bridge(config.bridge, piers=True)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plt.title("Difference of cracked and uncracked")
    plt.tight_layout()
    plt.savefig(config.get_image_path("verification/cracking", "crack.pdf"))
    plt.close()


def crack_plot(
    config: Config,
    crack_x_min: float,
    crack_length: float,
    response_type: ResponseType,
    run: bool = False,
    scatter: bool = False,
    temps: Tuple[float, float] = [17, 23],
):
    """Plot bridge responses to temperature with and without cracking.

    Args:
        config: simulation configuration object.
        crack_x_min: lower X position of crack zone.
        crack_length: length of crack zone in X direction.
        response_type: type of sensor response to plot.
        run: force the simulation data to be regenerated.
        scatter: scatter plot instead of contour plot.
        temps: temperature profile of the deck.

    """
    points = [
        Point(x=x, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, 200)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 60)
    ]
    responses = temperature.effect(
        config=config,
        response_type=response_type,
        points=points,
        temps_bt=([temps[0]], [temps[1]]),
    ).T[0]
    responses = Responses(
        response_type=response_type, responses=list(zip(responses, points)),
    )
    plot.contour_responses(config, responses)
    plot.top_view_bridge(config.bridge, piers=True)
    plt.show()
