from config import Config
from plot.vehicles import (
    plot_db,
    plot_density,
    plot_length_vs_axles,
    plot_length_vs_weight,
    plot_weight_vs_axles,
)


def vehicle_plots(c: Config):
    """Plot vehicle information based on Config.vehicle_density."""
    plot_db(c=c, save=c.get_image_path("vehicles", f"db"))
    plot_density(c=c, save=c.get_image_path("vehicles", f"density"))
    plot_length_vs_axles(
        c=c, save=c.get_image_path("vehicles", f"length-vs-axles")
    )
    plot_length_vs_weight(
        c=c, save=c.get_image_path("vehicles", f"length-vs-weight")
    )
    plot_weight_vs_axles(
        c=c, save=c.get_image_path("vehicles", f"weight-vs-axles")
    )
