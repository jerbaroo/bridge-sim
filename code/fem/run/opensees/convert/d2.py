"""Convert parsed 2D OpenSees responses to [Response]."""
from typing import Dict, List

from config import Config
from fem.run import Parsed
from model import Response
from model.response import ResponseType


def convert_responses_2d(
    c: Config, parsed_responses: Parsed
) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed 2D OpenSees responses to [Response]."""
    sim_inds = list(parsed_responses.keys())
    for sim_ind in sim_inds:
        sim_responses = parsed_responses[sim_ind]

        def translation_to_responses(trans):
            """Convert data indexed as [time][node] to a list of Response."""
            node_ids = c.os_node_ids()
            return [
                Response(
                    trans[time][i],
                    x=c.bridge.x_min + (i * c.os_node_step),
                    y=c.bridge.y_max,
                    z=c.bridge.z_center,
                    time=time,
                    node_id=node_ids[i],
                )
                for time in range(len(trans))
                for i in range(len(trans[time]))
            ]

        if ResponseType.XTranslation in sim_responses:
            sim_responses[ResponseType.XTranslation] = translation_to_responses(
                sim_responses[ResponseType.XTranslation]
            )
        if ResponseType.YTranslation in sim_responses:
            sim_responses[ResponseType.YTranslation] = translation_to_responses(
                sim_responses[ResponseType.YTranslation]
            )

        # Stress and strain for each section's fiber.

        def stress_to_responses(stress):
            """Stress or strain data to a list of Response."""
            elem_ids = c.os_elem_ids()
            return [
                Response(
                    val,
                    x=(
                        c.bridge.x_min
                        + (i * c.os_node_step)
                        + (c.os_node_step / 2)
                    ),
                    y=point.y,
                    z=point.z,
                    time=time,
                    elem_id=elem_ids[i],
                    section_id=section_id,
                    fiber_cmd_id=fiber_cmd_id,
                )
                for _, (
                    val,
                    i,
                    section_id,
                    time,
                    fiber_cmd_id,
                    point,
                ) in enumerate(stress)
            ]

        if ResponseType.Stress in sim_responses:
            sim_responses[ResponseType.Stress] = stress_to_responses(
                sim_responses[ResponseType.Stress]
            )
        if ResponseType.Strain in sim_responses:
            sim_responses[ResponseType.Strain] = stress_to_responses(
                sim_responses[ResponseType.Strain]
            )

    return parsed_responses
