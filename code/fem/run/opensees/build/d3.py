"""Build OpenSees 3D model files."""
from config import Config
from fem.params import ExptParams


def build_model(c: Config, expt_params: ExptParams, fem_runner: "OSRunner"):
    raise NotImplementedError()

