import itertools

import numpy as np
from matplotlib.cm import get_cmap

from classify.scenario.bridge import CrackedBridge, center_lane_crack
from classify.scenarios import healthy_and_cracked_scenarios
from config import Config
from fem.build import get_bridge_shells
from fem.model import BuildContext, Shell
from fem.params import ExptParams, SimParams
from fem.run.build.elements import shells_by_id
from fem.run.opensees import OSRunner
from fem.run.opensees.build import build_model_3d
from model.bridge import Point
from plot import default_cmap, plt
from plot.geometry import plot_cloud_of_nodes
from plot.geometry.shell import shell_properties_3d
from util import flatten, safe_str


def make_shell_plots(c: Config):
    """Make plots of the shells, coloured by material property."""
    original_c = c
    # For each damage scenario build the model and extract the shells.
    for damage_scenario in healthy_and_cracked_scenarios:
        c, sim_params = damage_scenario.use(original_c, SimParams([]))
        for ctx, ctx_name in [
            (BuildContext(add_loads=[Point(x=85, y=0, z=0)]), "refined"),
            (None, "not-refined"),
        ]:
            bridge_shells = get_bridge_shells(bridge=c.bridge, ctx=ctx)
            deck_shells = flatten(bridge_shells[0], Shell)
            pier_shells = flatten(bridge_shells[1], Shell)
            all_shells = flatten(bridge_shells, Shell)

            # For each combination of parameters plot the shells.
            for shells_name, shells in [
                ("all", all_shells), ("deck", deck_shells), ("pier", pier_shells),
            ]:
                for outline, label in itertools.product([True, False], [True, False]):
                    for prop_name, prop_units, prop_f in [
                            ("Thickness", "m", lambda s: s.thickness),
                            ("Density", "kg/m", lambda s: s.density),
                            ("Poisson's ratio", "m/m", lambda s: s.poissons),
                            ("Young's modulus", "MPa", lambda s: s.youngs),
                    ]:
                        for cmap in [default_cmap, get_cmap("tab10")]:

                            shell_properties_3d(
                                shells=shells,
                                prop_units=prop_units,
                                prop_f=prop_f,
                                cmap=cmap,
                                outline=outline,
                                label=label,
                                colorbar=not label,
                            )
                            plt.title(f"{prop_name} of {c.bridge.name}")
                            plt.savefig(
                                c.get_image_path(
                                    f"geometry/{ctx_name}",
                                    safe_str(f"shells-{shells_name}-{prop_name}-outline-{outline}-{cmap.name}") + ".pdf",
                                )
                            )
                            plt.close()


def make_cloud_of_node_plots(c: Config):
    """Make all variations of the cloud of nodes plots."""

    def both_axis_plots(prop: str, c: Config, **kwargs):
        """Make cloud of nodes plots for full and equal axes."""
        # Cloud of nodes with equal axes.
        plot_cloud_of_nodes(
            title=prop,
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

    _c = c

    def all_plots(prop: str, **kwargs):
        """Plots of healthy and cracked bridge."""
        for damage_scenario in healthy_and_cracked_scenarios(_c):
            c = (
                damage_scenario.crack_config(_c)
                if isinstance(damage_scenario, CrackedBridge)
                else _c
            )
            deck_pier_plots(prop, c=c, **kwargs)

    all_plots("Bridge 705: Young's Modulus", units="MPa", node_prop=lambda s: s.youngs)
    # all_plots("Density", node_prop=lambda s: s.density)
    # all_plots("Thickness", node_prop=lambda s: s.thickness)
