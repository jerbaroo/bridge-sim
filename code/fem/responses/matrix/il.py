import numpy as np
from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses.matrix import ResponsesMatrix, load_expt_responses
from fem.run import FEMRunner
from model.load import PointLoad
from model.response import ResponseType
from util import print_d

# Print debug information for this file.
D: bool = False


class ILMatrix(ResponsesMatrix):
    """Responses of one sensor type for influence line calculations.

    Each simulation is for a different loading position in the longitudinal
    direction of the bridge. The z position is fixed for one ILMatrix, thus a
    different ILMatrix should be used for each tire track on a bridge.

    """

    def response_to(
            self, x_frac: float, load_x_frac: float, load: float,
            interp_sim: bool = False, interp_response: bool = False,
            y_frac: float = 1, z_frac: float = 0.5, time_index: int = 0):
        """The response value in kN at a position to a load at a position.

        Note that only the loading position in longitudinal direction can be
        chosen 'load_x_frac', the position in transverse direction is fixed for
        a single ILMatrix.

        Args:
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on y-axis in [0 1].
            z_frac: float, response position on x-axis in [0 1].
            load_x_frac: float, load position on x-axis in [0 1].
            load: float, value of the load in kN.
            time_index: int, time index of the simulation.

        """
        assert 0 <= x_frac <= 1
        assert 0 <= load_x_frac <= 1
        print_d(D, f"x_frac = {x_frac} = load_x_frac = {load_x_frac}")
        response = super().sim_response(
            expt_frac=load_x_frac, x_frac=x_frac, y_frac=y_frac, z_frac=z_frac,
            time_index=time_index, interp_sim=interp_sim,
            interp_response=interp_response)
        return response * (load / self.c.il_unit_load_kn)

    @staticmethod
    def load(
            c: Config, response_type: ResponseType, fem_runner: FEMRunner,
            load_z_frac: float, save_all: bool = True) -> "ILMatrix":
        """Load an ILMatrix from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, type of sensor response to load.
            fem_runner: FEMRunner, program to run finite element simulations.
            load_z_frac: float, load position as a fraction of the transverse
                direction in [0 1].
            save_all: bool, whether to save responses from all sensor types when
                running simulations, this is useful if simulations take a long
                time to run and you anticipate needing other sensor types.

        """
        assert 0 <= load_z_frac <= 1
        id_str = (
            f"il-{response_type}-{fem_runner.name}-{c.il_unit_load_kn}"
            + f"-{c.il_num_loads}-zfrac={load_z_frac}")
        print(id_str)

        # Determine experiment simulation parameters.
        _expt_params = ExptParams([
            FEMParams(
                ploads=[PointLoad(
                    x_frac=x_frac, z_frac=load_z_frac, kn=c.il_unit_load_kn)],
                response_types=[response_type])
            for x_frac in np.linspace(0, 1, c.il_num_loads)])

        def load_func(expt_params):
            """Load a ResponsesMatrix from given simulation parameters."""
            il_matrix = ILMatrix(
                c=c, response_type=response_type, expt_params=expt_params,
                fem_runner=fem_runner, save_all=save_all,
                expt_responses=load_expt_responses(
                    c=c, expt_params=expt_params, response_type=response_type,
                    fem_runner=fem_runner))
            il_matrix.load_z_frac = load_z_frac
            return il_matrix

        return ResponsesMatrix.load(
            c=c, id_str=id_str, expt_params=_expt_params, load_func=load_func,
            fem_runner=fem_runner, save_all=save_all)
