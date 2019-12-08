"""Convert parsed OpenSees responses to List[Response]."""
from collections import defaultdict
from typing import Dict, List

from config import Config
from fem.params import SimParams, ExptParams
from fem.run import Parsed
from fem.run.build.types import Node, bridge_3d_nodes
from model import Response, Point
from model.response import ResponseType
from util import print_d

# Print debug information for this file.
D = "fem.run.opensees.convert.d3"
# D = False


def convert_sim_translation_responses(
    nodes: List[Node],
    sim_ind: int,
    response_type: ResponseType,
    parsed_sim_responses: Dict[ResponseType, List[List[float]]],
    converted_expt_responses: Dict[int, Dict[ResponseType, List[Response]]],
):
    """Convert parsed simulation translation responses to List[Response].

    The converted responses will be entered into the given dictionary.

    """
    # If the requested response type is not available do nothing.
    # TODO: Should we not raise an Error?
    if response_type not in parsed_sim_responses:
        return
    parsed_sim_trans_responses = parsed_sim_responses[response_type]
    result = []  # The List[Response] that we are converting to.
    node_index = 0  # Index of node corresponding to current response.
    # For each time step in the simulation.
    for time in range(len(parsed_sim_trans_responses)):
        # For each collected response at that time.
        for i in range(len(parsed_sim_trans_responses[time])):
            node = nodes[node_index]
            result.append(
                Response(
                    value=parsed_sim_trans_responses[time][i],
                    x=node.x,
                    y=node.y,
                    z=node.z,
                    time=time,
                    node_id=node.n_id,
                )
            )
            node_index += 1
    converted_expt_responses[sim_ind][response_type] = result


def convert_responses_3d(
    c: Config, expt_params: ExptParams, parsed_expt_responses: Parsed
) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed OpenSees responses to List[Response]."""
    # Nodes in order of which the nodal responses are read from disk. A
    # dictionary of simulation index to ResponseType to [Response].
    converted_expt_responses = defaultdict(dict)
    for sim_ind, parsed_sim_responses in parsed_expt_responses.items():
        fem_params = expt_params.sim_params[sim_ind]
        nodes = bridge_3d_nodes(
            deck_nodes=fem_params.deck_nodes,
            all_support_nodes=fem_params.all_support_nodes,
        )
        # Parse x, y, and z translation responses if necessary.
        for response_type in [
            ResponseType.XTranslation,
            ResponseType.YTranslation,
            ResponseType.ZTranslation,
        ]:
            convert_sim_translation_responses(
                nodes=nodes,
                sim_ind=sim_ind,
                response_type=response_type,
                parsed_sim_responses=parsed_expt_responses[sim_ind],
                converted_expt_responses=converted_expt_responses,
            )
    return converted_expt_responses
