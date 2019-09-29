"""Convert parsed OpenSees responses to List[Response]."""
from collections import defaultdict
from typing import Dict, List

from config import Config
from fem.params import FEMParams, ExptParams
from fem.run import Parsed
from fem.run.opensees.common import Node, traverse_3d_nodes
from model import Response, Point
from model.response import ResponseType


def convert_sim_translation_responses(
        nodes: List[Node], sim_ind: int, response_type: ResponseType,
        parsed_sim_responses: Dict[ResponseType, List[List[float]]],
        converted_expt_responses: Dict[int, Dict[ResponseType, List[Response]]]
        ):
    """Convert parsed simulation translation responses to List[Response].

    The converted responses will be entered into the given dictionary.
    """
    # If the requested response type is not available do nothing.
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
            result.append(Response(
                value=parsed_sim_trans_responses[time][i], x=node.x, y=node.y,
                z=node.z, time=time, node_id=node.n_id))
            node_index += 1
    converted_expt_responses[sim_ind][response_type] = result


def convert_responses_3d(
        c: Config, expt_params: ExptParams, parsed_expt_responses: Parsed
        ) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed OpenSees responses to List[Response]."""
    # Nodes in order of which the nodal responses are read from disk.
    # A dictionary of simulation index to ResponseType to [Response].
    converted_expt_responses = defaultdict(dict)
    for sim_ind, parsed_sim_responses in parsed_expt_responses.items():
        nodes = traverse_3d_nodes(deck_nodes=expt_params.fem_params[sim_ind].deck_nodes)
        # Parse y translation responses if necessary.
        convert_sim_translation_responses(
            nodes=nodes, sim_ind=sim_ind,
            response_type=ResponseType.YTranslation,
            parsed_sim_responses=parsed_expt_responses[sim_ind],
            converted_expt_responses=converted_expt_responses)
    return converted_expt_responses