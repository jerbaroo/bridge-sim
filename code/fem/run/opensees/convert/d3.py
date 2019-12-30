"""Convert parsed OpenSees responses to List[Response]."""
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List

import numpy as np

from config import Config
from fem.build import det_nodes, det_shells
from fem.model import Node, Shell
from fem.params import SimParams, ExptParams
from fem.run import Parsed
from model import Response, Point
from model.response import ResponseType
from util import print_d, print_w

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


def convert_strain_responses(
    elements: List[Shell],
    sim_ind: int,
    parsed_sim_responses: Dict[ResponseType, List[List[float]]],
    converted_expt_responses: Dict[int, Dict[ResponseType, List[Response]]],
):
    if ResponseType.Strain not in parsed_sim_responses:
        return
    parsed_sim_strain = parsed_sim_responses[ResponseType.Strain]
    result = []
    print_w("Elements belonging to piers will not have strain recorded")
    print_w("Strain responses are specified to be at y=0, but recorded lower")

    # For each integration point..
    assert len(parsed_sim_strain) == 4
    for i_point in range(4):

        # ..consider the responses for each element.
        assert len(elements) == len(parsed_sim_strain[i_point])
        for element, el_responses in zip(elements, parsed_sim_strain[i_point]):

            # Skip any elements belonging to the pier.
            if element.pier:
                continue

            # First calculate the center offset of the integration points..
            if not hasattr(element, "i_point_offset"):
                element.i_point_offset = (
                    element.length() * ((1 / np.sqrt(3)) / 2),
                    element.width() * ((1 / np.sqrt(3)) / 2),
                )
            i_point_x_offset, i_point_z_offset = element.i_point_offset
            i_point_x_offset, i_point_z_offset = 0, 0
            # print()
            # print(element.center())
            # print(element.length(), element.width())
            # print(element.i_point_offset)

            # ..then determine the position of each integration point.
            response_point = deepcopy(element.center())
            if i_point + 1 == 1:
                response_point.x -= i_point_x_offset
                response_point.z -= i_point_z_offset
            elif i_point + 1 == 2:
                response_point.x += i_point_x_offset
                response_point.z -= i_point_z_offset
            elif i_point + 1 == 3:
                response_point.x += i_point_x_offset
                response_point.z += i_point_z_offset
            elif i_point + 1 == 4:
                response_point.x -= i_point_x_offset
                response_point.z += i_point_z_offset
            else:
                raise ValueError("Unknown integration point {i_point + 1}")

            # Calculate and record the response.
            eps11, eps22, _g12, theta11, theta22, theta33, _g13, _g23 = list(
                el_responses
            )
            half_height = element.section.thickness / 2
            # print(response_point.x, response_point.y, response_point.z)
            # print(eps11)
            result.append(
                Response(
                    value=(eps11 - (theta11 * half_height)) * -1e6,
                    x=response_point.x,
                    y=response_point.y,
                    z=response_point.z,
                )
            )

    converted_expt_responses[sim_ind][ResponseType.Strain] = result
    print(len(result))


def convert_responses_3d(
    c: Config, expt_params: ExptParams, parsed_expt_responses: Parsed
) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed OpenSees responses to List[Response]."""
    # A dictionary of simulation index to ResponseType to [Response].
    converted_expt_responses = defaultdict(dict)
    for sim_ind, parsed_sim_responses in parsed_expt_responses.items():
        sim_params = expt_params.sim_params[sim_ind]
        nodes = det_nodes(sim_params.bridge_nodes)
        elements = det_shells(sim_params.bridge_shells)
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
        convert_strain_responses(
            elements=elements,
            sim_ind=sim_ind,
            parsed_sim_responses=parsed_expt_responses[sim_ind],
            converted_expt_responses=converted_expt_responses,
        )
    return converted_expt_responses
