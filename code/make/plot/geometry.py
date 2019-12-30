import itertools

from matplotlib.cm import get_cmap

from classify.scenarios import healthy_and_cracked_scenarios
from config import Config
from fem.build import get_bridge_nodes, get_bridge_shells
from fem.model import BuildContext, Node, Shell
from fem.params import SimParams
from model.bridge import Point
from plot import default_cmap, plt
from plot.geometry.shell import shell_properties_3d
from plot.geometry.node import node_scatter_3d
from util import flatten, safe_str


def make_shell_plots(c: Config):
    """Make plots of the shells, coloured by material property."""
    original_c = c
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
                                    f"geometry/shells-{ctx_name}",
                                    safe_str(f"{shells_name}-{prop_name}-outline-{outline}-{cmap.name}") + ".pdf",
                                )
                            )
                            plt.close()


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
                ("all", all_nodes), ("deck", deck_nodes), ("pier", pier_nodes),
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
