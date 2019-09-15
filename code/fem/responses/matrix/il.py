import numpy as np
from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses.matrix import ResponsesMatrix, load_expt_responses
from fem.run import FEMRunner
from model.load import Load
from model.response import ResponseType
from util import print_d

# Print debug information for this file.
D: bool = False


class ILMatrix(ResponsesMatrix):
    """Responses of one sensor type for influence line simulations."""

    def response(
            self, x_frac: float, load_x_frac: float, load: float,
            interp_load: bool = False, interp_response: bool = False,
            y_frac: float = 1, z_frac: float = 0.5, time_index: int = 0):
        """The response value in kN at a position to a load at a position.

        Args:
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on x-axis in [0 1].
            z_frac: float, response position on x-axis in [0 1].
            load_x_frac: float, load position on x-axis in [0 1].
            load: float, value of the load in kN.
            time_index: int, time index of the simulation.

        """
        assert 0 <= x_frac <= 1
        assert 0 <= load_x_frac <= 1
        print_d(D, f"x_frac = {x_frac} = load_x_frac = {load_x_frac}")
        response = super()._response(
            expt_frac=load_x_frac, x_frac=x_frac, y_frac=y_frac, z_frac=z_frac,
            time_index=time_index, interp_load=interp_load,
            interp_response=interp_response)
        return response * (load / self.c.il_unit_load_kn)


def load_il_matrix(
        c: Config, response_type: ResponseType, fem_runner: FEMRunner,
        save_all: bool = True) -> ILMatrix:
    """Load an ILMatrix from disk, running simulations first if necessary.

    Args:
        c: Config, global configuration object.
        response_type: ResponseType, the type of sensor response to load.
        fem_runner: FEMRunner, the FEM program to run simulations with.
        save_all: bool, save all response types when running a simulation.

    """
    id_str = (
        f"il-{response_type}-{fem_runner.name}-{c.il_unit_load_kn}"
        + f"-{c.il_num_loads}")

    # Determine experiment simulation parameters.
    _expt_params = ExptParams([
        FEMParams(
            loads=[Load(x_frac, c.il_unit_load_kn)],
            response_types=[response_type])
        for x_frac in np.linspace(0, 1, c.il_num_loads)])

    def load_func(expt_params):
        return ILMatrix(
            c=c, response_type=response_type, expt_params=expt_params,
            fem_runner_name=fem_runner.name,
            expt_responses=load_expt_responses(
                c, expt_params, response_type, fem_runner))

    return ResponsesMatrix.load(
        c=c, id_str=id_str, expt_params=_expt_params, load_func=load_func,
        save_all=save_all)
