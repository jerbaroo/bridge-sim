"""Run an OpenSees simulation."""
import subprocess

from config import Config
from fem.params import ExptParams
from fem.run import FEMRunner, fem_file_path
from util import *


def run_model(c: Config, expt_params: ExptParams, fem_runner: FEMRunner,
              sim_ind: int):
    """Run an OpenSees simulation."""
    subprocess.run(
        [c.os_exe_path,
         fem_file_path(expt_params.fem_params[sim_ind], fem_runner)])
    return expt_params
