import matplotlib as mpl
import matplotlib.pyplot as plt

from bridge_sim import plot
from bridge_sim.model import Config


def plot_asphalt(config: Config):
    plt.portrait()
    plt.subplot(2, 1, 1)
    config.self_weight_asphalt = True
    cmap, norm = plot.shells(
        config,
        color_f=lambda shell: shell.mass(config) / shell.area(),
        ret_cmap_norm=True,
    )
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plot.top_view_bridge(config.bridge, lanes=True)
    plt.title("Mass / area without asphalt")
    plt.subplot(2, 1, 2)
    config.self_weight_asphalt = False
    plot.shells(
        config, color_f=lambda shell: shell.mass(config) / shell.area(), norm=norm
    )
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), cmap=cmap, norm=norm
    )
    plot.top_view_bridge(config.bridge, lanes=True)
    plt.title("Mass / area with asphalt")
    plt.savefig(config.get_image_path("verification/asphalt", "asphalt.pdf"))
    plt.close()
