from fem.build import AllSupportNodes
from fem.params import SimParams
from model.bridge import Bridge


def print_mesh_info(
    bridge: Bridge, fem_params: SimParams, all_pier_nodes: AllSupportNodes
):
    """Print information about the mesh after each stage of building."""
    to_lens = lambda x: np.array(list(map(len, x)))
    base = to_lens(fem_params.deck_stages_info["base"])
    piers = to_lens(fem_params.deck_stages_info["piers"])
    loads = to_lens(fem_params.deck_stages_info["loads"])

    loads -= piers
    piers -= base
    print_i(
        "Deck nodes (x * z)"
        + f"\n\tbase mesh  = {base[0]} * {base[1]}"
        + f"\n\tfrom piers = {piers[0]} * {piers[1]}"
        + f"\n\tfrom loads = {loads[0]} * {loads[1]}"
    )

    num_pier_nodes_z, num_pier_nodes_y = [], []
    for pier_nodes in all_pier_nodes:
        for wall_nodes in pier_nodes:
            wall_shape = np.array(wall_nodes).shape
            num_pier_nodes_z.append(wall_shape[0])
            num_pier_nodes_y.append(wall_shape[1])
    base = [bridge.base_mesh_pier_nodes_y, bridge.base_mesh_pier_nodes_z]
    piers = np.array([np.mean(num_pier_nodes_y), np.mean(num_pier_nodes_z)])
    piers -= np.array(base)
    print_i(
        "Pier nodes (y * z)"
        + f"\n\tbase mesh  = {base[0]} * {base[1]}"
        + f"\n\tfrom piers = {piers[0]} * {piers[1]} (mean)"
    )
