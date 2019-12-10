from classify.scenario.bridge import center_lane_crack
from config import Config
from plot.geom import plot_cloud_of_nodes


def make_cloud_of_node_plots(c: Config):
    """Make all variations of the cloud of nodes plots."""

    def both_axis_plots(prop: str, c: Config, **kwargs):
        """Make cloud of nodes plots for full and equal axes."""
        # Cloud of nodes with equal axes.
        plot_cloud_of_nodes(
            c=c,
            equal_axis=True,
            save=c.get_image_path(f"cloud-of-nodes{prop}-equal-axis", "cloud"),
            **kwargs,
        )
        # Cloud of nodes without axis correction.
        # plot_cloud_of_nodes(
        #     c=c,
        #     equal_axis=False,
        #     save=c.get_image_path(f"cloud-of-nodes{prop}", "cloud"),
        #     **kwargs,
        # )

    def deck_pier_plots(prop: str, **kwargs):
        """Make both axis plots for all deck and pier variants."""
        both_axis_plots(prop, deck=True, piers=False, **kwargs)
        both_axis_plots(prop, deck=False, piers=True, **kwargs)
        both_axis_plots(prop, deck=True, piers=True, **kwargs)

    def all_plots(prop: str, **kwargs):
        """Plots of healthy and cracked bridge."""
        deck_pier_plots(prop, c=center_lane_crack().crack_config(c), **kwargs)
        deck_pier_plots(prop, c=c, **kwargs)

    # Plots of some node property.
    all_plots("-youngs", node_prop=lambda s: s.youngs)
    all_plots("-density", node_prop=lambda s: s.density)
    all_plots("-thickness", node_prop=lambda s: s.thickness)
