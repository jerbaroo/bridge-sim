"""Run a Diana simulation."""
import os
import subprocess

from config import Config
from fem.params import ExptParams


def run_model(c: Config, expt_params: ExptParams):
    """Run a Diana simulation."""
    if not expt_params.is_mobile_load():
        raise ValueError("Diana: only MOBILE load supported")
    out = ".out"
    assert c.di_out_path.endswith(out)
    os.remove(c.di_filos_path)
    result = subprocess.run(
        [
            c.di_exe_path,
            c.di_model_path,
            c.di_cmd_path,
            c.di_out_path[: -len(out)],
            c.di_filos_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.stderr:
        print(result.stderr.decode("utf-8"))
        # Print output log.
        with open(c.di_out_path) as f:
            print(f.read())
    os.rm(c.di_filos_path)
    os.rm(c.di_out_path)
    return expt_params
