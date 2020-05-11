"""Build an OpenSees 2D or 3D model file."""
from lib.config import Config
from lib.fem.params import ExptParams
from lib.fem.run.opensees.build.d2 import build_model_2d
from lib.fem.run.opensees.build.d3 import build_model_3d
from lib.model.bridge import Dimensions


def build_model(
    c: Config, expt_params: ExptParams, fem_runner: "OSRunner",
):
    """Build an OpenSees 2D or 3D model file."""
    if c.bridge.dimensions == Dimensions.D2:
        return build_model_2d(c=c, expt_params=expt_params, os_runner=fem_runner)
    else:
        return build_model_3d(c=c, expt_params=expt_params, os_runner=fem_runner)
