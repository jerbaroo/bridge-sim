"""Convert parsed Diana responses to [Response]."""
from typing import Dict, List

from config import Config
from fem.run import Parsed
from model import *


def convert_responses(c: Config, parsed: Parsed,
                      response_types: List[ResponseType]
                     ) -> Dict[ResponseType, List[Response]]:
    """Convert parsed Diana responses to [Response]."""
    results = dict()

    if ResponseType.XTranslation in response_types:
        results[ResponseType.XTranslation] = [
            Response(dx, x=x, y=y, z=z, time=time, node_id=node_id)
            for time in parsed["translation"]
            for node_id, dx, _dy, _dz, x, y, z in parsed["translation"][time]]

    if ResponseType.YTranslation in response_types:
        results[ResponseType.YTranslation] = [
            Response(dy, x=x, y=y, z=z, time=time, node_id=node_id)
            for time in parsed["translation"]
            for node_id, _dx, dy, _dz, x, y, z in parsed["translation"][time]]

    if ResponseType.Strain in response_types:
        results[ResponseType.Strain] = [
            Response(ey, x=x, y=y, z=z, time=time, elem_id=elem_id,
                     srf_id=srf_id, node_id=node_id)
            for time in parsed["strain"]
            for elem_id, srf_id, node_id, _ex, ey, _ez, gx, gy, gz, x, y, z
            in parsed["strain"][time]]

    return results
