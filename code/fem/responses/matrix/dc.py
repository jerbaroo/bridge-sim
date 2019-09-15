from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses.matrix import ResponsesMatrix, load_expt_responses
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from model.load import DisplacementCtrl
from model.response import ResponseType


class DCMatrix(ResponsesMatrix):
    """Responses of one sensor type for displacement control simulations.

    Note the displacement is set when loading an instance of this class.

    """

    def response_to(
            self, x_frac: float, load_x_frac: float, load: float,
            interp_sim: bool = False, interp_response: bool = False,
            y_frac: float = 1, z_frac: float = 0.5, time_index: int = 0):
        """The response value in kN at a position to a load at a position.

        Args:
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on x-axis in [0 1].
            z_frac: float, response position on x-axis in [0 1].
            load_x_frac: float, pier position on x-axis in [0 1].
            load: float, value of the load in kN.
            time_index: int, time index of the simulation.

        """
        # Response due to displacement at a pier
        dc_response = self.sim_response(
            expt_frac=load_x_frac, x_frac=x_frac, y_frac=y_frac, z_frac=z_frac,
            time_index=time_index, interp_response=interp_response)
        # Response due to load under normal bridge conditions.
        il_matrix = ILMatrix.load(
            c=self.c, response_type=self.response_type,
            fem_runner=self.fem_runner, save_all=self.save_all)
        il_response = il_matrix.response_to(
            x_frac=x_frac, load_x_frac=load_x_frac, load=load,
            interp_sim=interp_sim, interp_response=interp_response,
            y_frac=y_frac, z_frac=z_frac, time_index=time_index)
        # Return summation of both responses.
        return dc_response + il_response

    @staticmethod
    def load(
            c: Config, response_type: ResponseType, fem_runner: FEMRunner,
            displacement: float = 0.1, save_all: bool = True):
        """Load a DCMatrix from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, the type of sensor response to load.
            fem_runner: FEMRunner, the FEM program to run simulations with.
            displacement: float, the displacement at each pier in meters.
            save_all: bool, save all response types when running a simulation.

        """

        id_str = f"dc-{response_type}-{fem_runner.name}-{displacement}"

        # Determine experiment simulation parameters.
        _expt_params = ExptParams([
            FEMParams(
                loads=[],
                displacement_ctrl=DisplacementCtrl(displacement, i),
                response_types=[response_type])
            for i in range(len(c.bridge.supports))])

        def load_func(expt_params):
            return DCMatrix(
                c=c, response_type=response_type, expt_params=expt_params,
                fem_runner=fem_runner, save_all=save_all,
                expt_responses=load_expt_responses(
                    c=c, expt_params=expt_params, response_type=response_type,
                    fem_runner=fem_runner))

        return ResponsesMatrix.load(
            c=c, id_str=id_str, expt_params=_expt_params, load_func=load_func,
            save_all=save_all)
