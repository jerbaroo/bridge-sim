"""Convert responses from an OpenSees simulation"""

from typing import Dict, List

from bridge_sim.model import ResponseType, Config
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import Parsed
from bridge_sim.sim.run.opensees.convert.d3 import convert_responses_3d
from bridge_sim.util import print_d

# Print debug information for this file.
D: bool = True


def convert_responses(
    c: Config, expt_params: List[SimParams], parsed_expt_responses: Parsed
) -> Dict[int, Dict[ResponseType, List["Response"]]]:
    """Parse fem from an OpenSees simulation."""
    print_d(D, f"Converting {c.bridge.dimensions} bridge fem")
    return convert_responses_3d(
        c=c, expt_params=expt_params, parsed_expt_responses=parsed_expt_responses,
    )
