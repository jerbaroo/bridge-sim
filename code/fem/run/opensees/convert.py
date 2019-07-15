"""Convert parsed OpenSees responses to [Response]."""
from typing import Dict, List

from config import Config
from fem.run import Parsed
from model import *


def convert_responses(c: Config, parsed: Parsed, _
                     ) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed responses to Responses."""

    def translation_to_responses(trans):
        """Convert data indexed as [time][node] to a list of Response."""
        node_ids = c.os_node_ids()
        return [
            Response(trans[time][i], x=i * c.os_node_step, y=0, z=0,
                     time=time, node_id=node_ids[i])
            for time in range(len(trans))
            for i in range(len(trans[time]))]

    if ResponseType.XTranslation in parsed:
        x = translation_to_responses(parsed[ResponseType.XTranslation])
    if ResponseType.YTranslation in parsed:
        y = translation_to_responses(parsed[ResponseType.YTranslation])

    ##### Stress and strain for each section's fiber. #####

    def stress_to_responses(stress, section_id, fiber_cmd_id, y, z):
        """Stress or strain data to a list of Response."""
        # TODO: Check assertion makes sense.
        assert len(stress) == _sim_time
        elem_ids = c.os_elem_ids()
        return [
            Response(
                stress[time][i], x=i * c.os_node_step + (c.os_node_step / 2),
                y=y, z=z, time=time, elem_id=elem_ids[i],
                section_id=section_id, fiber_cmd_id=fiber_cmd_id)
            for time in range(len(stress))
            for i in range(len(stress[time]))]

    if ResponseType.Stress in parsed:
        stress = stress_to_responses(
            parsed[ResponseType.Stress], section.id, fiber_cmd_id, point.y,
            point.z)
    if ResponseType.Strain in parsed:
        strain = stress_to_responses(
            parsed[ResponseType.Strain], section.id, fiber_cmd_id, point.y,
            point.z)

    return {
        ResponseType.XTranslation:
            x if ResponseType.XTranslation in parsed else None,
        ResponseType.YTranslation:
            y if ResponseType.YTranslation in parsed else None,
        ResponseType.Stress:
            stress if ResponseType.Stress in parsed else None,
        ResponseType.Strain:
            strain if ResponseType.Strain in parsed else None
    }
