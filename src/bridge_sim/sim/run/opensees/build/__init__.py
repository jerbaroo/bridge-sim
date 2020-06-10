"""Build an OpenSees model file."""
from typing import List

from bridge_sim.model import Config
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run.opensees.build.d3 import build_model_3d


def build_model(
    c: Config, expt_params: List[SimParams], fem_runner: "OSRunner",
):
    """Build an OpenSees 2D or 3D model file."""
    return build_model_3d(c=c, expt_params=expt_params, os_runner=fem_runner)
