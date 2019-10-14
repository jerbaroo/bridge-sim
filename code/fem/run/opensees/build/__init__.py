"""Build an OpenSees 2D or 3D model file."""
from config import Config
from fem.params import ExptParams
from fem.run.opensees.build.d2 import build_model_2d
from fem.run.opensees.build.d3 import build_model_3d
from model.bridge import Dimensions


def build_model(
        c: Config, expt_params: ExptParams, fem_runner: "OSRunner",
        include_support_3d_nodes: bool = True):
    """Build an OpenSees 2D or 3D model file.

    Args:
        c: Config, global configuratin object.
        include_support_3d_nodes: bool, for testing, if False don't include the
            nodes for the supports.

    """
    if c.bridge.dimensions == Dimensions.D2:
        return build_model_2d(
            c=c, expt_params=expt_params, os_runner=fem_runner)
    else:
        return build_model_3d(
            c=c, expt_params=expt_params, os_runner=fem_runner,
            include_support_nodes=include_support_3d_nodes)
