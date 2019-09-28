"""Build an OpenSees 2D or 3D model file."""
from config import Config
from fem.params import ExptParams
from fem.run.opensees.build.d2 import build_model_2d
from fem.run.opensees.build.d3 import build_model_3d
from model.bridge import Dimensions


def build_model(c: Config, expt_params: ExptParams, os_runner: "OSRunner"):
    """Build an OpenSees 2D or 3D model file."""
    if c.bridge.dimensions == Dimensions.D2:
        return build_model_2d(
            c=c, expt_params=expt_params, fem_runner=os_runner)
    else:
        return build_model_3d(
            c=c, expt_params=expt_params, os_runner=os_runner)
