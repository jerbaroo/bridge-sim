from config import Config
from fem.params import ExptParams, FEMParams
from fem.responses.matrix import ResponsesMatrix, load_expt_responses
from fem.run import FEMRunner
from model.load import DisplacementCtrl
from model.response import ResponseType


class DCMatrix(ResponsesMatrix):
    """Responses of one sensor type for displacement control simulations."""

    # TODO Factor out to ResponsesMatrix.load.
    @staticmethod
    def load(
            c: Config, response_type: ResponseType, fem_runner: FEMRunner,
            displacement: float = 0.1, save_all: bool = True):
        """Load a DCMatrix from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration.
            response_type: ResponseType, the type of response to load.
            fem_runner: FEMRunner, the FEM program to run simulations with.
            displacement: float, the extent of the displacement at each pier.
            save_all: bool, save all response types when running a simulation.

        """

        def dc_matrix_id() -> str:
            return f"dc-{response_type}-{fem_runner.name}-{displacement}"

        # Return ILMatrix if already calculated.
        id_ = dc_matrix_id()
        if id_ in c.il_matrices:
            return c.il_matrices[id_]

        # Determine simulation parameters.
        # If save_all is true pass all response types.
        response_types = (
            [rt for rt in ResponseType] if save_all else [response_type])
        expt_params = ExptParams([
            FEMParams(
                loads=[],
                displacement_ctrl=DisplacementCtrl(displacement, i),
                response_types=response_types)
            for i in range(len(c.bridge.fixed_nodes))])

        # Calculate DCMatrix, keep a reference and return.
        c.il_matrices[id_] = DCMatrix(
            c, response_type, expt_params, fem_runner.name,
            load_expt_responses(c, expt_params, response_type, fem_runner))
        return c.il_matrices[id_]
