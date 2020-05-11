from itertools import chain

from lib.config import Config
from lib.fem.run.build.types import AllSupportNodes, DeckNodes


def assert_all_pier_nodes(c: Config, all_pier_nodes: AllSupportNodes):
    """Sanity check that all pier nodes have the correct structure."""
    assert len(all_pier_nodes) == len(c.bridge.supports)
    for s_nodes in all_pier_nodes:
        assert len(s_nodes) == 2
        assert isinstance(s_nodes, tuple)
        for w_nodes in s_nodes:
            assert isinstance(w_nodes, list)
            assert isinstance(w_nodes[0], list)


def assert_deck_in_pier_pier_in_deck(
    deck_nodes: DeckNodes, all_pier_nodes: AllSupportNodes
):
    """The number of top nodes per pier must equal that range in the mesh."""
    # First create a list of deck nodes sorted by x then z position.
    sorted_deck_nodes = sorted(
        chain.from_iterable(deck_nodes), key=lambda n: (n.x, n.z)
    )
    for pier_nodes in all_pier_nodes:
        for wall_nodes in pier_nodes:
            # Get the top line of nodes of the wall and assert we got them
            # correctly.
            wall_top_nodes = list(map(lambda ys: ys[0], wall_nodes))
            for z, node in enumerate(wall_top_nodes):
                assert node.y > wall_nodes[z][1].y
            x = wall_top_nodes[0].x
            for x_index in range(1, len(wall_top_nodes)):
                assert x == wall_top_nodes[x_index].x
            # Find the deck nodes with the correct x position and range of z.
            min_z = wall_top_nodes[0].z
            max_z = wall_top_nodes[-1].z
            deck_in_range = len(
                list(
                    n
                    for n in sorted_deck_nodes
                    if n.x == x and n.z >= min_z and n.z <= max_z
                )
            )
            assert deck_in_range == len(wall_top_nodes)
