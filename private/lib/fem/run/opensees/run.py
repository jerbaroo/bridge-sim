"""Run an OpenSees simulation."""
import subprocess

from lib.config import Config
from lib.fem.params import ExptParams
from lib.fem.run import FEMRunner


def run_model(c: Config, expt_params: ExptParams, fem_runner: FEMRunner, sim_ind: int):
    """Run an OpenSees simulation."""
    subprocess.run(
        [
            fem_runner.exe_path,
            fem_runner.sim_raw_path(
                sim_params=expt_params.sim_params[sim_ind], ext="tcl"
            ),
        ]
    )
    return expt_params
