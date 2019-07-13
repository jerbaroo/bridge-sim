"""Convert parsed Diana responses to [Response]."""
from collections import defaultdict
from typing import Dict, List

from config import Config
from fem.params import ExptParams
from fem.run import Parsed
from model import *


def convert_responses(c: Config, expt_params: ExptParams, parsed: Parsed,
                     ) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Convert parsed Diana responses to [Response]."""
    if not expt_params.is_mobile_load():
        raise ValueError("Diana: only MOBILE load supported")

    results = defaultdict(dict)
    response_types = expt_params.fem_params[0].response_types

    if ResponseType.XTranslation in response_types:
        for sim in parsed["translation"]:
            results[sim][ResponseType.XTranslation] = [
                Response(dx, x=x, y=y, z=z, time=sim, node_id=node_id)
                for node_id, dx, _dy, _dz, x, y, z
                in parsed["translation"][sim]]

    if ResponseType.YTranslation in response_types:
        results[sim][ResponseType.YTranslation] = [
            Response(dy, x=x, y=y, z=z, time=sim, node_id=node_id)
            for sim in parsed["translation"]
            for node_id, _dx, dy, _dz, x, y, z in parsed["translation"][sim]]

    if ResponseType.Strain in response_types:
        results[sim][ResponseType.Strain] = [
            Response(ey, x=x, y=y, z=z, time=sim, elem_id=elem_id,
                     srf_id=srf_id, node_id=node_id)
            for sim in parsed["strain"]
            for elem_id, srf_id, node_id, _ex, ey, _ez, gx, gy, gz, x, y, z
            in parsed["strain"][sim]]

    return results
