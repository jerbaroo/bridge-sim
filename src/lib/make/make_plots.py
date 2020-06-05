"""Make all plots for the thesis.

These function provide data to functions in '/plot'.

"""
from config import Config
from fem.run.opensees import OSRunner
from plot import (
    plot_bridge_deck_side,
    plot_bridge_first_section,
    plt,
)
from model.response import ResponseType
from bridge_sim.util import print_i, safe_str
from vehicles.sample import sample_vehicle
from vehicles.stats import vehicle_data_noise_stats, vehicle_density_stats


# Print debug information for this file.
D: str = "make.make_plots"
# D: bool = False


def make_stats(c: Config):
    """Make all textual information for the thesis."""
    print_i("\n\n" + vehicle_density_stats(c) + "\n")
    print_i("\n\n" + vehicle_data_noise_stats(c) + "\n")


def make_normal_mv_load_animations(c: Config, per_axle: bool = False):
    """Make animations of a pload moving across a bridge."""
    plt.close()
    mv_load = MovingLoad.from_vehicle(x_frac=0, vehicle=sample_vehicle(c), lane=0)
    per_axle_str = f"-peraxle" if per_axle else ""
    for response_type in ResponseType:
        animate_mv_load(
            c,
            mv_load,
            response_type,
            OSRunner(c),
            per_axle=per_axle,
            save=safe_str(
                c.image_path(
                    f"animations/{c.bridge.name}-{OSRunner(c).name}"
                    + f"-{response_type.name()}{per_axle_str}"
                    + f"-load-{mv_load.str_id()}"
                )
            ).lower()
            + ".mp4",
        )

