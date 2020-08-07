"""Run an OpenSees simulation."""
import subprocess
from typing import List

from bridge_sim.model import Config
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import FEMRunner


def run_model(
    c: Config, expt_params: List[SimParams], fem_runner: FEMRunner, sim_ind: int
):
    """Run an OpenSees simulation."""
    subprocess.run(
        [
            fem_runner.exe_path,
            fem_runner.sim_model_path(
                config=c, sim_params=expt_params[sim_ind], ext="tcl"
            ),
        ]
    )
    return expt_params
