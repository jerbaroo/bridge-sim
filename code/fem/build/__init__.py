from typing import Optional

from fem.build.deck import get_deck_nodes, get_deck_shells
from fem.build.piers import get_pier_nodes, get_pier_shells
from fem.model import BridgeNodes, BridgeShells, BuildContext
from model.bridge import Bridge


def get_bridge_nodes(bridge: Bridge, ctx: Optional[BuildContext] = None) -> BridgeNodes:
    if ctx is None:
        ctx = BuildContext([])
    return get_deck_nodes(bridge=bridge, ctx=ctx), get_pier_nodes(bridge=bridge, ctx=ctx)


def get_bridge_shells(bridge: Bridge, ctx: Optional[BuildContext] = None) -> BridgeShells:
    if ctx is None:
        ctx = BuildContext([])
    bridge_nodes = get_bridge_nodes(bridge=bridge, ctx=ctx)
    return (
        get_deck_shells(bridge=bridge, deck_nodes=bridge_nodes[0], ctx=ctx),
        get_pier_shells(bridge=bridge, pier_nodes=bridge_nodes[1], ctx=ctx),
    )
