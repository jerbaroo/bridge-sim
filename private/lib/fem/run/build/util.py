from copy import deepcopy
import numpy as np

from lib.fem.params import SimParams
from lib.fem.run.build.types import AllSupportNodes
from lib.model.bridge import Bridge
from util import print_i


def print_mesh_info(
    bridge: Bridge, sim_params: SimParams, all_pier_nodes: AllSupportNodes
):
    """Print information about the mesh after each stage of building."""

    ################
    ##### Deck #####
    ################

    to_lens = lambda x: np.array(list(map(len, x)))

    mesh_name_lens = []
    for name, positions in list(sim_params.deck_stages_info.items()):
        mesh_name_lens.append((name, to_lens(positions)))

    print_i("Deck nodes (x * z)")
    for i, (name, lens) in enumerate(mesh_name_lens):
        lens_from = deepcopy(lens)
        if i != 0:
            lens_from -= mesh_name_lens[i - 1][1]
        print_i(f"  from {name} = {lens_from[0]} * {lens_from[1]}")
        if i == len(mesh_name_lens) - 1:
            print_i(f"  total = {lens[0]} * {lens[1]}")

    #################
    ##### Piers #####
    #################

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
        + f"\n  from deck = {piers[0]} * {piers[1]} (mean)"
    )
