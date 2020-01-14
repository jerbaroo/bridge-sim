"""Convert responses from an OpenSees simulation"""
from typing import Dict, List
from config import Config
from fem.params import ExptParams
from fem.run import Parsed
from fem.run.opensees.convert.d2 import convert_responses_2d
from fem.run.opensees.convert.d3 import convert_responses_3d
from model.bridge import Dimensions
from model.response import Response, ResponseType
from util import print_d

# Print debug information for this file.
D: bool = True


def convert_responses(
    c: Config, expt_params: ExptParams, parsed_expt_responses: Parsed
) -> Dict[int, Dict[ResponseType, List[Response]]]:
    """Parse responses from an OpenSees simulation."""
    print_d(D, f"Converting {c.bridge.dimensions} bridge responses")
    if c.bridge.dimensions == Dimensions.D2:
        return convert_responses_2d(c=c, parsed_responses=parsed_expt_responses)
    else:
        return convert_responses_3d(
            c=c, expt_params=expt_params, parsed_expt_responses=parsed_expt_responses,
        )
