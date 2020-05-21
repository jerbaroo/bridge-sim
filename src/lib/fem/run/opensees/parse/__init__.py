"""Parse responses from an OpenSees simulation"""
from bridge_sim.model import Config
from lib.fem.params import ExptParams
from lib.fem.run import Parsed
from lib.fem.run.opensees.parse.d3 import parse_responses_3d
from util import print_d

# Print debug information for this file.
D: bool = True


def parse_responses(
    c: Config, expt_params: ExptParams, os_runner: "OSRunner"
) -> Parsed:
    """Parse responses from an OpenSees simulation."""
    print_d(D, f"parsing {c.bridge.dimensions} bridge responses")
    return parse_responses_3d(c=c, expt_params=expt_params, os_runner=os_runner)
