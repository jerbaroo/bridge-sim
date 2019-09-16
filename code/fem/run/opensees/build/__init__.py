"""Build OpenSees 2D or 3D model files."""
from config import Config
from fem.params import ExptParams
from fem.run.opensees.build.d2 import build_model as build_2d
from fem.run.opensees.build.d3 import build_model as build_3d
from model.bridge import Dimensions


def build_model(c: Config, expt_params: ExptParams, fem_runner: "OSRunner"):
    if c.bridge.dimensions == Dimensions.D2:
        return build_2d(c=c, expt_params=expt_params, fem_runner=fem_runner)
    else:
        return build_3d(c=c, expt_params=expt_params, fem_runner=fem_runner)
