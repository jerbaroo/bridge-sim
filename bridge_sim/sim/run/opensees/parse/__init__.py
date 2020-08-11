"""Parse fem from an OpenSees simulation"""
from typing import List

from bridge_sim.model import Config
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import Parsed
from bridge_sim.sim.run.opensees.parse.d3 import parse_responses_3d
from bridge_sim.util import print_d

# Print debug information for this file.
D: bool = True


def parse_responses(
    c: Config, expt_params: List[SimParams], os_runner: "OSRunner"
) -> Parsed:
    """Parse fem from an OpenSees simulation."""
    print_d(D, f"parsing {c.bridge.dimensions} bridge fem")
    return parse_responses_3d(c=c, expt_params=expt_params, os_runner=os_runner)
