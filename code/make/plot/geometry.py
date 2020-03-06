import itertools

import numpy as np
from matplotlib.cm import get_cmap

from classify.scenarios import healthy_and_cracked_scenarios
from classify.without import without_pier_lines, without_wheel_tracks
from config import Config
from fem.build import get_bridge_nodes, get_bridge_shells
from fem.model import BuildContext, Node, Shell
from fem.params import SimParams
from model.bridge import Point
from plot import default_cmap, parula_cmap, plt
from plot.geometry import top_view_bridge
from plot.geometry.shell import shell_properties_3d, shell_properties_top_view
from plot.geometry.node import node_scatter_3d
from plot.responses import plot_deck_sensors
from util import flatten, safe_str


def make_shell_properties_3d(original_c: Config):
    """Make plots of the shells in 3D, coloured by material property."""
    # For each damage scenario build the model and extract the shells.
    for damage_scenario in healthy_and_cracked_scenarios:
        c, sim_params = damage_scenario.use(original_c, SimParams([]))
        for ctx, ctx_name in [
            (BuildContext(add_loads=[Point(x=85, y=0, z=0)]), "refined"),
            (None, "unrefined"),
        ]:
            bridge_shells = get_bridge_shells(bridge=c.bridge, ctx=ctx)
            deck_shells = flatten(bridge_shells[0], Shell)
            pier_shells = flatten(bridge_shells[1], Shell)
            all_shells = flatten(bridge_shells, Shell)
            # For each combination of parameters plot the shells.
            for shells_name, shells in [
                ("pier", pier_shells),
                ("all", all_shells),
                ("deck", deck_shells),
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
                                    f"geometry/shells-{ctx_name}-3d",
                                    safe_str(
                                        f"{shells_name}-{prop_name}-outline-{outline}-{cmap.name}"
                                    )
                                    + ".pdf",
                                )
                            )
                            plt.close()


def make_shell_properties_top_view(
    c: Config,
    shells_name_: str,
    prop_name_: str,
    refined_: bool,
    outline: bool,
    lanes: bool,
):
    """Make plots of the shells in top view, coloured by material property."""
    original_c = c
    # For each damage scenario build the model and extract the shells.
    for damage_scenario, damage_name in zip(
        healthy_and_cracked_scenarios, [None, "cracked"]
    ):
        c, sim_params = damage_scenario.use(original_c, SimParams([]))
        # TODO: Hack to fix bridge name in plot title, being corrupted somewhere.
        bridge_name = c.bridge.name
        for ctx, ctx_name, refined, in [
            (
                BuildContext(
                    add_loads=[Point(x=85, y=0, z=0)], refinement_radii=[2, 1, 0.5],
                ),
                "refined",
                True,
            ),
            (None, "unrefined", False),
        ]:
            if refined != refined_:
                continue
            bridge_shells = get_bridge_shells(bridge=c.bridge, ctx=ctx)
            deck_shells = flatten(bridge_shells[0], Shell)
            pier_shells = flatten(bridge_shells[1], Shell)
            all_shells = pier_shells + deck_shells
            for shells_name, shells in [
                ("piers", pier_shells),
                ("deck", deck_shells),
            ]:
                if shells_name != shells_name_:
                    continue
                for prop_name, prop_units, prop_f in [
                    ("Mesh", "", None),
                    ("Thickness", "m", lambda s: np.around(s.thickness, 3)),
                    ("Density", "kg/m", lambda s: np.around(s.density, 3)),
                    ("Poisson's ratio", "m/m", lambda s: s.poissons),
                    ("Young's modulus", "MPa", lambda s: np.around(s.youngs, 1)),
                ]:
                    if prop_name_ not in prop_name.lower():
                        continue
                    for cmap in [parula_cmap, default_cmap]:

                        def top_view():
                            top_view_bridge(
                                bridge=c.bridge,
                                abutments=True,
                                piers=True,
                                lanes=lanes,
                                compass=prop_f is not None,
                            )

                        top_view()
                        shell_properties_top_view(
                            shells=shells,
                            prop_f=prop_f,
                            prop_units=prop_units,
                            cmap=cmap,
                            colorbar=prop_f is not None,
                            # label=prop_f is not None,
                            outline=outline,
                        )
                        top_view()
                        damage_str = "" if damage_name is None else f" ({damage_name})"
                        plt.title(
                            f"{prop_name} of {bridge_name}'s {shells_name}{damage_str}"
                        )
                        plt.savefig(
                            c.get_image_path(
                                f"geometry/{shells_name}-shells-{ctx_name}-top-view",
                                safe_str(
                                    f"{prop_name}-{cmap.name}-outline-{outline}-lanes-{lanes}"
                                )
                                + ".pdf",
                            )
                        )
                        plt.close()
                        if prop_f is None:
                            break


def make_node_plots(original_c: Config):
    """Make all variations of 3d scatter plots of nodes."""
    for damage_scenario in healthy_and_cracked_scenarios:
        c, sim_params = damage_scenario.use(original_c, SimParams([]))
        for ctx, ctx_name in [
            (BuildContext(add_loads=[Point(x=85, y=0, z=0)]), "refined"),
            (None, "unrefined"),
        ]:
            bridge_nodes = get_bridge_nodes(bridge=c.bridge, ctx=ctx)
            deck_nodes = set(flatten(bridge_nodes[0], Node))
            pier_nodes = set(flatten(bridge_nodes[1], Node))
            all_nodes = set(flatten(bridge_nodes, Node))
            # For each combination of parameters plot the nodes.
            for nodes_name, nodes in [
                ("all", all_nodes),
                ("deck", deck_nodes),
                ("pier", pier_nodes),
            ]:
                node_scatter_3d(nodes=nodes)
                plt.title(f"Nodes of {c.bridge.name}")
                plt.savefig(
                    c.get_image_path(
                        f"geometry/nodes-{ctx_name}",
                        safe_str(f"{nodes_name}") + ".pdf",
                    )
                )
                plt.close()


def make_available_sensors_plot(c: Config, pier_radius: float, track_radius):
    """Scatter plot of sensors used for classification."""
    top_view_bridge(c.bridge, abutments=True, piers=True, compass=False)
    without_p = without_pier_lines(c=c, radius=pier_radius)
    without_t = without_wheel_tracks(c=c, radius=track_radius)

    def without(point: Point) -> bool:
        return without_t(point) or without_p(point)

    plot_deck_sensors(c=c, without=without, label=True)
    plt.title(f"Sensors available for classification on Bridge 705")
    plt.tight_layout()
    plt.savefig(c.get_image_path("sensors", "unavailable-sensors.pdf"))
    plt.close()
