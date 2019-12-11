import numpy as np

from fem.params import SimParams
from fem.run.build.types import AllSupportNodes
from model.bridge import Bridge
from util import print_i


def print_mesh_info(
    bridge: Bridge, sim_params: SimParams, all_pier_nodes: AllSupportNodes
):
    """Print information about the mesh after each stage of building."""
    to_lens = lambda x: np.array(list(map(len, x)))
    base = to_lens(sim_params.deck_stages_info["base"])
    piers = to_lens(sim_params.deck_stages_info["piers"])
    loads = to_lens(sim_params.deck_stages_info["loads"])
    sections = to_lens(sim_params.deck_stages_info["sections"])
    refinement = to_lens(sim_params.deck_stages_info["refinement"])
    total = to_lens(sim_params.deck_stages_info["refinement"])

    refinement -= sections
    sections -= loads
    loads -= piers
    piers -= base
    print_i(
        "Deck nodes (x * z)"
        f"\n  base mesh  = {base[0]} * {base[1]}"
        f"\n  from piers = {piers[0]} * {piers[1]}"
        f"\n  from loads = {loads[0]} * {loads[1]}"
        f"\n  from materials = {sections[0]} * {sections[1]}"
        f"\n  from refinement = {refinement[0]} * {refinement[1]}"
        f"\n  total = {total[0]} * {total[1]}"
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
        + f"\n  base mesh  = {base[0]} * {base[1]}"
        + f"\n  from piers = {piers[0]} * {piers[1]} (mean)"
    )
