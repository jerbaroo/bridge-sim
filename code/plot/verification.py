"""Verification-related plots"""
from config import Config
from fem.params import FEMParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import Load
from model.response import ResponseType
from plot import plt


def plot_convergence_with_shell_size(max_shell_areas):
    """Plot responses as shell density is increased."""
    response_type = ResponseType.YTranslation
    fem_params = FEMParams(
        loads=[Load(x_frac=35 / 102.75, kn=100)],
        response_types=[response_type])
    maxes = []
    for max_shell_area in max_shell_areas:
        c = bridge_705_config(
            bridge=bridge_705_3d, max_shell_area=max_shell_area)
        fem_runner = OSRunner(c)
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=fem_runner)
        maxes.append(max(r.value for r in fem_responses._responses))
    print(max_shell_areas)
    print(maxes)
    plt.plot(max_shell_areas, maxes)
    plt.show()
