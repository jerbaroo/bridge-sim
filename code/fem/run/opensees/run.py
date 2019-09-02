"""Run an OpenSees simulation."""
import subprocess

from config import Config
from fem.params import ExptParams
from fem.run import FEMRunner


def run_model(
        c: Config, expt_params: ExptParams, fem_runner: FEMRunner,
        sim_ind: int):
    """Run an OpenSees simulation."""
    subprocess.run(
        [c.os_exe_path,
         fem_runner.fem_file_path(expt_params.fem_params[sim_ind])])
    return expt_params
