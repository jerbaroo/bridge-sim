"""Build a mesh of Nodes and shells from a Bridge."""

from collections import defaultdict
from typing import List, Optional, Tuple

from bridge_sim.sim.build.deck import get_deck_nodes, get_deck_shells
from bridge_sim.sim.build.piers import get_pier_nodes, get_pier_shells
from bridge_sim.sim.model import (
    BridgeNodes,
    BridgeShells,
    BuildContext,
    DeckNodes,
    DeckShellNodes,
    Node,
    Shell,
)
from bridge_sim.model import Bridge
from bridge_sim.util import flatten


def get_bridge_nodes(bridge: Bridge, ctx: Optional[BuildContext] = None) -> BridgeNodes:
    if ctx is None:
        ctx = BuildContext([])
    return (
        get_deck_nodes(bridge=bridge, ctx=ctx),
        get_pier_nodes(bridge=bridge, ctx=ctx),
    )


def get_bridge_shells(
    bridge: Bridge, ctx: Optional[BuildContext] = None, ret_nodes: bool = False
) -> BridgeShells:
    if ctx is None:
        ctx = BuildContext([])
    bridge_nodes = get_bridge_nodes(bridge=bridge, ctx=ctx)
    bridge_shells = (
        get_deck_shells(bridge=bridge, deck_shell_nodes=bridge_nodes[0], ctx=ctx),
        get_pier_shells(bridge=bridge, pier_nodes=bridge_nodes[1], ctx=ctx),
    )
    if ret_nodes:
        return bridge_shells, bridge_nodes
    return bridge_shells


def get_bridge_shells_and_nodes(
    bridge: Bridge, ctx: Optional[BuildContext] = None
) -> Tuple[BridgeNodes, BridgeShells]:
    return get_bridge_shells(bridge=bridge, ctx=ctx, ret_nodes=True)


def to_deck_nodes(deck_shell_nodes: DeckShellNodes) -> DeckNodes:
    """Convert 'DeckShellNodes' to 'DeckNodes'."""
    # A dict of z position to x position to Node.
    deck_nodes_dict = defaultdict(dict)
    for node in set(flatten(deck_shell_nodes, Node)):
        deck_nodes_dict[node.z][node.x] = node
    # Iterate through sorted z and x positions.
    deck_nodes = []
    for z in sorted(deck_nodes_dict.keys()):
        deck_nodes.append([])
        for x in sorted(deck_nodes_dict[z].keys()):
            deck_nodes[-1].append(deck_nodes_dict[z][x])
    return deck_nodes


def det_nodes(iterable) -> List[Node]:
    """Nodes in a deterministic ordering."""
    nodes = set(flatten(iterable, Node))
    return sorted(nodes, key=lambda n: n.n_id)


def det_nodes_id_str(ctx: BuildContext) -> str:
    nodes = det_nodes(ctx.nodes_by_id.values())
    return " ".join(map(lambda n: str(n.n_id), nodes))


def det_shells(iterable) -> List[Shell]:
    """Shells in a deterministic ordering."""
    shells = set(flatten(iterable, Shell))
    return sorted(shells, key=lambda s: s.e_id)


def det_shells_id_str(ctx: BuildContext) -> str:
    shells = det_shells(ctx.shells_by_id.values())
    return " ".join(map(lambda s: str(s.e_id), shells))
