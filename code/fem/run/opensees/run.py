"""Run an OpenSees simulation."""
import subprocess

from config import Config
from fem.params import ExptParams
from fem.run import FEMRunner, fem_file_path


def run_model(c: Config, expt_params: ExptParams, fem_runner: FEMRunner):
    """Run an OpenSees simulation."""
    for fem_params in expt_params.fem_params:
        subprocess.run(
            [c.os_exe_path, built_model_path(fem_params, fem_runner)])
    return expt_params
