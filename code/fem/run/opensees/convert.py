"""Convert parsed OpenSees responses to [Response]."""
from typing import Dict, List

from config import Config
from fem.run import Parsed
from model import *


def convert_responses(c: Config, parsed: Parsed
                     ) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed OpenSees responses to [Response]."""
    sim_inds = list(parsed.keys())
    for sim_ind in sim_inds:
        sim_responses = parsed[sim_ind]

        def translation_to_responses(trans):
            """Convert data indexed as [time][node] to a list of Response."""
            node_ids = c.os_node_ids()
            return [
                Response(trans[time][i], x=i * c.os_node_step, y=0, z=0,
                        time=time, node_id=node_ids[i])
                for time in range(len(trans))
                for i in range(len(trans[time]))]

        if ResponseType.XTranslation in sim_responses:
            sim_responses[ResponseType.XTranslation] = (
                translation_to_responses(
                    sim_responses[ResponseType.XTranslation]))
        if ResponseType.YTranslation in sim_responses:
            sim_responses[ResponseType.YTranslation] = (
                translation_to_responses(
                    sim_responses[ResponseType.YTranslation]))

        ##### Stress and strain for each section's fiber. #####

        def stress_to_responses(stress, section_id, fiber_cmd_id, y, z):
            """Stress or strain data to a list of Response."""
            # TODO: Check assertion makes sense.
            print("")
            print("")
            print("")
            assert len(stress) == _sim_time
            elem_ids = c.os_elem_ids()
            return [
                Response(
                    stress[time][i], x=i * c.os_node_step + (c.os_node_step / 2),
                    y=y, z=z, time=time, elem_id=elem_ids[i],
                    section_id=section_id, fiber_cmd_id=fiber_cmd_id)
                for time in range(len(stress))
                for i in range(len(stress[time]))]

        if ResponseType.Stress in sim_responses:
            sim_responses[ResponseType.Stress] = stress_to_responses(
                sim_responses[ResponseType.Stress], section.id, fiber_cmd_id,
                point.y, point.z)
        if ResponseType.Strain in sim_responses:
            sim_responses[ResponseType.Strain] = stress_to_responses(
                sim_responses[ResponseType.Strain], section.id, fiber_cmd_id,
                point.y, point.z)

    return parsed
