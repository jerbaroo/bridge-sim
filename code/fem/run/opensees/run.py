"""Run an OpenSees simulation."""
import subprocess

from config import Config
from fem.params import ExptParams
from fem.run import FEMRunner


def run_model(
    c: Config, expt_params: ExptParams, fem_runner: FEMRunner, sim_ind: int
):
    """Run an OpenSees simulation."""
    subprocess.run(
        [
            c.os_exe_path,
            fem_runner.sim_raw_path(
                sim_params=expt_params.sim_params[sim_ind], ext="tcl"
            ),
        ]
    )
    return expt_params
